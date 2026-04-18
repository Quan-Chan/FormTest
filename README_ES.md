# Framework de Pruebas de Modelos de IA

Un marco de pruebas automatizado para evaluar la capacidad de los Modelos de Lenguaje Grande (LLM) para entender y analizar formatos de datos estructurados.

## Descripción general

Este proyecto está diseñado para evaluar y probar la capacidad de los modelos de IA para entender y analizar archivos de formatos de datos estructurados. A través de casos de prueba preestablecidos, llama automáticamente a la API de IA y compara los resultados devueltos con las respuestas esperadas, cuantificando así el rendimiento del modelo en la comprensión de formatos.

## Estructura del proyecto

```
草稿A/
├── 测试软件/           # Aplicación principal (Backend Flask + Frontend HTML)
├── 测试软件2/         # Variante de configuración (diferentes modelos/parámetros)
├── 测试软件3/
├── 测试软件4/
├── 测试集/           # Conjunto de datos de prueba (no casos reales, generado por IA)
│   ├── 被测试文件/    # Archivos de ejemplo en varios formatos
│   │   ├── XML/
│   │   ├── JSON/
│   │   ├── YAML/
│   │   ├── Markdown/
│   │   ├── DSL/
│   │   └── 列表示例/
│   ├── 教学视频测试问题/
│   ├── 运行日志测试问题/
│   ├── 企业信息测试问题/
│   └── UI.json       # Configuración de interfaz de prueba
├── 备份/             # Copias de seguridad de formatos históricos
├── 更新日志/         # Registros de correcciones de errores
└── 任务说明/         # Documentos de tareas de desarrollo
```

## Formatos compatibles

- XML
- JSON
- YAML
- Markdown (incluyendo tablas, pares clave-valor)
- DSL (Lenguaje Específico del Dominio)
- Listas de texto plano

## Características principales

1. **Pruebas multiformato**: Prueba las capacidades de análisis de múltiples formatos de datos simultáneamente
2. **Pruebas por lotes**: Ejecuta casos de prueba en lotes con salida de streaming
3. **Soporte múltiples modelos**: Configura múltiples modelos de IA para pruebas comparativas
4. **Caché de respuestas**: Evita llamadas API repetidas para acelerar pruebas iterativas
5. **System Prompt personalizado**: Configura asociaciones de prueba a través de bindings.json
6. **Control de concurrencia**: Concurrencia y recuentos de reintento configurables

## Inicio rápido

### 1. Instalar dependencias

```bash
pip install -r 测试软件/requirements.txt
```

### 2. Iniciar servicio

```bash
cd 测试软件
python app.py
# o hacer doble clic en run.bat
```

### 3. Acceder a la interfaz

Abre el navegador en http://localhost:5000

### 4. Configurar y ejecutar

1. Configura la dirección de la API y los parámetros del modelo en Configuración
2. Selecciona los archivos de formato y grupos de preguntas de prueba
3. Haz clic en "Iniciar prueba"
4. Ver el flujo de resultados en tiempo real y puntuaciones finales

## Configuración

| Parámetro | Descripción | Valor predeterminado |
|------|------|--------|
| base_url | Dirección de API | http://192.168.1.45:1919/v1 |
| model | Nombre del modelo | qwen3.5-0.8b |
| temperature | Temperatura | 0.7 |
| concurrency | Concurrencia | 1 |
| test_count | Pruebas por pregunta | 1 |
| max_retries | Máx. reintentos | 3 |

## Endpoints de API

| Endpoint | Método | Descripción |
|------|------|------|
| /api/v1/config | GET/POST | Gestión de configuración |
| /api/v1/models | GET | Obtener modelos disponibles |
| /api/v1/ui-config | GET | Obtener configuración de interfaz de prueba |
| /api/v1/question-groups | GET | Obtener grupos de preguntas |
| /api/v1/bindings | GET/POST | Configuración de enlaces |
| /api/v1/run-tests | POST | Ejecutar pruebas (streaming SSE) |
| /api/v1/results | GET | Obtener todos los resultados de pruebas |
| /api/v1/answer-cache | GET | Obtener caché de respuestas |

## Aviso importante

### Declaración del conjunto de datos de prueba

**Todo el contenido en el conjunto de datos de prueba de este proyecto son ejemplos generados por IA, no datos de casos reales.**

El conjunto de datos de prueba incluye:
- Ejemplos de información de videos教程
- Ejemplos de registros de operación
- Ejemplos de información empresarial
- Archivos de ejemplo en varios formatos (XML, JSON, YAML, Markdown, DSL)

Estos datos se utilizan únicamente para probar las capacidades de comprensión y análisis de formatos estructurados de los modelos de IA, y no representan ningún escenario empresarial real.

## Pila tecnológica

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML + CSS + JavaScript vanilla
- **Llamadas API**: requests (streaming SSE)
- **Ejecución de pruebas**: Concurrencia ThreadPoolExecutor

## Historial de versiones

Ver `更新日志/changelog.json`

## Licencia

MIT