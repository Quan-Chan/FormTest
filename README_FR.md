# FormTest - Cadre de test de capacité d'analyse de formats structurés pour l'IA

> **Les ensembles de tests fournis sont des données fictives générées par l'IA, et non des données réelles. Toute ressemblance avec des faits réels serait purement fortuite.**
>
> **Ce projet n'a pas fait l'objet d'une planification et d'une construction programmatique approfondies. La structure du code et la couverture des tests sont encore incomplètes. Il est fourni à titre de référence et d'apprentissage uniquement.**

Un cadre de test automatisé pour évaluer la capacité des grands modèles de langage (LLM) à comprendre et analyser des formats de données structurées. Grâce à des cas de test prédéfinis, il appelle automatiquement l'API IA, compare les résultats renvoyés avec les réponses attendues et quantifie les performances de compréhension des formats du modèle.

## Démarrage rapide

### 1. Installer les dépendances

```bash
pip install -r APPs/requirements.txt
```

### 2. Lancer

```bash
cd APPs
python app.py
# ou double-cliquez sur run.bat
```

Ouvrir le navigateur sur [http://localhost:5000](http://localhost:5000)

### 3. Configuration

Après le démarrage, cliquez sur le bouton **Paramètres** dans le coin supérieur droit de l'interface web pour configurer l'URL de l'API, le modèle, les paramètres, etc. Vous pouvez également vous référer à `APPs/config.example.json` pour créer un fichier de configuration.

Principaux éléments de configuration :
- `base_url` — URL de l'API (support de l'ajout automatique de `/v1`)
- `model` — Nom du modèle par défaut
- `model_thinking_config` — Configuration du mode de réflexion par modèle
- `streaming` — Activation/désactivation du flux SSE
- `concurrency` — Nombre de threads concurrents
- `disabled_params` — Paramètres masqués/désactivés dans l'interface

### 4. Exécuter les tests

1. Sur le **canevas**, utilisez l'éditeur de nœuds pour combiner : invite × question × modèle
2. Cliquez sur **Démarrer le test** pour visualiser les résultats en flux continu en temps réel
3. Une fois le test terminé, vous pouvez consulter/filtrer les résultats dans **Historique des résultats**

## Structure du projet

```
FormTest/
├── APPs/                          # Programme principal
│   ├── app.py                     # Backend Flask (API + moteur d'exécution de tests + flux SSE)
│   ├── requirements.txt           # Dépendances Python
│   ├── run.bat                    # Script de démarrage Windows
│   ├── config.example.json        # Modèle de configuration
│   ├── flow.json                  # Définition du diagramme de flux
│   └── static/
│       └── index.html             # SPA frontend (HTML/CSS/JS natif, ~7300 lignes)
├── Benches/                       # Ensembles de données de test
│   ├── AI嘉豪测试/                # Questions de culture IA (adapté de NAGI STUDIO)
│   ├── Python测试/                # Test de connaissances avancées Python
│   ├── 企业信息测试/              # Informations d'entreprises fictives
│   ├── 教学视频测试/              # Contenu de vidéos pédagogiques Python
│   └── 运行日志测试/              # Analyse de journaux d'exploitation système
├── skills/                        # Scripts d'outils utilisables directement
│   ├── New-TestSet-新建测试集.ps1 # Script PowerShell pour créer une nouvelle structure de test
│   └── QA-Extract-问答提取.md     # Guide d'extraction de paires Q/R à partir de fichiers sources
├── .opencode/
│   └── skills/                    # Compétences opencode AI (pour support Agent IA)
│       ├── new-test-set/          # Création de structure de test
│       └── qa-extract/            # Extraction de paires Q/R
├── .gitignore
├── LICENSE                        # Licence Apache 2.0
└── README.md                      # Ce fichier
```

## Ensembles de tests

### Structure

Chaque ensemble de tests utilise un fichier marqueur `.test-set-part` pour identifier le rôle des sous-répertoires. Le nom du répertoire est arbitraire ; le système identifie le rôle via le contenu du fichier marqueur :

