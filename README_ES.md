# FormTest - Framework de Evaluación de Parseo de Formatos de IA

> **Todos los conjuntos de datos de prueba son datos ficticios generados por IA, no datos reales. Cualquier parecido con la realidad es pura coincidencia.**
>
> **Este proyecto carece de una planificación adecuada de construcción y pruebas. La estructura del código y la cobertura de pruebas no son completas. Solo para fines de referencia y aprendizaje.**

Un framework de pruebas automatizado para evaluar la capacidad de los Modelos de Lenguaje Grande (LLM) para entender y analizar formatos de datos estructurados.

## Estructura del Proyecto

```
FormTest/
├── APPs/              # Aplicación principal (Backend Flask + Frontend HTML)
│   ├── app.py            # Punto de entrada Flask, API REST + SSE
│   ├── config.json       # Configuración de ejecución
│   ├── requirements.txt  # Dependencias Python
│   ├── run.bat           # Script de inicio rápido
│   ├── static/           # Archivos frontend (index.html + CSS/JS)
│   └── data/             # Datos de ejecución
├── Benches/               # Datos de prueba (generados por IA, no reales)
│   ├── 教学视频测试/     # Prueba de contenido de video educativo
│   ├── 企业信息测试/     # Prueba de información empresarial
│   ├── 运行日志测试/     # Prueba de registros de operación
│   └── Python进阶测试/   # Prueba de Python avanzado
├── .gitignore
├── LICENSE               # Apache License 2.0
└── README*.md            # README multilingüe
```

## Estructura del Conjunto de Pruebas

```
Benches/<nombre>/
├── 测试问题/             # Preguntas de prueba (JSON)
│   ├── 基础问题.json     # Preguntas básicas
│   └── 进阶问题.json     # Preguntas avanzadas
├── 测试系统提示词/       # Mismo contenido en múltiples formatos
│   ├── <nombre>原版.txt  #   Texto plano
│   ├── <nombre>列表.txt  #   Lista numerada
│   ├── <nombre>JSON.txt  #   JSON
│   ├── <nombre>YAML.txt  #   YAML
│   ├── <nombre>XML.txt   #   XML
│   ├── <nombre>Markdown.txt    # Markdown tabla
│   ├── <nombre>MarkdownKV.txt  # Markdown clave-valor
│   ├── <nombre>DSL.txt   #   DSL
│   └── Metadatos .json
└── 测试结果/             # Resultados (auto-generados)
```

## Funciones Principales

- **Comparación multi-formato** — Mismo contenido en 8 formatos
- **Automatización por lotes** — Producto cartesiano de prompts × preguntas × modelos
- **Modelos múltiples en paralelo** — Comparación horizontal de modelos
- **Streaming SSE en tiempo real**
- **Pruebas múltiples** — Repetición configurable por pregunta
- **Control de concurrencia**
- **Guardado incremental**
- **Snapshots de archivo**

## Inicio Rápido

```bash
pip install -r APPs/requirements.txt
cd 测试软件
python app.py
```

Abrir navegador: http://localhost:5000

Después de iniciar, haga clic en "Configuración" en la esquina superior derecha de la interfaz web para configurar la API, el modelo y los parámetros.

## Endpoints de API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/config` | GET/POST | Gestión de configuración |
| `/api/v1/models` | GET | Listar modelos |
| `/api/v1/test-set/scan` | GET | Escanear conjuntos |
| `/api/v1/test-set/prompts` | GET | Obtener prompts |
| `/api/v1/test-set/questions` | GET | Obtener preguntas |
| `/api/v1/test-set/results` | GET | Obtener resultados |
| `/api/v1/run-tests` | POST | Ejecutar pruebas (SSE) |
| `/api/v1/stop-tests` | POST | Detener pruebas |
| `/api/v1/canvas-state` | GET/POST | Estado del canvas |
| `/api/v1/archives` | GET/POST/DELETE | Gestión de archivos |
| `/api/v1/tags` | GET | Obtener etiquetas |

## Stack Tecnológico

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML / CSS / JavaScript vanilla
- **Llamadas API**: `requests` (SSE + JSON)
- **Concurrencia**: `ThreadPoolExecutor`
- **Salida**: Server-Sent Events

## Aviso Importante

**Todos los conjuntos de datos de prueba en este proyecto son datos ficticios generados por IA, no datos reales. Cualquier parecido con entidades, organizaciones o escenarios reales es pura coincidencia.** Estos datos se utilizan únicamente para evaluar la capacidad de los modelos de IA para comprender y analizar formatos estructurados.

## Licencia

Apache License 2.0 — Ver [LICENSE](LICENSE)

---

**Esto podría ser algo escrito por una IA borracha. Mi objetivo principal es torturar a la IA.**
