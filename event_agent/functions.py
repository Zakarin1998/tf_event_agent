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

# MOCK DELLE FUNZIONI: search-flights , search-hotels, search-events
dct_fn_search_flights = {
    "name": "search_flights",
    "description": "Trova voli o treni per la tratta specificata",
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "Città di partenza"},
            "destination": {"type": "string", "description": "Città di arrivo"},
            "date": {"type": "string", "description": "Data di partenza (YYYY-MM-DD)"}
        },
        "required": ["origin", "destination", "date"]
    }
}

dct_fn_search_hotels = {
    "name": "search_hotels",
    "description": "Trova hotel disponibili nella città e periodo indicato",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Città di destinazione"},
            "checkin": {"type": "string", "description": "Data check-in (YYYY-MM-DD)"},
            "checkout": {"type": "string", "description": "Data check-out (YYYY-MM-DD)"}
        },
        "required": ["city", "checkin", "checkout"]
    }
}

dct_fn_search_events = {
    "name": "search_events",
    "description": "Cerca eventi nella città in una data specifica",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Città di destinazione"},
            "date": {"type": "string", "description": "Data in formato YYYY-MM-DD"}
        },
        "required": ["city", "date"]
    }
}

dct_fn_get_weather_forecast = {
    "name": "get_weather_forecast",
    "description": "Recupera previsioni del tempo per una città e data",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Città di interesse"},
            "date": {"type": "string", "description": "Data in formato YYYY-MM-DD"}
        },
        "required": ["city", "date"]
    }
}


FUNCTIONS = [
    # Funzioni file I/O che già avevi
    dct_fn_read_file,
    dct_fn_write_file,
    dct_fn_fetch_event_from_url,
    dct_fn_load_json,
    dct_fn_write_json,
    dct_fn_parse_html_file,
    # Nuove funzioni viaggio
    dct_fn_search_flights,
    dct_fn_search_hotels,
    dct_fn_search_events,
    dct_fn_get_weather_forecast
]
