# FormTest - Framework de Evaluación de Capacidad de Análisis de Formatos Estructurados para IA

> **Todos los conjuntos de prueba incluidos son datos ficticios generados por IA, no datos reales. Cualquier parecido con la realidad es mera coincidencia.**
>
> **Este proyecto no ha pasado por una construcción y planificación de pruebas exhaustivas. La estructura del código y la cobertura de pruebas son incompletas y se proporcionan solo con fines de referencia y aprendizaje.**

Un framework de pruebas automatizadas para evaluar la capacidad de los Modelos de Lenguaje de Gran Escala (LLM) para comprender y analizar formatos de datos estructurados. Mediante casos de prueba predefinidos, invoca automáticamente la API de IA y compara los resultados devueltos con las respuestas esperadas para cuantificar el rendimiento de comprensión de formato del modelo.

## Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r APPs/requirements.txt
```

### 2. Iniciar

```bash
cd APPs
python app.py
# O haga doble clic en run.bat
```

Abra [http://localhost:5000](http://localhost:5000) en su navegador.

### 3. Configuración

Después de iniciar, haga clic en el botón **Ajustes** en la esquina superior derecha de la interfaz web para configurar la dirección de la API, el modelo, los parámetros, etc. También puede consultar `APPs/config.example.json` para crear un archivo de configuración.

Elementos de configuración principales:
- `base_url` — Dirección de la API (admite el añadido automático de `/v1`)
- `model` — Nombre del modelo predeterminado
- `model_thinking_config` — Configurar el modo de razonamiento/pensamiento por modelo
- `streaming` — Interruptor de transmisión SSE
- `concurrency` — Número de hilos simultáneos
- `disabled_params` — Parámetros ocultos/deshabilitados en el frontend

### 4. Ejecutar Pruebas

1. En el **Lienzo**, use el editor de nodos para combinar: Prompt × Pregunta × Modelo
2. Haga clic en **Iniciar Prueba** para ver los resultados de transmisión en tiempo real
3. Después de la prueba, puede ver/filtrar los resultados en **Historial de Resultados**

## Estructura del Proyecto

```
FormTest/
├── APPs/                          # Aplicación principal
│   ├── app.py                     # Backend Flask (API + motor de ejecución de pruebas + transmisión SSE)
│   ├── requirements.txt           # Dependencias de Python
│   ├── run.bat                    # Script de inicio para Windows
│   ├── config.example.json        # Plantilla de configuración
│   ├── flow.json                  # Definición del diagrama de flujo
│   └── static/
│       └── index.html             # SPA frontend (HTML/CSS/JS puro, ~7300 líneas)
├── Benches/                       # Conjuntos de datos de prueba
│   ├── AI嘉豪测试/                # Prueba de opción múltiple de alfabetización en IA (adaptado de NAGI STUDIO)
│   ├── Python测试/                # Prueba de conocimientos avanzados de Python
│   ├── 企业信息测试/              # Información ficticia de registro de empresas
│   ├── 教学视频测试/              # Contenido de video tutorial de Python para principiantes
│   └── 运行日志测试/              # Análisis de registros de operaciones del sistema
├── skills/                        # Scripts de herramientas para uso directo del usuario
│   ├── New-TestSet-新建测试集.ps1 # Script de PowerShell para crear un nuevo esqueleto de conjunto de prueba
│   └── QA-Extract-问答提取.md     # Guía para extraer pares de preguntas y respuestas de archivos fuente
├── .opencode/
│   └── skills/                    # Habilidades de IA de opencode (para soporte de Agente de IA)
│       ├── new-test-set/          # Crear esqueleto de conjunto de prueba
│       └── qa-extract/            # Extracción de pares de preguntas y respuestas
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # Este archivo
```

## Conjuntos de Prueba

### Estructura

Cada conjunto de prueba utiliza archivos marcadores `.test-set-part` para identificar los roles de los subdirectorios. Los nombres de los directorios pueden ser arbitrarios; el sistema identifica los roles a través del contenido del archivo marcador:

```
Benches/<nombre>/
├── <directorio de preguntas>/     # Contiene .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10 preguntas
│   └── 进阶问题.json              # 10 preguntas (algunos conjuntos solo tienen básicas)
├── <directorio de prompts>/       # Contiene .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <nombre>原版.json          # Formato narrativo en texto plano
│   ├── <nombre>列表.json          # Formato de lista numerada
│   ├── <nombre>JSON.json          # Formato estructurado JSON
│   ├── <nombre>YAML.json          # Formato YAML
│   ├── <nombre>XML.json           # Formato XML
│   ├── <nombre>Markdown.json      # Formato de tabla Markdown
│   ├── <nombre>MarkdownKV.json    # Formato de pares clave-valor Markdown
│   └── <nombre>DSL.json           # Formato DSL personalizado
└── <directorio de resultados>/    # Contiene .test-set-part → "results" (generado en tiempo de ejecución)
    └── .test-set-part
