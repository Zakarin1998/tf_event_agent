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
    parse_html_file,
    fetch_event_from_url,
    list_events_by_query,
    search_events,
    search_flights,
    search_hotels,
    get_weather_forecast
)

logger = logging.getLogger(__name__)

FUNCTION_DISPATCHER = {
    # "parse_html_file": parse_html_file,
    # "write_file": write_file,
    # "read_file": read_file,
    # "load_json": load_json,
    # "write_json": write_json,
    # "fetch_event_from_url": fetch_event_from_url,
    # "list_events_by_query": list_events_by_query,
    # new functions
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "search_events": search_events,
    "get_weather_forecast": get_weather_forecast
}


class EventbriteAgent:
    def __init__(self):
        self.chat_history = []
        logger.info("🤖 Avvio di Eventbrite Agent...")

        initial_prompt = """
            Sei un assistente viaggi intelligente.
            Il tuo compito è:
                - proporre soluzioni di trasporto (voli, treni, autobus) per la tratta richiesta dall'utente
                - proporre alloggi disponibili nelle date indicate
                - mostrare previsioni del tempo per le date e la destinazione
                - suggerire eventi, attrazioni o attività interessanti nella città
            Rispondi in maniera chiara e sintetica, in italiano.
        """

        response = chat_functions(
            user_message=initial_prompt,
            functions=FUNCTIONS,
            function_call="auto"
        )
        message = gpt_choice_message(response)
        self.chat_history.append(message)

        self._handle_functions(message)

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
        # ritorna SEMPRE l’ultimo message (anche se è content)
        return message

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
            message = self._handle_functions(message)
            logger.info("⚙️🗨️ %s", message.get("content"))
        else:
            logger.info("🗨️ %s", message.get("content"))


def run_eventbrite_agent():
    agent = EventbriteAgent()
    while True:
        user_input = input("❓ Inserisci URL evento o 'exit' per uscire: ")
        if user_input.lower() == "exit":
            break
        agent.ask(user_input)
