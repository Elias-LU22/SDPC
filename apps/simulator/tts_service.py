import os
import re
import hashlib
import asyncio
from django.conf import settings

# Voces neuronales de alta fidelidad para el mercado hispano en Texas
VOICE_MALE = "es-US-AlonsoNeural"
VOICE_FEMALE = "es-US-PalomaNeural"

# Directorio de caché local para evitar re-sintetizar frases idénticas
CACHE_DIR = os.path.join(settings.BASE_DIR, "cache", "tts")


def clean_tts_text(text):
    """
    Limpia el texto eliminando acotaciones entre corchetes, viñetas,
    marcas de markdown y espacios redundantes para locución natural.
    """
    if not text:
        return ""
    # Eliminar acotaciones escénicas entre corchetes [Abre la puerta], [Cierra la puerta]
    cleaned = re.sub(r'\[.*?\]', '', text)
    # Eliminar formato markdown
    cleaned = re.sub(r'[*_#`~]', '', cleaned)
    # Reemplazar múltiples espacios o saltos de línea por un único espacio
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned[:600]


def get_cache_path(voice, text):
    """
    Genera una ruta única de archivo basada en el hash SHA-256 de la voz y el texto.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = f"{voice}:{text}".encode("utf-8")
    filename = hashlib.sha256(key).hexdigest() + ".mp3"
    return os.path.join(CACHE_DIR, filename)


async def _synthesize_edge_tts_async(text, voice, output_path):
    """
    Ejecuta la llamada asíncrona a edge-tts para generar el archivo de audio MP3.
    """
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def synthesize_speech(text, gender="M", timeout=5):
    """
    Sintetiza el texto usando la voz neuronal de Microsoft correspondiente al género.
    Devuelve los bytes de audio MP3 si se genera o existe en caché, o None en caso de fallo.
    """
    clean_text = clean_tts_text(text)
    if not clean_text or len(clean_text) < 2:
        return None

    voice = VOICE_FEMALE if (gender or "").upper() == "F" else VOICE_MALE
    cache_path = get_cache_path(voice, clean_text)

    # 1. Comprobar si ya existe en la caché local en disco
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        try:
            with open(cache_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"[TTS] Error al leer archivo en caché: {e}")

    # 2. Intentar sintetizar en línea mediante edge-tts
    try:
        # Ejecutar la corutina asíncrona con límite de tiempo
        asyncio.run(asyncio.wait_for(_synthesize_edge_tts_async(clean_text, voice, cache_path), timeout=timeout))

        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            with open(cache_path, "rb") as f:
                return f.read()
    except ImportError:
        print("[TTS] Paquete edge-tts no instalado en el entorno local. Se usará fallback del navegador.")
    except Exception as e:
        print(f"[TTS] Excepción durante la síntesis con {voice}: {e}")
        # Si falló la creación, limpiar cualquier archivo incompleto
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except Exception:
                pass

    return None
