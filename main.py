import logging
from dotenv import load_dotenv

from core.audio import AudioEngine
from core.llm import AIEngine
from core.commands import CommandHandler
from core.extractor import AnswerExtractor

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Hide HTTP request logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


# =====================================================
# MAIN
# =====================================================


def main():

    load_dotenv()

    try:
        audio = AudioEngine()
        llm = AIEngine()

        # CommandHandler remembers the current application
        commander = CommandHandler(llm)

        extractor = AnswerExtractor()

    except Exception as e:

        logging.critical(f"Failed to initialize Anni: {e}")

        return

    # -------------------------------------------------
    # Startup
    # -------------------------------------------------

    audio.speak("Hello Sir, Anni is online and ready for listening....")

    # -------------------------------------------------
    # Main loop
    # -------------------------------------------------

    while True:

        query = audio.listen()

        if not query:
            continue

        query_lower = query.lower().strip()

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        if any(
            word in query_lower.split() for word in ("exit", "quit", "stop", "sleep")
        ):

            audio.speak("Thank you and Goodbye sir.")

            break

        # -------------------------------------------------
        # RESET CHAT
        # -------------------------------------------------

        if "reset chat" in query_lower:

            llm.reset_chat()

            audio.speak("Chat history cleared.")

            continue

        # -------------------------------------------------
        # SAVE AI PROMPT
        # -------------------------------------------------

        if "using ai" in query_lower:

            audio.speak("Processing.")

            response = llm.save_ai_prompt(query)

            audio.speak(response)

            continue

        # -------------------------------------------------
        # DESKTOP TASK
        # -------------------------------------------------

        if commander.looks_like_task(query):

            response = commander.process_system_command(query)

            if response:

                audio.speak(response)

                continue

        # -------------------------------------------------
        # NORMAL AI QUESTION
        # -------------------------------------------------

        full_response = llm.chat(query)

        short_response = extractor.get_spoken_material(full_response)

        audio.speak(short_response)


if __name__ == "__main__":
    main()
