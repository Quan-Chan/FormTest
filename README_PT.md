# FormTest - Framework de Teste de Capacidade de Análise de Formato Estruturado para IA

> **Os conjuntos de teste incluídos são todos dados fictícios gerados por IA, não dados reais. Qualquer semelhança é mera coincidência.**
>
> **Este projeto não passou por construção e planejamento de testes adequados; a estrutura do código e a cobertura de testes ainda não são completas. É apenas para referência e aprendizado.**

Um framework de teste automatizado para avaliar a capacidade de modelos de linguagem de grande escala (LLM) de entender e analisar dados em formatos estruturados. Por meio de casos de teste predefinidos, ele chama automaticamente a API de IA, compara os resultados retornados com as respostas esperadas e quantifica o desempenho de compreensão de formato do modelo.

## Início Rápido

### 1. Instalar Dependências

```bash
pip install -r APPs/requirements.txt
```

### 2. Iniciar

```bash
cd APPs
python app.py
# Ou clique duas vezes em run.bat
```

Abra [http://localhost:5000](http://localhost:5000) no navegador

### 3. Configurar

Após iniciar, clique no botão **Configurações** no canto superior direito da interface web para configurar o endereço da API, modelo, parâmetros etc. Você também pode consultar `APPs/config.example.json` para criar um arquivo de configuração.

Principais itens de configuração:
- `base_url` — Endereço da API (suporta acréscimo automático de `/v1`)
- `model` — Nome do modelo padrão
- `model_thinking_config` — Configuração de modo de raciocínio/reflexão por modelo
- `streaming` — Alternância de saída SSE em stream
- `concurrency` — Número de threads simultâneas
- `disabled_params` — Parâmetros ocultos/desabilitados no frontend

### 4. Executar Testes

1. No **Canvas**, use o editor de nós para combinar: Prompt × Pergunta × Modelo
2. Clique em **Iniciar Teste** para ver os resultados em stream em tempo real
3. Após a conclusão, visualize/filtre os resultados em **Histórico de Resultados**

## Estrutura do Projeto

```
FormTest/
├── APPs/                          # Programa principal
│   ├── app.py                     # Backend Flask (API + mecanismo de execução de teste + SSE em stream)
│   ├── requirements.txt           # Dependências Python
│   ├── run.bat                    # Script de inicialização para Windows
│   ├── config.example.json        # Modelo de configuração
│   ├── flow.json                  # Definição do fluxograma
│   └── static/
│       └── index.html             # SPA frontend (HTML/CSS/JS nativos, ~7300 linhas)
├── Benches/                       # Conjuntos de dados de teste
│   ├── AI嘉豪测试/                # Perguntas de múltipla escolha sobre alfabetização em IA (adaptado de NAGI STUDIO)
│   ├── Python测试/                # Teste de conhecimento avançado em Python
│   ├── 企业信息测试/              # Informações empresariais fictícias
│   ├── 教学视频测试/              # Conteúdo de vídeo didático introdutório de Python
│   └── 运行日志测试/              # Análise de logs de operação de sistema
├── skills/                        # Scripts de ferramentas utilizáveis diretamente
│   ├── New-TestSet-新建测试集.ps1 # PowerShell para criar esqueleto de novo conjunto de teste
│   └── QA-Extract-问答提取.md     # Guia para extrair pares de QA de arquivos fonte
├── .opencode/
│   └── skills/                    # Skills opencode AI (para suporte a AI Agent)
│       ├── new-test-set/          # Criar esqueleto de conjunto de teste
│       └── qa-extract/            # Extrair pares de QA
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # Este arquivo
```

## Conjuntos de Teste

### Estrutura

Cada conjunto de teste usa o arquivo de marcação `.test-set-part` para identificar a função do subdiretório. O nome do diretório pode ser qualquer um; o sistema identifica pelo conteúdo do arquivo de marcação:

```
Benches/<nome>/
├── <diretório de perguntas>/      # Contém .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10 perguntas
│   └── 进阶问题.json              # 10 perguntas (alguns conjuntos têm apenas básicas)
├── <diretório de prompts>/        # Contém .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <nome>原版.json            # Formato narrativo em texto puro
│   ├── <nome>列表.json            # Formato de lista numerada
│   ├── <nome>JSON.json            # Formato estruturado JSON
│   ├── <nome>YAML.json            # Formato YAML
│   ├── <nome>XML.json             # Formato XML
│   ├── <nome>Markdown.json        # Formato de tabela Markdown
│   ├── <nome>MarkdownKV.json      # Formato de pares chave-valor Markdown
│   └── <nome>DSL.json             # Formato DSL personalizado
└── <diretório de resultados>/     # Contém .test-set-part → "results" (gerado em tempo de execução)
    └── .test-set-part
```

### Formatos de Teste

| Formato | Descrição |
|------|------|
| Original (Plain Text) | Texto narrativo puro, usado como referência base |
| Lista (List) | Lista numerada/com marcadores |
| JSON | Objeto JSON padrão |
| YAML | Dados estruturados YAML |
| XML | Representação hierárquica com tags XML |
| Markdown | Tabela Markdown |
| MarkdownKV | Pares chave-valor Markdown |
| DSL | Linguagem de domínio específico personalizada |

### Domínios de Teste

| Conjunto de Teste | Domínio de Conteúdo | Perguntas | Fonte |
|--------|----------|------|------|
| Teste de Vídeo Didático | Transcrição de palestra de programação Python | 20 | Fictício (IA) |
| Teste de Informações Empresariais | Informações empresariais fictícias | 20 | Fictício (IA) |
| Teste de Log de Operação | Entradas de log de operação de sistema | 20 | Fictício (IA) |
| Teste Python | Decoradores/gerenciadores de contexto/generators Python | 20 | Fictício (IA) |
| Teste de Alfabetização em IA | Perguntas de múltipla escolha sobre IA (básico/avançado/equívocos/humanidades) | 30 | Adaptado de [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## Funcionalidades Principais

- **Editor de Canvas Visual** — Canvas de nós SVG, combinação de prompt × pergunta × modelo por arrastar e soltar, suporte a desenho de linhas de conexão
- **Desfazer/Refazer** — Sistema completo de histórico, suporte a Ctrl+Z / Ctrl+Shift+Z
- **Teste de Comparação Multiformato** — Mesmo conteúdo apresentado em 8 formatos, avaliando a diferença de compreensão do modelo para cada formato
- **Teste Automatizado em Lote** — Combinação de produto cartesiano de prompt × pergunta × modelo, execução simultânea automática
- **Gerenciamento de Múltiplos Modelos** — Gerenciamento por popup de modelos, suporte a adicionar/remover/ordenar modelos extras
- **Configuração de Raciocínio** — Parâmetros thinking/reasoning_effort configuráveis independentemente por modelo
- **Alternância de Desabilitação de Parâmetros** — Cada parâmetro pode ser ativado/desativado individualmente via dot-toggle
- **Saída em Stream em Tempo Real** — Push de resultados em stream baseado em SSE, progresso do teste visível em tempo real
- **Visualização de Histórico** — Pesquisa e filtro de resultados históricos por status/modelo/texto
- **Arquivar/Restaurar** — Salvar/carregar snapshots de configuração de teste (incluindo estado do canvas + configuração de raciocínio do modelo)
- **Detecção de Modelo _notFound** — Canvas detecta automaticamente modelos indisponíveis e exibe aviso ⚠
- **Complemento Automático de /v1** — Interruptor que adiciona automaticamente `/v1` ao final do endereço da API
- **Tema Escuro/Claro** — Sistema completo de variáveis CSS para alternância de temas
- **Suporte a API Anthropic** — Suporte a formato de mensagem Anthropic + parsing de raciocínio SSE dedicado
- **Teste Múltiplo** — Uma única pergunta pode ser repetida várias vezes para medir a estabilidade da resposta
- **Controle de Concorrência** — Número de threads simultâneas e estratégia de repetição configuráveis
- **Salvamento Incremental** — Salvamento incremental periódico de resultados durante o teste para evitar perda acidental
- **Validação de Segurança de Caminho** — Prevenção contra ataques de travessia de caminho, verificação de nomes reservados do Windows, lista branca de nomes de arquivo

## Interface da API

| Endpoint | Método | Descrição |
|------|------|------|
| `/` | GET | Fornece o SPA frontend |
| `/api/v1/config` | GET/POST | Leitura/salvamento de configuração |
| `/api/v1/models` | GET/POST | Obter lista de modelos disponíveis/salvar lista de modelos |
| `/api/v1/test-set/scan` | GET | Escanear conjuntos de teste |
| `/api/v1/test-set/prompts` | GET | Obter prompts de sistema do conjunto de teste |
| `/api/v1/test-set/questions` | GET | Obter perguntas do conjunto de teste |
| `/api/v1/test-set/results` | GET | Obter resultados históricos de teste |
| `/api/v1/test-job/hub` | POST | Agendamento unificado de tarefas (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | Push de resultados em stream SSE em tempo real |
| `/api/v1/canvas-state` | GET/POST | Salvar/ler estado do canvas |
| `/api/v1/archives` | GET/POST/DELETE | Gerenciamento de arquivos |
| `/api/v1/tags` | GET | Obter todas as tags |

Resposta de erro: `404` → `{"error": "Not found"}`, `500` → `{"error": "Erro interno do servidor"}`

## Itens de Configuração

| Chave | Tipo | Descrição |
|-----|------|------|
| `api_key` | string | Chave da API |
| `base_url` | string | Endereço da API |
| `model` | string | Nome do modelo padrão |
| `models` | string[] | Lista de modelos extras |
| `temperature` | float | Temperatura (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | Tamanho do contexto |
| `concurrency` | int | Número de threads simultâneas (1-50) |
| `test_count` | int | Número de repetições de teste por pergunta |
| `max_retries` | int | Número máximo de tentativas |
| `streaming` | bool | Alternância de SSE em stream |
| `timeout` | int | Tempo limite de requisição em segundos |
| `model_thinking_config` | object | Configuração de raciocínio por modelo, ex: `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Forçar uso de formato de mensagem Anthropic |
| `force_openai_endpoint` | bool | Forçar uso de endpoint compatível com OpenAI |
| `disabled_params` | string[] | Lista de nomes de parâmetros ocultos/desabilitados no frontend |

## OpenCode Skills

Este projeto inclui duas skills de ferramentas para ajudar a criar e gerenciar rapidamente conjuntos de teste:

### Ferramentas do Usuário (`skills/`)

Scripts e documentos que podem ser executados diretamente por desenvolvedores:

| Arquivo | Descrição |
|------|------|
| `skills/New-TestSet-新建测试集.ps1` | Script PowerShell que cria automaticamente um esqueleto de conjunto de teste numerado com diretórios e arquivos de marcação .test-set-part |
| `skills/QA-Extract-问答提取.md` | Guia detalhado explicando como extrair pares de QA de arquivos fonte e gerar arquivos JSON compatíveis |

### Skills para AI Agent (`.opencode/skills/`)

Se você usa [opencode](https://opencode.ai) ou ferramentas de codificação de IA compatíveis, as skills em `.opencode/skills/` podem ser descobertas e carregadas automaticamente pelo AI Agent:

| Skill | Descrição |
|------|------|
| `new-test-set` | Orienta a IA a criar esqueleto de conjunto de teste (diretórios + arquivos de marcação), com numeração automática para evitar conflitos |
| `qa-extract` | Orienta a IA a extrair pares de QA de arquivos fonte e gerar JSON compatível com o formato de conjunto de teste do FormTest |

## Stack Tecnológica

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML / CSS nativos (sistema de variáveis personalizado, tema claro/escuro) / JavaScript
- **Chamadas de IA**: Biblioteca `requests` (suporta SSE em stream e modo JSON comum, compatível com OpenAI / Anthropic API)
- **Concorrência**: Pool de threads `ThreadPoolExecutor` + retry com backoff exponencial
- **Saída**: Server-Sent Events (`text/event-stream`)

## Aviso Importante

**O conteúdo dos conjuntos de teste deste projeto são todos dados de exemplo fictícios gerados por IA, não dados reais. Qualquer semelhança é mera coincidência.** Todos os dados são usados exclusivamente para avaliar a capacidade de modelos de IA de entender e analisar formatos estruturados, não representando nenhum cenário de negócios real ou entidade.

- `Benches/AI嘉豪测试/` é adaptado do [Teste de Alfabetização em IA do NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao), distribuído sob licença MIT
- Os demais conjuntos de teste são todos dados fictícios gerados por IA

## Licença

Apache License 2.0 — Consulte o arquivo [LICENSE](LICENSE) para detalhes

---

**Isso pode ser algo que a IA escreveu depois de beber bebida alcoólica falsificada — meu objetivo principal é torturar a IA.**
