# 🚪 DoorPro: Simulador de Prospección Comercial Puerta a Puerta

Un simulador interactivo y pedagógico para entrenar a vendedores, asesores de cambaceo y prospectores comerciales en ventas en frío cara a cara en terreno.

Desarrollado con **Python + Django 6**, plantillas de **Django Templates**, estilos modernos con **Tailwind CSS** e interacción reactiva en tiempo real mediante **HTMX** (sin frameworks pesados como React ni compiladores de JavaScript). Diseñado para ser **100% gratuito**, sin requerir tarjetas de crédito ni suscripciones a APIs.

---

## 🌟 Características Principales

### 1. 🎭 Arquetipos Psicológicos Reales de Puerta Fría
Cada casa cuenta con perfiles de comportamiento calibrados según la psicología de campo:
- **El Ocupado / Con Prisa**: Tiene la mano en el pomo o el coche encendido. Exige ganchos de menos de 15 segundos; los discursos corporativos largos provocan portazos inmediatos.
- **El Desconfiado / Escéptico**: Teme fraudes y exige pruebas. Se desarma con validación de desconfianza y pruebas sociales de vecinos cercanos.
- **El Amable Evasivo ("El del Folleto")**: Sonríe amablemente y pide un folleto para deshacerse de ti. Entrena la técnica de aceptar y redirigir con preguntas de dolor.
- **El Hostil / Malhumorado**: Pone a prueba la resiliencia emocional del vendedor. Enseña a desescalar conflictos con respeto absoluto o retirarse con dignidad.
- **El Prospecto Calificado (Golden Lead)**: Tiene una necesidad activa. Premia el cierre directo y castiga la cobardía o la sobre-explicación.
- **Nadie en Casa**: Enseña la disciplina de no perder tiempo en puertas vacías y dejar un colgador (*Door Hanger*).

### 2. ⚡ Dinámica de Juego y Atributos RPG
- **Medidores en Vivo**: Cada prospecto cuenta con barras interactivas de **Paciencia** (que se agota con respuestas largas o agresivas) e **Interés Comercial** (que sube al descubrir dolores reales).
- **Habilidades del Vendedor**:
  - *Empatía y Escucha*: Reduce la desconfianza inicial y calma prospectos tensos.
  - *Persuasión & Objeciones*: Aumenta el impacto positivo al refutar excusas.
  - *Resiliencia Emocional*: Mitiga la pérdida de moral y energía ante rechazos agresivos.
  - *Técnica de Cierre*: Aumenta el éxito al solicitar la cita o la firma de contrato.
- **Entrenamiento Continuo**: Invierte las comisiones ganadas ($) para subir de nivel tus atributos de venta.

### 3. 🧠 Sales Coach Virtual
- Retroalimentación pedagógica instantánea tras cada elección: explica **por qué** funcionó o falló una respuesta, citando metodologías de venta real (Sandler, SPIN, Cierre de Doble Alternativa, Escucha Activa).
- Reporte detallado al final de la jornada con embudo de conversión (Funnel), análisis de errores recurrentes y la "regla de oro" del día.

### 4. 🏙️ Variedad de Productos y Mercados
- **Campaña de Telecom**: Fibra Óptica 500 Megas.
- **Campaña de Seguridad**: Alarmas y Cámaras Inteligentes 24/7.
- **Campaña Fintech / B2B**: Terminales Punto de Venta (TPV) para pequeños comercios.
- **Campaña de Energía**: Paneles Solares Residenciales.
- Zonas residenciales y corredores comerciales con diferentes dificultades y tasas de apertura.

---

## 🚀 Puesta en Marcha (100% Gratuito y Local)

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Ejecutar las migraciones y poblar datos iniciales
```bash
python manage.py migrate
python manage.py seed_data
```

### 3. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

Abre en tu navegador:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Pruebas Automatizadas
Para ejecutar la suite completa de pruebas unitarias y de integración:
```bash
python manage.py test
```

---

## 🛠️ Arquitectura Técnica
- **Backend**: Django 6.1 (Python 3.12)
- **Base de Datos**: SQLite 3 (embebida, cero costo)
- **Vistas**: Vistas tradicionales de Django combinadas con respuestas parciales HTMX para actualización instantánea sin recarga de pantalla.
- **Frontend / UI**: Django Templates + Tailwind CSS (vía CDN) + HTMX (vía CDN). Cero dependencias de Node.js, Webpack o npm.
