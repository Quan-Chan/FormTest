# Framework de Teste de Modelos de IA

> **警告 Warning**: 尚未完成正在优化前端随后重构后端及文件结构

Um framework de teste automatizado para avaliar a capacidade de Large Language Models (LLM) entenderem e analisarem formatos de dados estruturados.

## Visão Geral

Este projeto é projetado para avaliar e testar a capacidade de modelos de IA entenderem e analisarem arquivos de formatos de dados estruturados. Através de casos de teste predefinidos, ele chama automaticamente a API de IA e compara os resultados retornados com as respostas esperadas, quantificando assim o desempenho do modelo na compreensão de formatos.

## Estrutura do Projeto

```
草稿A/
├── 软件 de Teste/     # Aplicação principal (Backend Flask + Frontend HTML)
├── 软件 de Teste2/    # Variante de configuração (diferentes modelos/parâmetros)
├── 软件 de Teste3/
├── 软件 de Teste4/
├── Conjunto de Testes/ # Conjunto de dados de teste (não casos reais, gerado por IA)
│   ├── Arquivos de Teste/ # Arquivos de exemplo em vários formatos
│   │   ├── XML/
│   │   ├── JSON/
│   │   ├── YAML/
│   │   ├── Markdown/
│   │   ├── DSL/
│   │   └── Lista de Exemplos/
│   ├── Perguntas de Teste de Vídeo/
│   ├── Perguntas de Teste de Log/
│   ├── Perguntas de Teste Empresarial/
│   └── UI.json       # Configuração da interface de teste
├── Backup/           # Backups de formatos históricos
├── Log de Atualizações/ # Logs de correções de bugs
└── Descrição de Tarefas/ # Documentos de tarefas de desenvolvimento
```

## Formatos Suportados

- XML
- JSON
- YAML
- Markdown (incluindo tabelas, pares chave-valor)
- DSL (Linguagem Específica de Domínio)
- Listas de texto simples

## Principais Funcionalidades

1. **Teste Multi-formato**: Testa capacidades de parsing de vários formatos de dados simultaneamente
2. **Teste em Lote**: Executa casos de teste em lote com saída de streaming
3. **Suporte Multi-modelo**: Configura múltiplos modelos de IA para testes comparativos
4. **Cache de Respostas**: Evita chamadas API repetidas para acelerar testes iterativos
5. **System Prompt Personalizado**: Configura associações de teste via bindings.json
6. **Controle de Concorrência**: Concorrência e contagens de repetição configuráveis

## Início Rápido

### 1. Instalar Dependências

```bash
pip install -r 软件 de Teste/requirements.txt
```

### 2. Iniciar Serviço

```bash
cd 软件 de Teste
python app.py
# ou clique duas vezes em run.bat
```

### 3. Acessar Interface

Abra o navegador em http://localhost:5000

### 4. Configurar e Executar

1. Configure o endereço da API e parâmetros do modelo em Configurações
2. Selecione arquivos de formato e grupos de perguntas de teste
3. Clique em "Iniciar Teste"
4. Visualize o fluxo de resultados em tempo real e pontuações finais

## Configuração

| Parâmetro | Descrição | Padrão |
|------|------|--------|
| base_url | Endereço da API | http://192.168.1.45:1919/v1 |
| model | Nome do modelo | qwen3.5-0.8b |
| temperature | Temperatura | 0.7 |
| concurrency | Concorrência | 1 |
| test_count | Testes por pergunta | 1 |
| max_retries | Máx. repetições | 3 |

## Endpoints da API

| Endpoint | Método | Descrição |
|------|------|------|
| /api/v1/config | GET/POST | Gerenciamento de configuração |
| /api/v1/models | GET | Obter modelos disponíveis |
| /api/v1/ui-config | GET | Obter configuração da interface de teste |
| /api/v1/question-groups | GET | Obter grupos de perguntas |
| /api/v1/bindings | GET/POST | Configuração de associações |
| /api/v1/run-tests | POST | Executar testes (streaming SSE) |
| /api/v1/results | GET | Obter todos os resultados de testes |
| /api/v1/answer-cache | GET | Obter cache de respostas |

## Aviso Importante

### Declaração do Conjunto de Dados de Teste

**Todo o conteúdo no conjunto de dados de teste deste projeto são exemplos gerados por IA, não dados de casos reais.**

O conjunto de testes inclui:
- Exemplos de informações de vídeos tutoriais
- Exemplos de logs de operação
- Exemplos de informações empresariais
- Arquivos de exemplo em vários formatos (XML, JSON, YAML, Markdown, DSL)

Estes dados são usados exclusivamente para testar as capacidades de compreensão e análise de formatos estruturados dos modelos de IA, e não representam nenhum cenário de negócios real.

## Stack Tecnológico

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML + CSS + JavaScript vanilla
- **Chamadas de API**: requests (streaming SSE)
- **Execução de Testes**: Concorrência ThreadPoolExecutor

## Histórico de Versões

Veja `Log de Atualizações/changelog.json`

## Licença

Apache License 2.0 - Ver [LICENSE](LICENSE)

---

> **警告 Warning**: 尚未完成正在优化前端随后重构后端及文件结构