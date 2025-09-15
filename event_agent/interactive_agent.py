"""Interactive function call agent"""
import logging
import json
from event_agent.gpt_wrap import chat_functions, gpt_choice_message
from event_agent.functions import FUNCTIONS
from event_agent.agent_functions import (
    write_file,
    read_file,
    load_json,
    write_json,
    # parse_html_file,
    fetch_event_from_url,
    list_events_by_query
)

logger = logging.getLogger(__name__)

FUNCTION_DISPATCHER = {
    # "parse_html_file": parse_html_file,
    "write_file": write_file,
    "read_file": read_file,
    "load_json": load_json,
    "write_json": write_json,
    "fetch_event_from_url": fetch_event_from_url,
    "list_events_by_query": list_events_by_query
}


class EventbriteAgent:
    def __init__(self):
        self.chat_history = []
        logger.info("🤖 Avvio di Eventbrite Agent...")

        initial_prompt = f"""
            Sei un assistente tecnico. 
            Il tuo compito è di elaborare le informazioni da un file HTML
            
            - trovare URL di Eventbrite di eventi in relazione con la richiesta dell'utente 
            - recuperare informazioni da Eventbrite API se ti viene passato un URL

            Dopo l'elaborazione, l'utente potrà farti domande su:
            - struttura del file HTML
            - informazioni principali relative al contenuto del file e all'evento
        """

        response = chat_functions(
            user_message=initial_prompt,
            functions=FUNCTIONS,
            function_call="auto"
        )
        message = gpt_choice_message(response)
        self.chat_history.append(message)

        self._handle_functions(message)

    @staticmethod
    def print_event(event):
        logger.info("\n---------------------------")

        logger.info(f"Titolo: {event.title}")
        logger.info(f"Data: {event.date}")
        logger.info(f"URL: {event.url}")
        logger.info(f"Location: {event.location.name}, {event.location.address}")
        logger.info(f"Categoria: {', '.join(event.categories)}")
        logger.info(
            f"Description: {event.description[:150]}..." if event.description else "No description"
        )

        logger.info("---------------------------\n")

    def _handle_functions(self, message):
        while message.get("function_call"):
            fname = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])

            if fname in FUNCTION_DISPATCHER:
                logger.info(f"⚙️  Eseguo funzione: {fname} con args: {args}")
                result = FUNCTION_DISPATCHER[fname](**args)

                function_response = {
                    "role": "function",
                    "name": fname,
                    "content": json.dumps(result)
                }
                self.chat_history.append(function_response)

                response = chat_functions(
                    messages=self.chat_history,
                    functions=FUNCTIONS,
                    function_call="auto"
                )
                message = gpt_choice_message(response)
                self.chat_history.append(message)
            else:
                logger.warning(f"❌ Funzione non gestita: {fname}")
                break

    def fetch_event(self, url: str):
        """Fetch single event by URL"""
        try:
            event = fetch_event_from_url(url)
            self.chat_history.append({"role": "system", "content": f"Fetched event {event.title}"})
            self.print_event(event)
        except Exception as e:
            logger.error(f"Errore nel fetch dell'evento: {e}")

    def search_events(self, query: str, location: str = "Torino"):
        """Search events by query"""
        try:
            events = list_events_by_query(query, location)
            for event in events:
                self.print_event(event)
        except Exception as e:
            logger.error(f"Errore nella ricerca eventi: {e}")

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        response = chat_functions(
            messages=self.chat_history,
            functions=FUNCTIONS,
            function_call="auto"
        )
        message = gpt_choice_message(response)
        self.chat_history.append(message)

        if message.get("function_call"):
            self._handle_functions(message)
        else:
            logger.info("🗨️ %s", message.get("content"))


def run_eventbrite_agent():
    agent = EventbriteAgent()
    while True:
        user_input = input("❓ Inserisci URL evento o 'exit' per uscire: ")
        if user_input.lower() == "exit":
            break
        agent.fetch_event(user_input)
