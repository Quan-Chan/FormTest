# Framework de Test de Modèles IA

Un framework de test automatisé pour évaluer la capacité des grands modèles de langage (LLM) à comprendre et analyser les formats de données structurés.

## Aperçu

Ce projet est conçu pour évaluer et tester la capacité des modèles IA à comprendre et analyser les fichiers de formats de données structurés. À travers des cas de test prédéfinis, il appeler automatiquement l'API IA et compare les résultats retournés avec les réponses attendues, quantifiant ainsi les performances du modèle dans la compréhension des formats.

## Structure du projet

```
草稿A/
├── 测试软件/           # Application principale (Backend Flask + Frontend HTML)
├── 测试软件2/         # Variante de configuration (différents modèles/paramètres)
├── 测试软件3/
├── 测试软件4/
├── 测试集/           # Ensemble de données de test (cas non réels, généré par IA)
│   ├── 被测试文件/    # Fichiers d'exemple dans divers formats
│   │   ├── XML/
│   │   ├── JSON/
│   │   ├── YAML/
│   │   ├── Markdown/
│   │   ├── DSL/
│   │   └── 列表示例/
│   ├── 教学视频测试问题/
│   ├── 运行日志测试问题/
│   ├── 企业信息测试问题/
│   └── UI.json       # Configuration de l'interface de test
├── 备份/             # Sauvegardes de formats historiques
├── 更新日志/         # Journaux de correction de bugs
└── 任务说明/         # Documents de tâches de développement
```

## Formats pris en charge

- XML
- JSON
- YAML
- Markdown (y compris les tables, paires clé-valeur)
- DSL (Langage Spécifique au Domaine)
- Listes de texte brut

## Fonctionnalités principales

1. **Test multi formats**: Teste les capacités d'analyse de plusieurs formats de données simultanément
2. **Test par lots**: Exécute les cas de test par lots avec sortie en streaming
3. **Support multi modèles**: Configure plusieurs modèles IA pour des tests comparatifs
4. **Cache des réponses**: Évite les appels API répétés pour accélérer les tests itératifs
5. **System Prompt personnalisé**: Configure les associations de test via bindings.json
6. **Contrôle de concurrence**: Concurrence et nombre de tentatives configurables

## Démarrage rapide

### 1. Installer les dépendances

```bash
pip install -r 测试软件/requirements.txt
```

### 2. Démarrer le service

```bash
cd 测试软件
python app.py
# oudouble-cliquez sur run.bat
```

### 3. Accéder à l'interface

Ouvrez le navigateur à http://localhost:5000

### 4. Configurer et exécuter

1. Configurez l'adresse API et les paramètres du modèle dans les paramètres
2. Sélectionnez les fichiers de format et les groupes de questions de test
3. Cliquez sur "Démarrer le test"
4. Visualisez le flux de résultats en temps réel et les scores finaux

## Configuration

| Paramètre | Description | Valeur par défaut |
|------|------|--------|
| base_url | Adresse API | http://192.168.1.45:1919/v1 |
| model | Nom du modèle | qwen3.5-0.8b |
| temperature | Température | 0.7 |
| concurrency | Concurrence | 1 |
| test_count | Tests par question | 1 |
| max_retries | Tentatives max | 3 |

## Points de terminaison API

| Point | Méthode | Description |
|------|------|------|
| /api/v1/config | GET/POST | Gestion de configuration |
| /api/v1/models | GET | Obtenir les modèles disponibles |
| /api/v1/ui-config | GET | Obtenir la configuration de l'interface |
| /api/v1/question-groups | GET | Obtenir les groupes de questions |
| /api/v1/bindings | GET/POST | Configuration des liaisons |
| /api/v1/run-tests | POST | Exécuter les tests (streaming SSE) |
| /api/v1/results | GET | Obtenir tous les résultats de tests |
| /api/v1/answer-cache | GET | Obtenir le cache des réponses |

## Avis important

### Déclaration de l'ensemble de données de test

**Tout le contenu de l'ensemble de données de test de ce projet est des exemples générés par IA, pas des données de cas réels.**

L'ensemble de données de test inclut :
- Exemples d'informations de vidéos tutoriels
- Exemples de journaux d'opérations
- Exemples d'informations d'entreprise
- Fichiers d'exemple dans divers formats (XML, JSON, YAML, Markdown, DSL)

Ces données sont utilisées uniquement pour tester les capacités de compréhension et d'analyse des formats structurés des modèles IA, et ne représentent aucun scénario métier réel.

## Pile technologique

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: HTML + CSS + JavaScript vanilla
- **Appels API**: requests (streaming SSE)
- **Exécution des tests**: Concurrence ThreadPoolExecutor

## Historique des versions

Voir `更新日志/changelog.json`

## Licence

MIT