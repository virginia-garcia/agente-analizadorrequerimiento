# Agente-Analizador de Requerimiento

## Objetivo

Desarrollar un flujo de trabajo que permita transformar requerimientos de negocio en documentación funcional estructurada, facilitando la comunicación entre stakeholders y equipos técnicos.

## Caso de uso de ejemplo

Una plataforma de e-commerce necesita mejorar su sistema de recomendaciones de productos para aumentar la conversión de ventas.

## Solución propuesta

Se diseñó un asistente basado en IA generativa capaz de procesar requerimientos en lenguaje natural y generar automáticamente:

- Historias de usuario
- Criterios de aceptación
- Propuestas de solución técnica
- Identificación de riesgos
- Métricas de éxito

El resultado se puede descargar como documento **Word, PDF, Markdown o JSON**, listo para enviar a un cliente.

### Qué contiene el documento generado

| Sección                          | Detalle                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------- |
| **Historias de usuario**         | Entre 5 y 8, con ID (HU-01), título y prioridad (Alta / Media / Baja)                    |
| **Criterios de aceptación**      | De 3 a 5 por historia, en formato _Dado / Cuando / Entonces_, con casos borde y de error |
| **Requisitos no funcionales**    | Rendimiento, seguridad, privacidad, disponibilidad                                       |
| **Solución técnica**             | Enfoque, componentes y datos necesarios                                                  |
| **Riesgos**                      | Técnicos y de negocio, cada uno con su mitigación                                        |
| **Métricas de éxito**            | Con objetivos numéricos                                                                  |
| **Supuestos y fuera de alcance** | Para delimitar el proyecto                                                               |
| **Preguntas abiertas**           | Ambigüedades que el negocio debe aclarar                                                 |

## Cómo funciona?

Un flujo de **tres agentes** que se pasan el trabajo entre sí:

```
Requerimiento ──►  Analista ──► Revisor ──►  Refinador ──► 📄 Word / PDF / MD / JSON
                   (borrador)     (critica)       (corrige)
```

1. **Analista:** genera el borrador completo siguiendo una guía de profundidad mínima.
2. **Revisor:** actúa como crítico. Busca criterios no medibles, historias sin casos borde, riesgos omitidos y métricas sin objetivo numérico.
3. **Refinador:** si el revisor no aprueba, corrige el borrador aplicando sus observaciones.

### Validación con Pydantic

Cada respuesta del modelo se valida contra un esquema (`modelos.py`). Si el JSON está incompleto o mal formado, el agente **reintenta pasándole el error al modelo** para que se autocorrija. Además, el esquema fija mínimos de calidad (por ejemplo, al menos 4 historias y 3 criterios por historia), de modo que un documento demasiado pobre no llega al usuario.

## Pasos de configuración para poder utilizar este programa

### 1. Tener Python instalado

Primero verificá si ya lo tenés:

```bash
python --version        # o, si usás python3: python3 --version
```

Si te aparece una versión (ej: 3.11), ya estás lista. Se recomienda **Python 3.10 o superior**.
Si no → tenés que instalarlo desde [python.org](https://www.python.org/downloads/).

### 2. Clonar el repositorio e instalar las librerías necesarias

```bash
git clone https://github.com/virginia-garcia/agente-analizadorrequerimiento.git
cd agente-analizadorrequerimiento

pip install -r requirements.txt      # o, si usás python3: pip3 install -r requirements.txt
```

Esto instala `openai`, `pydantic`, `streamlit`, `python-docx`, `reportlab` y el resto de las dependencias.

### 3. API Key

Necesitás una clave de OpenAI.

Pasos:

1. Ir a <https://platform.openai.com/>
2. Crear cuenta / loguearte
3. Generar una API Key
4. Copiar el archivo de ejemplo y pegar tu clave:

```bash
cp .env.example .env        # en Windows: copy .env.example .env
```

```
OPENAI_API_KEY=sk-...
```

El archivo `.env` está en `.gitignore`, así que tu clave no se sube al repositorio.

**Modelo:** por defecto usa `gpt-4o-mini`. Para cambiarlo, agregá `OPENAI_MODEL=gpt-4o` en el `.env`.

## Uso

### Interfaz web (Streamlit)

```bash
streamlit run app.py
```

Escribí el requerimiento, presioná **Generar documentación** y descargá el resultado en Word, PDF o Markdown. La app muestra el documento, lo que observó el revisor y el JSON validado.

<!-- Agregá acá una captura de la app: ![Demo](ejemplos/captura.png) -->

### Línea de comandos

```bash
# Un requerimiento en texto, salida en Markdown (por defecto)
python principal.py "Un e-commerce quiere mejorar recomendaciones"

# Desde un archivo, con varios formatos a la vez
python principal.py --archivo requerimiento.txt --formato md docx pdf json

# Cambiar la carpeta de salida
python principal.py "..." --formato pdf --salida documentos
```

Los archivos se guardan en `salida/` con fecha y hora.

## Estructura del proyecto

| Archivo        | Rol                                                               |
| -------------- | ----------------------------------------------------------------- |
| `modelos.py`   | Esquemas Pydantic del documento y sus mínimos de calidad          |
| `agente.py`    | Flujo Analista → Revisor → Refinador, con validación y reintentos |
| `exportar.py`  | Exportación a Markdown, Word (`python-docx`) y PDF (`reportlab`)  |
| `app.py`       | Interfaz web con Streamlit                                        |
| `principal.py` | Interfaz de línea de comandos                                     |
| `tests/`       | Tests con el LLM simulado (no consumen API)                       |
| `ejemplos/`    | Muestras de Word y PDF                                            |

## Tests

```bash
pytest
```

Los tests simulan las respuestas del modelo, por lo que no requieren API key ni generan costos. Cubren:

- que los exportadores generen archivos Word y PDF válidos;
- el reintento automático cuando el JSON del modelo es inválido;
- el flujo completo con el paso del refinador;
- el rechazo de documentos por debajo del mínimo de calidad.

## Limitaciones

- La calidad del documento depende del modelo y de qué tan claro sea el requerimiento de entrada. Conviene que un analista lo **revise antes de enviarlo** a un cliente.
- La generación tarda entre 15 y 30 segundos, porque hace varias llamadas al modelo.
- Cada ejecución consume tokens de la API de OpenAI.

## Próximos pasos

- [ ] Herramientas para el agente (por ejemplo, crear tickets en Jira o Trello).
- [ ] Soporte para requerimientos en PDF o Word como entrada.
- [ ] API REST con FastAPI.
- [ ] Contenedor Docker.

## Stack

Python · OpenAI API · Pydantic · Streamlit · python-docx · ReportLab · pytest
