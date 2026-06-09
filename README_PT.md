# FormTest - Framework de Avaliação de Parsing de Formatos de IA

> **Todos os conjuntos de dados de teste são dados fictícios gerados por IA, não dados reais. Qualquer semelhança com a realidade é mera coincidência.**
>
> **Este projeto carece de planejamento adequado de construção e testes. A estrutura do código e a cobertura de testes não são completas. Apenas para fins de referência e aprendizado.**

Um framework de teste automatizado para avaliar a capacidade de Grandes Modelos de Linguagem (LLM) de entender e analisar formatos de dados estruturados.

## Estrutura do Projeto

```
FormTest/
├── 测试软件/              # Aplicação principal (Backend Flask + Frontend HTML)
│   ├── app.py            # Ponto de entrada Flask, API REST + SSE
│   ├── config.json       # Configuração de execução
│   ├── requirements.txt  # Dependências Python
│   ├── run.bat           # Script de início rápido
│   ├── static/           # Arquivos frontend
│   └── data/             # Dados de execução
├── 测试集/               # Dados de teste (gerados por IA, não reais)
│   ├── 教学视频测试/     # Teste de conteúdo de vídeo educacional
│   ├── 企业信息测试/     # Teste de informações empresariais
│   ├── 运行日志测试/     # Teste de logs de operação
│   └── Python进阶测试/   # Teste de Python avançado
├── .gitignore
├── LICENSE               # Apache License 2.0
└── README*.md            # README multilíngue
```

## Principais Funcionalidades

- **Comparação multi-formato** — Mesmo conteúdo em 8 formatos
- **Automação em lote** — Produto cartesiano de prompts × perguntas × modelos
- **Múltiplos modelos em paralelo** — Comparação horizontal
- **Streaming SSE em tempo real**
- **Testes múltiplos** — Repetição configurável por pergunta
- **Controle de concorrência**
- **Salvamento incremental**
- **Snapshots de arquivo**

## Início Rápido

```bash
pip install -r 测试软件/requirements.txt
cd 测试软件
python app.py
```

Abrir navegador: http://localhost:5000

## Aviso Importante

**Todos os conjuntos de dados de teste neste projeto são dados fictícios gerados por IA, não dados reais. Qualquer semelhança com entidades, organizações ou cenários reais é mera coincidência.** Estes dados são usados exclusivamente para avaliar a capacidade dos modelos de IA de compreender e analisar formatos estruturados.

## Licença

Apache License 2.0 — Ver [LICENSE](LICENSE)

---

**Isso pode ser algo escrito por uma IA bêbada. Meu objetivo principal é torturar a IA.**
