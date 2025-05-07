
# 🧾 Namens- & Programmierkonventionen

## ===============================
## 1. NAMENSKONVENTIONEN
## ===============================

### 🔤 SPRACHE
- Alle Namen in **Englisch**
- Keine Abkürzungen oder Fantasienamen

### 🧮 FUNKTIONEN
- Format: `snake_case`
- Benennung: **Verb + Objekt**
  - Beispiel: `load_data()`, `calculate_mean()`

### 🧱 KLASSEN
- Format: `PascalCase`
- Benennung: **Substantiv**
  - Beispiel: `DataCleaner`, `ModelRunner`

### 🔣 VARIABLEN
- Format: `snake_case`
- Klar und beschreibend
  - Beispiel: `user_name`, `max_value`

### 🔒 KONSTANTEN
- Format: `UPPER_SNAKE_CASE`
  - Beispiel: `MAX_RETRIES`, `DEFAULT_TIMEOUT`



## ===============================
## 2. BRANCH-KONVENTIONEN
## ===============================

### 🔀 Format: `typ/kurze_beschreibung`

#### 📁 Gängige Typen:
- `feature/` – für neue Features
- `bugfix/` – für Fehlerbehebungen
- `refactor/` – für Code-Umstrukturierungen ohne Verhaltensänderung
- `test/` – für neue oder angepasste Tests
- `docs/` – für Dokumentation

#### ✅ Regeln:
- Nur Kleinbuchstaben
- Wörter mit `_` trennen
- Keine Sonderzeichen
- Verben im Infinitiv verwenden

#### 💡 Beispiele:
- `feature/add_user_authentication`
- `bugfix/fix_login_redirect`
- `refactor/optimize_data_loader`



## ===============================
## 3. KOMMENTARKONVENTIONEN
## ===============================

### 🗣️ Allgemeine Kommentare
- Immer auf **Englisch**
- Klar, in vollständigen Sätzen
- Beginnen mit Großbuchstaben

```python
# Load data from external API
# This function initializes the user session
```

### ⚠️ Spezielle Tags

| Tag     | Zweck                                   |
|---------|------------------------------------------|
| `TODO`  | Aufgabe, die noch umgesetzt werden muss |
| `FIXME` | Bekannter Fehler, der zu beheben ist    |
| `NOTE`  | Wichtiger Hinweis oder Kontext          |
| `HACK`  | Temporäre, unschöne Zwischenlösung      |

#### 💬 Beispiele:

```python
# TODO: Add unit test for this function
# FIXME: This causes an index out of range error
# NOTE: This assumes the input is already validated
# HACK: Hardcoded token, replace later
```


## ===============================
## 4. COMMIT-KONVENTIONEN
## ===============================

### 🧾 Format: `typ(bereich): nachricht`

#### 🧷 Typen

| Typ       | Bedeutung                              |
|-----------|-----------------------------------------|
| `feat`    | Neues Feature                           |
| `fix`     | Fehlerbehebung                          |
| `docs`    | Änderungen an der Dokumentation         |
| `style`   | Formatierung, keine Logikänderung       |
| `refactor`| Codeänderung ohne funktionale Änderung  |
| `test`    | Hinzufügen oder Anpassen von Tests      |
| `chore`   | Wartung, Tools, CI/CD                   |

### ✏️ Regeln:
- In **Englisch**
- **Präsens**, keine Vergangenheitsform
- Max. **72 Zeichen** für die erste Zeile
- **Kein Punkt** am Ende der ersten Zeile

#### 💡 Beispiele:
- `feat(auth): add OAuth2 login support`
- `fix(ui): resolve button misalignment`
- `refactor(api): simplify data fetch logic`
- `test(model): add null case coverage`



## ===============================
## 5. DATEI- UND DOKUMENTKONVENTIONEN
## ===============================

### 📄 Allgemeine Regeln für Dateinamen

- Sprache: **Englisch**
- Format: `lower_snake_case`
- Keine Leerzeichen oder Sonderzeichen (außer `_` und `.`)
- Dateityp und -zweck sollen klar erkennbar sein
- Vermeide generische Namen wie `test.py`, `document.txt`

### 🔢 Versionierung (falls nötig)
- Verwende `v1`, `v2`, `final`, `draft` **nur mit Kontext**
- Beispiel: `project_plan_v2_draft.md`
- Bei Code-Dateien kann Versionierung auch durch Git-Tags oder Branches erfolgen

```python
# Beispiel: Versionierung über Git
# Tag setzen: git tag v1.0 -m "First stable release"
# Tag pushen: git push origin v1.0
```

### 📁 Beispiele
| Dateityp       | Beispielname                     |
|----------------|----------------------------------|
| Python-Skript  | `load_user_data.py`              |
| CSV-Datei      | `exported_user_data_2024.csv`    |
| Markdown-Doku  | `api_documentation.md`           |
| Konfig-Datei   | `config_prod.yaml`               |
| Notebook       | `exploratory_analysis.ipynb`     |

### ✅ Zusätzliche Hinweise
- Projektübergreifend einheitliche Benennung bevorzugen
- Bei mehrteiligen Dateien klare Präfixe verwenden (`01_`, `02_` usw.)
- Für temporäre/experimentelle Dateien: `tmp_`, `sandbox_`, `dev_`

---
