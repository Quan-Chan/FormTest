# FormTest – Framework zum Testen der Fähigkeit zur Analyse strukturierter Formate durch KI

> **Alle beigefügten Testsätze sind KI-generierte fiktive Daten, keine echten Daten. Ähnlichkeiten mit tatsächlichen Gegebenheiten sind rein zufällig.**
>
> **Dieses Projekt wurde nicht gründlich durchdacht und getestet. Die Codestruktur und Testabdeckung sind unvollständig und dienen ausschließlich zu Referenz- und Lernzwecken.**

Ein automatisiertes Test-Framework zur Bewertung der Fähigkeit großer Sprachmodelle (LLMs), strukturierte Datenformate zu verstehen und zu parsen. Es verwendet vordefinierte Testfälle, ruft automatisch die KI-API auf und vergleicht die zurückgegebenen Ergebnisse mit den erwarteten Antworten, um die Formatverständnisleistung des Modells zu quantifizieren.

## Schnellstart

### 1. Abhängigkeiten installieren

```bash
pip install -r APPs/requirements.txt
```

### 2. Starten

```bash
cd APPs
python app.py
# Oder Doppelklick auf run.bat
```

Öffnen Sie [http://localhost:5000](http://localhost:5000) im Browser.

### 3. Konfiguration

Klicken Sie nach dem Start in der oberen rechten Ecke der Weboberfläche auf die Schaltfläche **Einstellungen**, um die API-Adresse, das Modell, Parameter usw. zu konfigurieren. Sie können auch `APPs/config.example.json` als Vorlage für eine Konfigurationsdatei verwenden.

Wichtige Konfigurationsoptionen:
- `base_url` — API-Adresse (unterstützt automatisches Anhängen von `/v1`)
- `model` — Standardmodellname
- `model_thinking_config` — Reasoning/Thinking-Modus pro Modell konfigurieren
- `streaming` — SSE-Streaming-Ein/Ausschalter
- `concurrency` — Anzahl gleichzeitiger Threads
- `disabled_params` — Im Frontend ausgeblendete/deaktivierte Parameter

### 4. Tests ausführen

1. Kombinieren Sie auf der **Leinwand** mit dem Node-Editor: Prompt × Frage × Modell
2. Klicken Sie auf **Test starten**, um die Streaming-Ergebnisse in Echtzeit zu sehen
3. Nach dem Test können Sie die Ergebnisse unter **Verlauf** einsehen/filtern

## Projektstruktur

```
FormTest/
├── APPs/                          # Hauptanwendung
│   ├── app.py                     # Flask-Backend (API + Testausführungs-Engine + SSE-Streaming)
│   ├── requirements.txt           # Python-Abhängigkeiten
│   ├── run.bat                    # Windows-Startskript
│   ├── config.example.json        # Konfigurationsvorlage
│   ├── flow.json                  # Flussdiagrammdefinition
│   └── static/
│       └── index.html             # Frontend-SPA (reines HTML/CSS/JS, ~7300 Zeilen)
├── Benches/                       # Testdatensätze
│   ├── AI嘉豪测试/                # KI-Literatur-Multiple-Choice (adaptiert von NAGI STUDIO)
│   ├── Python测试/                # Python-Fortgeschrittenen-Wissenstest
│   ├── 企业信息测试/              # Fiktive Firmenregistrierungsdaten
│   ├── 教学视频测试/              # Python-Anfänger-Tutorial-Videoinhalte
│   └── 运行日志测试/              # Systembetriebsprotokollanalyse
├── skills/                        # Werkzeugskripte für direkte Benutzung
│   ├── New-TestSet-新建测试集.ps1 # PowerShell-Skript zum Erstellen eines neuen Testsatz-Gerüsts
│   └── QA-Extract-问答提取.md     # Anleitung zum Extrahieren von Q&A-Paaren aus Quelldateien
├── .opencode/
│   └── skills/                    # opencode-KI-Fähigkeiten (für KI-Agenten-Unterstützung)
│       ├── new-test-set/          # Testsatz-Gerüst erstellen
│       └── qa-extract/            # Q&A-Paar-Extraktion
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # Diese Datei
```

## Testsätze

### Struktur

Jeder Testsatz verwendet `.test-set-part`-Markierungsdateien, um die Rollen der Unterverzeichnisse zu identifizieren. Verzeichnisnamen können beliebig sein; das System erkennt die Rollen anhand des Inhalts der Markierungsdatei:

```
Benches/<Name>/
├── <Fragenverzeichnis>/           # Enthält .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10 Fragen
│   └── 进阶问题.json              # 10 Fragen (manche Testsätze nur grundlegende)
├── <Promptverzeichnis>/           # Enthält .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <Name>原版.json            # Reiner Text (Erzählformat)
│   ├── <Name>列表.json            # Nummerierte Listenformat
│   ├── <Name>JSON.json            # JSON-strukturiertes Format
│   ├── <Name>YAML.json            # YAML-Format
│   ├── <Name>XML.json             # XML-Format
│   ├── <Name>Markdown.json        # Markdown-Tabellenformat
│   ├── <Name>MarkdownKV.json      # Markdown-Schlüssel-Wert-Paare
│   └── <Name>DSL.json             # Benutzerdefiniertes DSL-Format
└── <Ergebnisverzeichnis>/         # Enthält .test-set-part → "results" (zur Laufzeit generiert)
    └── .test-set-part
```

### Testformate

| Format | Beschreibung |
|--------|-------------|
| Original (Plain Text) | Reiner Text (Erzählung), als Basislinie |
| Liste (List) | Nummerierte/Aufzählungsliste |
| JSON | Standard-JSON-Objekt |
| YAML | YAML-strukturierte Daten |
| XML | XML-Tag-Hierarchie |
| Markdown | Markdown-Tabelle |
| MarkdownKV | Markdown-Schlüssel-Wert-Paare |
| DSL | Benutzerdefinierte domänenspezifische Sprache |

### Testdomänen

| Testsatz | Inhaltsdomäne | Anzahl | Quelle |
|----------|--------------|--------|--------|
| 教学视频测试 | Python-Programmiervorlesungs-Transkript | 20 | KI-fiktiv |
| 企业信息测试 | Fiktive Firmenregistrierungsdaten | 20 | KI-fiktiv |
| 运行日志测试 | Systembetriebsprotokolleinträge | 20 | KI-fiktiv |
| Python测试 | Python-Dekorateure/Generatoren/Kontextmanager | 20 | KI-fiktiv |
| AI嘉豪测试 | KI-Literatur-Multiple-Choice (Grundlagen/Fortgeschritten/Irrtümer/Geisteswissenschaften) | 30 | Adaptiert von [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## Kernfunktionen

- **Visueller Leinwandeditor** — SVG-Knoten-Leinwand, Kombination von Prompt × Frage × Modell per Drag & Drop, mit Verbindungslinienzeichnung
- **Rückgängig/Wiederholen** — Vollständiges Verlaufssystem mit Unterstützung für Strg+Z / Strg+Umschalt+Z
- **Multi-Format-Vergleichstests** — Gleicher Inhalt in 8 Formaten dargestellt, Bewertung der Formatverständnisunterschiede des Modells
- **Batch-Automatisierte Tests** — Kartesisches Produkt aus Prompt × Frage × Modell, automatisch parallel ausgeführt
- **Multi-Modell-Verwaltung** — Modell-Popup-Management mit Unterstützung zum Hinzufügen/Löschen/Sortieren zusätzlicher Modelle
- **Reasoning-Konfiguration** — Pro Modell unabhängige Konfiguration von Thinking/Reasoning_Effort-Parametern
- **Parameter-Umschaltung** — Jeder Parameter kann einzeln per Dot-Toggle aktiviert/deaktiviert werden
- **Streaming-Echtzeitausgabe** — SSE-basierter Streaming-Ergebnis-Push, Echtzeit-Sichtbarkeit des Testfortschritts
- **Verlaufsanzeige** — Filtern historischer Ergebnisse nach Status/Modell/Textsuche
- **Archivieren/Wiederherstellen** — Speichern/Laden von Testkonfigurations-Snapshots (inkl. Leinwandstatus + Modell-Reasoning-Konfiguration)
- **_notFound-Modellerkennung** — Leinwand erkennt nicht verfügbare Modelle automatisch und zeigt ⚠-Warnung an
- **Automatische /v1-Ergänzung** — Umschalter zum automatischen Anhängen von `/v1` an die API-Adresse
- **Dunkles/Helles Thema** — Vollständiges CSS-Variablensystem zur Themenumschaltung
- **Anthropic-API-Unterstützung** — Unterstützt Anthropic-Nachrichtenformat + dedizierte SSE-Reasoning-Analyse
- **Mehrrundentests** — Einzelfrage kann mehrfach wiederholt werden, um Antwortstabilität zu messen
- **Parallelitätssteuerung** — Konfigurierbare Anzahl gleichzeitiger Threads und Wiederholungsstrategie
- **Inkrementelles Speichern** — Regelmäßiges inkrementelles Speichern von Ergebnissen während des Tests, um Datenverlust zu verhindern
- **Pfadsicherheitsvalidierung** — Verhindert Path-Traversal-Angriffe, Windows-reservierte Namensprüfung, Dateinamen-Whitelist

## API-Endpunkte

| Endpunkt | Methode | Beschreibung |
|----------|---------|-------------|
| `/` | GET | Liefert das Frontend-SPA |
| `/api/v1/config` | GET/POST | Konfiguration lesen/speichern |
| `/api/v1/models` | GET/POST | Verfügbare Modellliste abrufen/Modellliste speichern |
| `/api/v1/test-set/scan` | GET | Testsätze scannen |
| `/api/v1/test-set/prompts` | GET | System-Prompts der Testsätze abrufen |
| `/api/v1/test-set/questions` | GET | Testsatzfragen abrufen |
| `/api/v1/test-set/results` | GET | Historische Testergebnisse abrufen |
| `/api/v1/test-job/hub` | POST | Einheitliche Aufgabenverteilung (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | SSE-Streaming-Echtzeit-Ergebnis-Push |
| `/api/v1/canvas-state` | GET/POST | Leinwandstatus speichern/lesen |
| `/api/v1/archives` | GET/POST/DELETE | Archivverwaltung |
| `/api/v1/tags` | GET | Alle Tags abrufen |

Fehlerantworten: `404` → `{"error": "Not found"}`, `500` → `{"error": "Interner Serverfehler"}`

## Konfigurationsoptionen

| Schlüssel | Typ | Beschreibung |
|-----------|------|-------------|
| `api_key` | string | API-Schlüssel |
| `base_url` | string | API-Adresse |
| `model` | string | Standardmodellname |
| `models` | string[] | Zusätzliche Modellliste |
| `temperature` | float | Temperatur (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | Kontextgröße |
| `concurrency` | int | Anzahl gleichzeitiger Threads (1-50) |
| `test_count` | int | Anzahl Testwiederholungen pro Frage |
| `max_retries` | int | Maximale Wiederholungsanzahl |
| `streaming` | bool | SSE-Streaming-Ein/Aus |
| `timeout` | int | Anfrage-Timeout in Sekunden |
| `model_thinking_config` | object | Pro-Modell-Reasoning-Konfiguration, z.B. `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Anthropic-Nachrichtenformat erzwingen |
| `force_openai_endpoint` | bool | OpenAI-kompatiblen Endpunkt erzwingen |
| `disabled_params` | string[] | Liste der im Frontend ausgeblendeten/deaktivierten Parameter |

## OpenCode-Fähigkeiten

Dieses Projekt enthält zwei Werkzeugfähigkeiten, die beim schnellen Erstellen und Verwalten von Testsätzen helfen:

### Benutzerwerkzeuge (`skills/`)

Skripte und Dokumentation, die Entwickler direkt ausführen können:

| Datei | Beschreibung |
|-------|-------------|
| `skills/New-TestSet-新建测试集.ps1` | PowerShell-Skript, das automatisch ein nummeriertes Testsatz-Gerüstverzeichnis und `.test-set-part`-Markierungsdateien erstellt |
| `skills/QA-Extract-问答提取.md` | Detaillierte Anleitung zum Extrahieren von Q&A-Paaren aus Quelldateien und Generieren kompatibler JSON-Dateien |

### KI-Agenten-Fähigkeiten (`.opencode/skills/`)

Wenn Sie [opencode](https://opencode.ai) oder ein kompatibles KI-Codierungstool verwenden, können die Fähigkeiten unter `.opencode/skills/` automatisch vom KI-Agenten entdeckt und geladen werden:

| Fähigkeit | Beschreibung |
|-----------|-------------|
| `new-test-set` | Führt die KI beim Erstellen eines Testsatz-Gerüsts (Verzeichnisse + Markierungsdateien), unterstützt automatische Nummerierung zur Vermeidung von Konflikten |
| `qa-extract` | Führt die KI beim Extrahieren von Q&A-Paaren aus Quelldateien, Ausgabe als JSON kompatibel mit dem FormTest-Testsatzformat |

## Technologie-Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Reines HTML / CSS (benutzerdefiniertes Variablensystem, dunkle/helle Themen) / JavaScript
- **KI-Aufrufe**: `requests`-Bibliothek (unterstützt sowohl SSE-Streaming als auch regulären JSON-Modus, kompatibel mit OpenAI / Anthropic API)
- **Parallelität**: `ThreadPoolExecutor`-Threadpool + exponentielles Backoff-Retry
- **Ausgabe**: Server-Sent Events (`text/event-stream`)

## Wichtiger Hinweis

**Der Inhalt der Testsätze in diesem Projekt besteht vollständig aus KI-generierten fiktiven Beispieldaten, keinen echten Daten. Ähnlichkeiten mit tatsächlichen Gegebenheiten sind rein zufällig.** Alle Daten dienen ausschließlich der Bewertung der Fähigkeit von KI-Modellen, strukturierte Formate zu verstehen und zu parsen, und repräsentieren keine realen Geschäftsszenarien oder Entitäten.

- `Benches/AI嘉豪测试/` ist adaptiert von [NAGI STUDIOs AI Jiahao Test](https://github.com/nagi-studio/ai-jiahao), veröffentlicht unter der MIT-Lizenz
- Alle anderen Testsätze sind KI-generierte fiktive Daten

## Lizenz

Apache License 2.0 – siehe [LICENSE](LICENSE)-Datei für Details

---

**Das könnte etwas sein, das eine KI geschrieben hat, während sie auf Fuselalkohol betrunken war – meine Hauptaufgabe ist es, die KI durchzuhecheln.**
