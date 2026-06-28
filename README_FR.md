# FormTest - Framework d'Évaluation du Parsing de Formats par l'IA

> **Tous les ensembles de données de test sont des données fictives générées par IA, et non des données réelles. Toute ressemblance avec des faits réels serait purement fortuite.**
>
> **Ce projet manque d'une planification rigoureuse de la construction du programme et des tests. La structure du code et la couverture des tests ne sont pas complètes. À des fins de référence et d'apprentissage uniquement.**

Un framework de test automatisé pour évaluer la capacité des grands modèles de langage (LLM) à comprendre et analyser les formats de données structurés.

## Structure du Projet

```
FormTest/
├── APPs/              # Application principale (Backend Flask + Frontend HTML)
│   ├── app.py            # Point d'entrée Flask, API REST + SSE
│   ├── config.json       # Configuration d'exécution
│   ├── requirements.txt  # Dépendances Python
│   ├── run.bat           # Script de démarrage rapide
│   ├── static/           # Fichiers frontend (index.html + CSS/JS)
│   └── data/             # Données d'exécution
├── Benches/               # Données de test (générées par IA, non réelles)
│   ├── 教学视频测试/     # Test de contenu vidéo pédagogique
│   ├── 企业信息测试/     # Test d'informations d'entreprise
│   ├── 运行日志测试/     # Test de journaux d'exploitation
│   └── Python进阶测试/   # Test Python avancé
├── .gitignore
├── LICENSE               # Apache License 2.0
└── README*.md            # README multilingue
```

## Fonctionnalités Principales

- **Comparaison multi-format** — Même contenu dans 8 formats
- **Automatisation par lots** — Produit cartésien prompts × questions × modèles
- **Modèles multiples en parallèle** — Comparaison horizontale
- **Streaming SSE en temps réel**
- **Tests multiples** — Répétition configurable par question
- **Contrôle de concurrence**
- **Sauvegarde incrémentielle**
- **Snapshots d'archive**

## Démarrage Rapide

```bash
pip install -r APPs/requirements.txt
cd APPs
python app.py
```

Ouvrir le navigateur : http://localhost:5000

Après le démarrage, cliquez sur "Paramètres" en haut à droite de l'interface web pour configurer l'API, le modèle et les paramètres.

## Avis Important

**Tous les ensembles de données de test dans ce projet sont des données fictives générées par IA, et non des données réelles. Toute ressemblance avec des entités, organisations ou scénarios réels serait purement fortuite.** Ces données sont utilisées uniquement pour évaluer la capacité des modèles d'IA à comprendre et analyser les formats structurés.

## Licence

Apache License 2.0 — Voir [LICENSE](LICENSE)

---

**Ce pourrait être quelque chose écrit par une IA sous l'emprise de l'alcool. Mon objectif principal est de torturer l'IA.**
