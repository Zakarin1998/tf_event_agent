"""GPT functions module."""

dct_fn_read_file = {
    "name": "read_file",
    "description": "Legge il contenuto di un file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Percorso del file da leggere."}
        },
        "required": ["path"]
    }
}

dct_fn_write_file = {
    "name": "write_file",
    "description": "Scrive contenuto su file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Percorso di destinazione."},
            "content": {"type": "string", "description": "Contenuto da scrivere nel file."}
        },
        "required": ["path", "content"]
    }
}

dct_fn_parse_html_file = {
    "name": "parse_html_file",
    "description": "Legge un event.html, estrae informazioni e restituisce una struttura JSON.",
    "parameters": {
        "type": "object",
        "properties": {
            "pom_path": {
                "type": "string",
                "description": "Percorso al file event.html"
            }
        },
        "required": ["html_path"]
    }
}

dct_fn_load_json = {
    "name": "load_json",
    "description": "Carica un file JSON da disco e restituisce la struttura.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Percorso al file JSON"
            }
        },
        "required": ["path"]
    }
}


dct_fn_write_json = {
    "name": "write_json",
    "description": "Salva dati JSON su file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Percorso file di destinazione."},
            "content": {"type": "object", "description": "Contenuto JSON da scrivere."}
        },
        "required": ["path", "content"]
    }
}


dct_fn_fetch_event_from_url = {
    "name": "fetch_event_from_url",
    "description": "Recupera informazioni di un evento Eventbrite usando l'URL.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {"type": "string", "description": "URL dell'evento su Eventbrite."}
        },
        "required": ["url"]
    }
}

FUNCTIONS = [
    dct_fn_read_file,
    dct_fn_write_file,
    dct_fn_fetch_event_from_url,
    dct_fn_load_json,
    dct_fn_write_json,
    dct_fn_parse_html_file,
]