```

### Formatos de Prueba

| Formato | Descripción |
|---------|-------------|
| Original (Plain Text) | Texto plano narrativo, usado como línea base |
| Lista (List) | Lista numerada/con viñetas |
| JSON | Objeto JSON estándar |
| YAML | Datos estructurados YAML |
| XML | Jerarquía de etiquetas XML |
| Markdown | Tabla Markdown |
| MarkdownKV | Pares clave-valor Markdown |
| DSL | Lenguaje de dominio específico personalizado |

### Dominios de Prueba

| Conjunto de Prueba | Dominio de Contenido | Cantidad | Fuente |
|--------------------|----------------------|----------|--------|
| 教学视频测试 | Transcripción de conferencia de programación Python | 20 | Ficticio IA |
| 企业信息测试 | Información ficticia de registro de empresas | 20 | Ficticio IA |
| 运行日志测试 | Entradas de registro de operaciones del sistema | 20 | Ficticio IA |
| Python测试 | Decoradores/generadores/administradores de contexto de Python | 20 | Ficticio IA |
| AI嘉豪测试 | Opción múltiple de alfabetización en IA (básico/avanzado/ideas erróneas/humanidades) | 30 | Adaptado de [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## Funcionalidades Principales

- **Editor de Lienzo Visual** — Lienzo de nodos SVG, combinación de Prompt × Pregunta × Modelo mediante arrastrar y soltar, con dibujo de líneas de conexión
- **Deshacer/Rehacer** — Sistema de historial completo compatible con Ctrl+Z / Ctrl+Mayús+Z
- **Pruebas Comparativas Multi-Formato** — Mismo contenido presentado en 8 formatos para evaluar las diferencias de comprensión de formato del modelo
- **Pruebas Automatizadas por Lotes** — Combinaciones de producto cartesiano de Prompt × Pregunta × Modelo, ejecutadas automáticamente en paralelo
- **Gestión Multi-Modelo** — Gestión emergente de modelos que permite añadir/eliminar/ordenar modelos adicionales
- **Configuración de Razonamiento** — Configuración independiente por modelo de los parámetros thinking/reasoning_effort
- **Alternancia de Parámetros** — Cada parámetro se puede habilitar/deshabilitar de forma independiente mediante un interruptor de punto
- **Salida en Tiempo Real por Transmisión** — Push de resultados de transmisión basado en SSE, visibilidad del progreso de la prueba en tiempo real
- **Visor de Historial de Resultados** — Filtrar resultados históricos por estado/modelo/búsqueda de texto
- **Archivar/Restaurar** — Guardar/cargar instantáneas de configuración de prueba (incluyendo estado del lienzo + configuración de razonamiento del modelo)
- **Detección de Modelo _notFound** — El lienzo detecta automáticamente modelos no disponibles y muestra una advertencia ⚠
- **Completado Automático de /v1** — Interruptor para añadir automáticamente `/v1` a la dirección de la API
- **Tema Oscuro/Claro** — Sistema completo de variables CSS para cambio de tema
- **Soporte de API Anthropic** — Compatible con el formato de mensajes de Anthropic + análisis de razonamiento SSE dedicado
- **Pruebas Multi-Ronda** — Una sola pregunta se puede repetir varias veces para medir la estabilidad de la respuesta
- **Control de Concurrencia** — Número configurable de hilos simultáneos y estrategia de reintento
- **Guardado Incremental** — Guarda resultados periódicamente durante la prueba para evitar la pérdida accidental de datos
- **Validación de Seguridad de Rutas** — Previene ataques de path traversal, comprobación de nombres reservados de Windows, lista blanca de nombres de archivo

## Endpoints de la API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Sirve el SPA del frontend |
| `/api/v1/config` | GET/POST | Leer/guardar configuración |
| `/api/v1/models` | GET/POST | Obtener lista de modelos disponibles/guardar lista de modelos |
| `/api/v1/test-set/scan` | GET | Escanear conjuntos de prueba |
| `/api/v1/test-set/prompts` | GET | Obtener prompts del sistema de los conjuntos de prueba |
| `/api/v1/test-set/questions` | GET | Obtener preguntas del conjunto de prueba |
| `/api/v1/test-set/results` | GET | Obtener resultados históricos de pruebas |
| `/api/v1/test-job/hub` | POST | Despacho unificado de tareas (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | Push de resultados en tiempo real por transmisión SSE |
| `/api/v1/canvas-state` | GET/POST | Guardar/leer estado del lienzo |
| `/api/v1/archives` | GET/POST/DELETE | Gestión de archivos |
| `/api/v1/tags` | GET | Obtener todas las etiquetas |

Respuestas de error: `404` → `{"error": "Not found"}`, `500` → `{"error": "Error interno del servidor"}`

## Opciones de Configuración

| Clave | Tipo | Descripción |
|-------|------|-------------|
| `api_key` | string | Clave de la API |
| `base_url` | string | Dirección de la API |
| `model` | string | Nombre del modelo predeterminado |
| `models` | string[] | Lista de modelos adicionales |
| `temperature` | float | Temperatura (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | Tamaño de contexto |
| `concurrency` | int | Número de hilos simultáneos (1-50) |
| `test_count` | int | Número de repeticiones de prueba por pregunta |
| `max_retries` | int | Número máximo de reintentos |
| `streaming` | bool | Interruptor de transmisión SSE |
| `timeout` | int | Tiempo de espera de solicitud en segundos |
| `model_thinking_config` | object | Configuración de razonamiento por modelo, ej. `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Forzar uso del formato de mensajes de Anthropic |
| `force_openai_endpoint` | bool | Forzar uso de endpoint compatible con OpenAI |
| `disabled_params` | string[] | Lista de parámetros ocultos/deshabilitados en el frontend |