```
Benches/<nom>/
├── <répertoire questions>/         # Contient .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json               # 10 questions
│   └── 进阶问题.json               # 10 questions (certains ensembles n'ont que les questions de base)
├── <répertoire prompts>/           # Contient .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <nom>原版.json              # Format texte narratif pur
│   ├── <nom>列表.json              # Format liste numérotée
│   ├── <nom>JSON.json              # Format structuré JSON
│   ├── <nom>YAML.json              # Format YAML
│   ├── <nom>XML.json               # Format XML
│   ├── <nom>Markdown.json          # Format tableau Markdown
│   ├── <nom>MarkdownKV.json        # Format paires clé-valeur Markdown
│   └── <nom>DSL.json               # Format DSL personnalisé
└── <répertoire résultats>/         # Contient .test-set-part → "results" (généré à l'exécution)
    └── .test-set-part
```

### Formats de test

| Format | Description |
|------|------|
| Texte brut (Plain Text) | Texte narratif pur, utilisé comme référence |
| Liste (List) | Liste numérotée / à puces |
| JSON | Objet JSON standard |
| YAML | Données structurées YAML |
| XML | Représentation hiérarchique XML |
| Markdown | Tableau Markdown |
| MarkdownKV | Paires clé-valeur Markdown |
| DSL | Langage spécifique au domaine personnalisé |

### Domaines de test

