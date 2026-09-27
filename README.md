# DoorPro: Simulador de Prospección Comercial Puerta a Puerta

Simulador interactivo en pantalla única para entrenamiento de asesores comerciales y prospectores en venta directa cara a cara en terreno.

Desarrollado con **Python + Django 6**, **Django Templates**, estilos limpios con **Tailwind CSS** (paleta verde-azul / teal), iconos SVG profesionales y comunicación dinámica en tiempo real mediante **HTMX**.

El proyecto es **100% gratuito**, no persiste datos en base de datos (todo se gestiona en memoria de sesión HTTP) y no requiere conexión a APIs externas ni modelos de pago.

---

## Características Principales

### 1. Pantalla Única de Chat
- Toda la simulación se ejecuta en una única interfaz de mensajería limpia, sobria y profesional, sin degradados ni emojis.
- Indicadores en tiempo real de **Paciencia del Residente** e **Interés Comercial**.
- Botón **Siguiente Puerta** para cambiar de prospecto en cualquier momento.
- Botón **Reiniciar** para repetir el contacto desde el inicio.

### 2. Arquetipos de Prospecto en Puerta Fría
- **El Ocupado**: Valora el tiempo; exige ganchos de 15 segundos y castiga los discursos largos corporativos.
- **El Desconfiado**: Teme estafas; se desarma con validación de su precaución y referencias de vecinos.
- **El Amable Evasivo**: Solicita el folleto para terminar la conversación; requiere aplicar preguntas de indagación de dolor antes de entregar material.
- **El Hostil**: Prueba la resiliencia y el control emocional; enseña desescalada profesional con respeto absoluto.
- **El Prospecto Calificado**: Cuenta con una necesidad activa; premia el cierre directo.

### 3. Asesoría del Coach Comercial
- Cada turno genera un análisis táctico en vivo que explica la efectividad de la respuesta seleccionada o redactada por el usuario.

---

## Puesta en Marcha

### 1. Activar entorno virtual
```bash
source venv/bin/activate
```

### 2. Iniciar el servidor
```bash
python manage.py runserver
```

Abre en tu navegador:
**http://127.0.0.1:8000/**

---

## Pruebas Automatizadas
```bash
python manage.py test
```
# SDPC