## Habilidades de OpenCode

Este proyecto incluye dos habilidades de herramientas que ayudan a crear y gestionar conjuntos de prueba rápidamente:

### Herramientas de Usuario (`skills/`)

Scripts y documentación que los desarrolladores pueden ejecutar directamente:

| Archivo | Descripción |
|---------|-------------|
| `skills/New-TestSet-新建测试集.ps1` | Script de PowerShell que crea automáticamente un esqueleto de conjunto de prueba numerado y archivos marcadores `.test-set-part` |
| `skills/QA-Extract-问答提取.md` | Guía detallada sobre cómo extraer pares de preguntas y respuestas de archivos fuente y generar archivos JSON compatibles |

### Habilidades de Agente de IA (`.opencode/skills/`)

Si usa [opencode](https://opencode.ai) o una herramienta de codificación de IA compatible, las habilidades en `.opencode/skills/` pueden ser descubiertas y cargadas automáticamente por el Agente de IA:

| Habilidad | Descripción |
|-----------|-------------|
| `new-test-set` | Guía a la IA para crear un esqueleto de conjunto de prueba (directorios + archivos marcadores), soporta numeración automática para evitar conflictos |
| `qa-extract` | Guía a la IA para extraer pares de preguntas y respuestas de archivos fuente, generando JSON compatible con el formato de conjunto de prueba de FormTest |

## Stack Tecnológico

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML / CSS puro (sistema de variables personalizado, temas oscuro/claro) / JavaScript
- **Llamadas a la IA**: Librería `requests` (soporta tanto modo de transmisión SSE como JSON normal, compatible con API de OpenAI / Anthropic)
- **Concurrencia**: Grupo de hilos `ThreadPoolExecutor` + reintento con backoff exponencial
- **Salida**: Server-Sent Events (`text/event-stream`)

## Aviso Importante

**El contenido de los conjuntos de prueba en este proyecto consiste completamente en datos de ejemplo ficticios generados por IA, no en datos reales. Cualquier parecido con la realidad es mera coincidencia.** Todos los datos se utilizan únicamente para evaluar la capacidad de los modelos de IA para comprender y analizar formatos estructurados y no representan ningún escenario empresarial o entidad real.

- `Benches/AI嘉豪测试/` está adaptado de [NAGI STUDIO's AI Jiahao Test](https://github.com/nagi-studio/ai-jiahao), publicado bajo la licencia MIT
- Todos los demás conjuntos de prueba son datos ficticios generados por IA

## Licencia

Apache License 2.0 — consulte el archivo [LICENSE](LICENSE) para más detalles

---

**Esto podría ser algo que una IA escribió borracha con alcohol adulterado — mi trabajo principal es interrogar a la IA.**
