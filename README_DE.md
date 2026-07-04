# FormTest - Framework zur Bewertung der KI-Formatparsung

> **Alle Testdatensätze sind KI-generierte fiktive Daten, keine echten Daten. Ähnlichkeiten mit tatsächlichen Gegebenheiten sind rein zufällig.**
>
> **Dieses Projekt wurde nicht ausreichend durchdacht in Bezug auf Programmkonstruktion und Testplanung. Der Code und die Testabdeckung sind noch nicht ausgereift. Nur für Referenz- und Lernzwecke.**

Ein automatisiertes Test-Framework zur Bewertung der Fähigkeit großer Sprachmodelle (LLM), strukturierte Datenformate zu verstehen und zu parsen. Durch voreingestellte Testfälle ruft es automatisch die KI-API auf und vergleicht die Ergebnisse mit den erwarteten Antworten.

## Projektstruktur

```
FormTest/
├── APPs/              # Hauptanwendung (Flask-Backend + HTML-Frontend)
│   ├── app.py            # Flask-Einstiegspunkt, REST API + SSE-Streaming
│   ├── config.json       # Laufzeitkonfiguration
│   ├── requirements.txt  # Python-Abhängigkeiten
│   ├── run.bat           # Schnellstart-Skript
│   ├── static/           # Frontend-Dateien (index.html + CSS/JS)
│   └── data/             # Laufzeitdaten (Canvas-Status, usw.)
├── Benches/               # Testdatensätze (KI-generiert, keine echten Daten)
│   ├── 教学视频测试/     # Lehrvideo-Inhaltstest
│   ├── 企业信息测试/     # Unternehmensinformationstest
│   ├── 运行日志测试/     # Systembetriebsprotokolltest
│   └── Python测试/   # Python-Fortgeschrittenentest
├── .gitignore
├── LICENSE               # Apache License 2.0
└── README*.md            # Mehrsprachige README-Dateien
```

## Testdatensatz-Struktur

Jeder Testdatensatz folgt dieser Struktur:

```
Benches/<Name>/
├── 测试问题/             # Testfragen (JSON-Format)
│   ├── 基础问题.json     # Grundlegende Fragen
│   └── 进阶问题.json     # Fortgeschrittene Fragen
├── 测试系统提示词/       # Gleicher Inhalt in mehreren Formaten
│   ├── <Name>原版.txt    #   Klartext
│   ├── <Name>列表.txt    #   Nummerierte Liste
│   ├── <Name>JSON.txt    #   JSON
│   ├── <Name>YAML.txt    #   YAML
│   ├── <Name>XML.txt     #   XML
│   ├── <Name>Markdown.txt      # Markdown-Tabelle
│   ├── <Name>MarkdownKV.txt    # Markdown-Schlüssel-Wert
│   ├── <Name>DSL.txt     #   DSL
│   └── Zugehörige .json-Metadaten
└── 测试结果/             # Testergebnisse (automatisch erzeugt)
```

### Formatvarianten

| Format | Beschreibung |
|--------|-------------|
| Klartext | Originaltext (Basislinie) |
| Liste | Nummerierte/Aufzählungsliste |
| JSON | Standard JSON-Objekt |
| YAML | YAML-Strukturdaten |
| XML | XML-Hierarchie |
| Markdown | Markdown-Tabellen |
| MarkdownKV | Markdown-Schlüssel-Wert-Paare |
| DSL | Benutzerdefinierte DSL |

### Testbereiche

| Testsatz | Inhaltsbereich |
|----------|---------------|
| 教学视频测试 (Lehrvideo) | Python-Programmiervorlesung |
| 企业信息测试 (Unternehmen) | Fiktive Firmendaten |
| 运行日志测试 (Betriebsprotokolle) | System-Logs |
| Python测试 (Python Fortgeschritten) | Python-Dekoratoren/Generatoren/Context-Manager |

## Kernfunktionen

- **Multiformat-Vergleich** — Gleicher Inhalt in 8 Formaten
- **Batch-Automation** — Kartesisches Produkt aus Prompts × Fragen × Modellen
- **Multimodell-Parallel** — Mehrere KI-Modelle im Vergleich
- **Echtzeit-SSE-Streaming** — Live-Ergebnisse via Server-Sent Events
- **Mehrfachtestung** — Wiederholte Tests pro Frage (`test_count`)
- **Parallelitätssteuerung** — Konfigurierbare Threads und Wiederholungen
- **Inkrementelles Speichern** — Regelmäßige Zwischenspeicherung
- **Archiv-Snapshots** — Testkonfiguration speichern/laden

## Schnellstart

```bash
pip install -r APPs/requirements.txt
cd APPs
python app.py
```

Browser öffnen: http://localhost:5000

Nach dem Start im Web-UI oben rechts auf "Einstellungen" klicken, um API-Adresse, Modell und Parameter zu konfigurieren.

## API-Endpunkte

| Endpunkt | Methode | Beschreibung |
|----------|---------|-------------|
| `/api/v1/config` | GET/POST | Konfiguration |
| `/api/v1/models` | GET | Modelle auflisten |
| `/api/v1/test-set/scan` | GET | Testsets scannen |
| `/api/v1/test-set/prompts` | GET | Prompts abrufen |
| `/api/v1/test-set/questions` | GET | Fragen abrufen |
| `/api/v1/test-set/results` | GET | Ergebnisse abrufen |
| `/api/v1/run-tests` | POST | Tests ausführen (SSE) |
| `/api/v1/stop-tests` | POST | Tests stoppen |
| `/api/v1/canvas-state` | GET/POST | Canvas-Status |
| `/api/v1/archives` | GET/POST/DELETE | Archivverwaltung |
| `/api/v1/tags` | GET | Alle Tags abrufen |

## Technologie-Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Vanilla HTML / CSS / JavaScript
- **KI-Aufrufe**: `requests` (SSE + JSON)
- **Parallelität**: `ThreadPoolExecutor`
- **Ausgabe**: Server-Sent Events (`text/event-stream`)

## Wichtiger Hinweis

**Alle Testdatensätze in diesem Projekt sind KI-generierte fiktive Daten, keine echten Daten. Ähnlichkeiten mit tatsächlichen Personen, Organisationen oder Szenarien sind rein zufällig.** Diese Daten dienen ausschließlich der Bewertung der Fähigkeit von KI-Modellen, strukturierte Formate zu verstehen und zu parsen.

## Lizenz

Apache License 2.0 — Siehe [LICENSE](LICENSE)

---

**Das könnte etwas sein, das eine KI unter Alkoholeinfluss geschrieben hat. Mein Hauptziel ist es, die KI zu quälen.**
