# KI-Modell Test-Framework

> **警告 Warning**: 尚未完成正在优化前端随后重构后端及文件结构

Ein automatisiertes Test-Framework zur Bewertung der Fähigkeiten von Large Language Models (LLM), strukturierte Datenformate zu verstehen und zu parsen.

## Überblick

Dieses Projekt dient zur Bewertung und zum Testen der Fähigkeit von KI-Modellen, verschiedene strukturierte Datendateiformate zu verstehen und zu parsen. Durch voreingestellte Testfälle ruft es automatisch die KI-API auf und vergleicht die zurückgegebenen Ergebnisse mit den erwarteten Antworten, um die Formatverständnisleistung des Modells zu quantifizieren.

## Projektstruktur

```
草稿A/
├── 测试软件/           # Hauptanwendung (Flask-Backend + HTML-Frontend)
├── 测试软件2/         # Konfigurationsvariante (verschiedene Modelle/Parameter)
├── 测试软件3/
├── 测试软件4/
├── 测试集/           # Testdatensatz (keine echten Fälle, KI-generiert)
│   ├── 被测试文件/    # Beispieldateien in verschiedenen Formaten
│   │   ├── XML/
│   │   ├── JSON/
│   │   ├── YAML/
│   │   ├── Markdown/
│   │   ├── DSL/
│   │   └── 列表示例/
│   ├── 教学视频测试问题/
│   ├── 运行日志测试问题/
│   ├── 企业信息测试问题/
│   └── UI.json       # Testoberflächenkonfiguration
├── 备份/             # Historische Format-Backups
├── 更新日志/         # Fehlerbehebungsprotokolle
└── 任务说明/         # Entwicklungsaufgabendokumente
```

## Unterstützte Formate

- XML
- JSON
- YAML
- Markdown (einschließlich Tabellen, KV-Schlüssel-Wert-Paare)
- DSL (Domänenspezifische Sprache)
- Nur-Text-Listen

## Kernfunktionen

1. **Multiformat-Test**: Testet Parsing-Fähigkeiten mehrerer Datenformate gleichzeitig
2. **Batch-Test**: Führt Testfälle im Batch mit Streaming-Ausgabe aus
3. **Multimodell-Unterstützung**: Konfiguriert mehrere KI-Modelle für Vergleichstests
4. **Antwort-Caching**: Vermeidet wiederholte API-Aufrufe für beschleunigte Iterationstests
5. **Benutzerdefinierter System-Prompt**: Konfiguriert Test-Assoziationen über bindings.json
6. **Parallelitätskontrolle**: Konfigurierbare Parallelität und Wiederholungsanzahl

## Schnellstart

### 1. Abhängigkeiten installieren

```bash
pip install -r 测试软件/requirements.txt
```

### 2. Dienst starten

```bash
cd 测试软件
python app.py
# oder Doppelklick auf run.bat
```

### 3. Oberfläche aufrufen

Browser öffnen http://localhost:5000

### 4. Konfigurieren und ausführen

1. API-Adresse und Modellparameter in Einstellungen konfigurieren
2. Zu testende Formatdateien und Testfragengruppen auswählen
3. Auf "Test starten" klicken
4. Echtzeit-Ergebnisstream und Endergebnisse anzeigen

## Konfiguration

| Parameter | Beschreibung | Standardwert |
|------|------|--------|
| base_url | API-Adresse | http://192.168.1.45:1919/v1 |
| model | Modellname | qwen3.5-0.8b |
| temperature | Temperatur | 0.7 |
| concurrency | Parallelität | 1 |
| test_count | Tests pro Frage | 1 |
| max_retries | Max. Wiederholungen | 3 |

## API-Endpunkte

| Endpunkt | Methode | Beschreibung |
|------|------|------|
| /api/v1/config | GET/POST | Konfigurationsverwaltung |
| /api/v1/models | GET | Verfügbare Modelle abrufen |
| /api/v1/ui-config | GET | Testoberflächenkonfiguration abrufen |
| /api/v1/question-groups | GET | Fragengruppen abrufen |
| /api/v1/bindings | GET/POST | Bindungskonfiguration |
| /api/v1/run-tests | POST | Tests ausführen (SSE-Streaming) |
| /api/v1/results | GET | Alle Testergebnisse abrufen |
| /api/v1/answer-cache | GET | Antwort-Cache abrufen |

## Wichtiger Hinweis

### Testdatensatz-Erklärung

**Der gesamte Inhalt im Testdatensatz dieses Projekts KI-generierte Beispiele, keine echten Falldaten.**

Der Testdatensatz enthält:
- Tutorial-Videoinformations-Beispiele
- Betriebsprotokoll-Beispiele
- Unternehmensinformations-Beispiele
- Beispieldateien in verschiedenen Formaten (XML, JSON, YAML, Markdown, DSL)

Diese Daten werden ausschließlich zum Testen der Fähigkeiten von KI-Modellen verwendet, strukturierte Formate zu verstehen und zu parsen, und repräsentieren keine realen Geschäftsszenarien.

## Technologie-Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Vanilla HTML + CSS + JavaScript
- **API-Aufrufe**: requests (Streaming SSE)
- **Testausführung**: ThreadPoolExecutor-Parallelität

## Versionshistorie

Siehe `更新日志/changelog.json`

## Lizenz

Apache License 2.0 - Siehe [LICENSE](LICENSE)