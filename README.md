**README**

# AI-Powered Maven Dependency Agent

Un MVP Python per l’analisi e l’esplorazione delle dipendenze Maven di un progetto tramite GPT e graph analytics.

---

## 📁 Struttura del progetto

Organizziamo il codice in un package principale `eventbrite_agent` e uno script CLI in `cli.py`.

```
.
├── tf_event_agent/             # Modulo principale
│   ├── __init__.py
│   ├── config.py               # costanti, logging centralizzato, utilità JSON
│   ├── html_extractor.py       # parse_html_file: parsing HTML
│   ├── agent_functions.py      # implementazione funzioni callable (parse, read, write, load_json)
│   ├── functions.py            # schema JSON per le funzioni GPT
│   ├── gpt_wrap.py             # wrapper OpenAI Chat API
│   ├── interactive_agent.py    # classe EventBriteAgent + run_eventbrite_agent()
│   └── eventbrite_wrapper.py   # funzioni per costruire e interrogare grafo di dipendenze
├── resources/
│   └── event.html              # file HTML di esempio
├── cli.py                      # interfaccia a menu per l’agente
├── run_agent.py                # entrypoint semplice
├── setup.py                    # configurazione pip install
├── Makefile                    # comandi utili
└── requirements.txt            # dipendenze
```

> Il codice sorgente principale è in `tf_event_agent/`, per facilitare estensioni e test.

---

## 🚀 Funzionalità core

1. **Parsing HTML** (`event_agent.html_extractor.parse_html_file`)

   * Estrae `groupId`, `artifactId`, `version`, `packaging` e dipendenze.

2. **Salvataggio JSON** (`event_agent.agent_functions.write_file`)

   * Produce `event_info.json` con struttura:

     ```json
     {
       "project": {...},
       "dependencies": [{...}, ...]
     }
     ```
3. **Chat interattiva GPT** (`event_agent.interactive_agent.EventbriteAgent`)

   * Domande sull'HTML via function calling (parse, read, write, load\_json).
4. **CLI/Menu** (`cli.py`)

   * Menu numerato con domande predefinite e supporto custom.
5. **Grafo delle dipendenze** (`event_agent.graph_util`)

   * Utilizza `networkx` per creare un DiGraph di project→dependency.
   * Query: cammini, cicli, filtri per scope.

---

## 🔧 Installazione

```bash
git clone <url>
cd <repo>
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
make install
```

---

## 📋 Comandi principali

| Comando           | Descrizione                                               |
|-------------------| --------------------------------------------------------- |
| `make install`    | Installa il progetto in modalità editable                 |
| `make run`        | Avvia sessione interattiva (equiv. `python run_agent.py`) |
| `make cli`        | Avvia menu CLI (`python cli.py`)                          |
| `event-agent`     | Entry point interattivo (via console\_scripts)            |
| `event-agent-cli` | Menu CLI (via console\_scripts)                           |

---

## 🛠️ Config & Logging

* `event_agent.config.setup_logging(level)` imposta il root logger.
* Costanti in `event_agent.config`:

  * `HTML_FILE`, `TXT_REPORT`, `RECIPIENTS`, `NVD_URL`.
  * Namespace Maven per `ElementTree`.

---

## ⚙️ Funzioni callable GPT

* `parse_html_file(html_path: str) -> dict`
* `read_file(path: str) -> str`
* `write_file(path: str, content: str) -> dict`
* `load_json(path: str) -> dict`

---

## 📈 Grafo delle Dipendenze

Modulo di utilità (`event_agent.graph_util`):

```python
from networkx import DiGraph

def build_dependency_graph(data: dict) -> DiGraph:
    g = DiGraph()
    project = data['project']['artifactId']
    g.add_node(project, **data['project'])
    for dep in data['dependencies']:
        key = dep['artifactId']
        g.add_node(key, **dep)
        g.add_edge(project, key, scope=dep['scope'])
    return g
```

**Esempi di interrogazione**:

* `list(g.successors(project))`
* `list(nx.simple_cycles(g))`
* `[n for n, e in g[project].items() if e['scope']=='test']`

---

## 🔮 Next Steps

1. **CVE-check**: integrazione NVD per versioni vulnerabili.
2. **Multi-modulo**: supporto a progetti Maven multi-module.
3. **Esportazione**: GraphViz, YAML, Dashboard web.
4. **AI Enrichment**: spiegazioni e raccomandazioni LLM.

**Buon lavoro!**