| Ensemble de tests | Domaine | Nb. de questions | Source |
|--------|----------|------|------|
| Enseignement vidéo | Transcription de cours Python | 20 | Fiction IA |
| Informations entreprises | Informations d'entreprises fictives | 20 | Fiction IA |
| Journaux d'exploitation | Entrées de journaux système | 20 | Fiction IA |
| Test Python | Décorateurs/générateurs/gestionnaires de contexte Python | 20 | Fiction IA |
| Culture IA | QCM culture IA (base/avancé/idées reçues/humain) | 30 | Adapté de [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## Fonctionnalités principales

- **Éditeur visuel sur canevas** — Canevas de nœuds SVG, combinaison par glisser-déposer invite × question × modèle, tracé de lignes de connexion
- **Annuler/Rétablir** — Système d'historique complet, support Ctrl+Z / Ctrl+Maj+Z
- **Test comparatif multi-format** — Même contenu présenté en 8 formats, évaluation des différences de compréhension du modèle pour chaque format
- **Test automatisé par lots** — Combinaison produit cartésien invite × question × modèle, exécution concurrente automatique
- **Gestion multi-modèle** — Gestion par fenêtre modale, ajout/suppression/tri de modèles supplémentaires
- **Configuration du raisonnement** — Paramètres thinking/reasoning_effort configurables indépendamment par modèle
- **Activation/désactivation des paramètres** — Chaque paramètre peut être activé/désactivé individuellement via dot-toggle
- **Sortie en temps réel en flux continu** — Diffusion des résultats via SSE, progression visible en temps réel
- **Consultation de l'historique** — Recherche/filtrage des résultats historiques par statut/modèle/texte
- **Archivage/Restauration** — Sauvegarde/chargement d'instantanés de configuration de test (état du canevas + configuration de raisonnement des modèles)
- **Détection de modèles _notFound** — Détection automatique des modèles indisponibles sur le canevas avec avertissement ⚠
- **Complément automatique /v1** — Interrupteur pour ajouter automatiquement `/v1` à l'URL de l'API
- **Thème sombre/clair** — Système complet de variables CSS pour le changement de thème
- **Support API Anthropic** — Support du format de message Anthropic + analyse SSE dédiée
- **Tests multiples** — Une même question peut être répétée plusieurs fois pour mesurer la stabilité des réponses
- **Contrôle de la concurrence** — Nombre de threads concurrents et stratégie de réessai configurables
- **Sauvegarde incrémentale** — Sauvegarde incrémentale périodique des résultats pendant les tests pour éviter les pertes accidentelles
- **Validation de sécurité des chemins** — Prévention des attaques de traversée de chemin, vérification des noms réservés Windows, liste blanche des noms de fichiers

## API

| Point d'accès | Méthode | Description |
|------|------|------|
| `/` | GET | Fournit le SPA frontend |
| `/api/v1/config` | GET/POST | Lecture/sauvegarde de la configuration |
| `/api/v1/models` | GET/POST | Obtention de la liste des modèles disponibles/sauvegarde de la liste |
| `/api/v1/test-set/scan` | GET | Analyse des ensembles de tests |
| `/api/v1/test-set/prompts` | GET | Obtention des invites système de l'ensemble de tests |
| `/api/v1/test-set/questions` | GET | Obtention des questions de l'ensemble de tests |
| `/api/v1/test-set/results` | GET | Obtention des résultats de test historiques |
| `/api/v1/test-job/hub` | POST | Ordonnancement unifié des tâches (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | Diffusion SSE des résultats en temps réel |
| `/api/v1/canvas-state` | GET/POST | Sauvegarde/lecture de l'état du canevas |
| `/api/v1/archives` | GET/POST/DELETE | Gestion des archives |
| `/api/v1/tags` | GET | Obtention de tous les tags |

Réponses d'erreur : `404` → `{"error": "Not found"}`, `500` → `{"error": "服务器内部错误"}`

## Éléments de configuration

| Clé | Type | Description |
|-----|------|------|
| `api_key` | string | Clé API |
| `base_url` | string | URL de l'API |
| `model` | string | Nom du modèle par défaut |
| `models` | string[] | Liste de modèles supplémentaires |
| `temperature` | float | Température (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | Taille du contexte |
| `concurrency` | int | Nombre de threads concurrents (1-50) |
| `test_count` | int | Nombre de répétitions par question |
| `max_retries` | int | Nombre maximum de tentatives |
| `streaming` | bool | Activation/désactivation du flux SSE |
| `timeout` | int | Délai d'attente de la requête en secondes |
| `model_thinking_config` | object | Configuration du raisonnement par modèle, ex. `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Forcer l'utilisation du format de message Anthropic |
| `force_openai_endpoint` | bool | Forcer l'utilisation d'un point d'accès compatible OpenAI |
| `disabled_params` | string[] | Liste des noms de paramètres masqués/désactivés dans l'interface |

## Compétences OpenCode

Ce projet comprend deux compétences d'outils pour créer et gérer rapidement des ensembles de tests :

### Outils utilisateur (`skills/`)

Scripts et documents exécutables directement par les développeurs :

| Fichier | Description |
|------|------|
| `skills/New-TestSet-新建测试集.ps1` | Script PowerShell créant automatiquement la structure de répertoire d'un ensemble de tests avec numérotation et fichiers marqueurs .test-set-part |
| `skills/QA-Extract-问答提取.md` | Guide détaillé expliquant comment extraire des paires Q/R de fichiers sources et générer des fichiers JSON compatibles |

### Compétences Agent IA (`.opencode/skills/`)

Si vous utilisez [opencode](https://opencode.ai) ou un outil de codage IA compatible, les compétences dans `.opencode/skills/` peuvent être automatiquement découvertes et chargées par l'Agent IA :

| Compétence | Description |
|------|------|
| `new-test-set` | Guide l'IA pour créer la structure d'un ensemble de tests (répertoires + fichiers marqueurs), avec numérotation automatique pour éviter les conflits |
| `qa-extract` | Guide l'IA pour extraire des paires Q/R de fichiers sources, au format JSON compatible avec les ensembles de tests FormTest |

## Stack technique

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML / CSS natif (système de variables personnalisées, thèmes sombre/clair) / JavaScript
- **Appel IA**: Bibliothèque `requests` (support des deux modes : flux SSE et JSON standard, compatible API OpenAI / Anthropic)
- **Concurrence**: `ThreadPoolExecutor` + backoff exponentiel pour les tentatives
- **Sortie**: Server-Sent Events (`text/event-stream`)

## Déclaration importante

**Le contenu des ensembles de tests de ce projet est constitué de données fictives générées par l'IA, et non de données réelles. Toute ressemblance avec des faits réels serait purement fortuite.** Toutes les données sont uniquement destinées à évaluer la capacité des modèles d'IA à comprendre et analyser des formats structurés, et ne représentent aucun scénario métier ou entité réelle.

- `Benches/AI嘉豪测试/` a été adapté du [Test de culture IA de NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao), publié sous licence MIT
- Les autres ensembles de tests sont des données fictives générées par l'IA

## Licence

Licence Apache 2.0 — Voir le fichier [LICENSE](LICENSE)

---

**Ceci a probablement été écrit par une IA ayant bu de l'alcool frelaté — mon vrai travail, c'est de passer l'IA sur le grill.**
