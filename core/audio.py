import logging
import time

import pyttsx3
import speech_recognition as sr


class AudioEngine:

    def __init__(self):

        # =================================================
        # SPEECH RECOGNITION
        # =================================================

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

        # Wait a little longer for complete commands
        self.recognizer.pause_threshold = 1.2

        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        # Maximum length of one spoken command
        self.phrase_time_limit = 20

        # =================================================
        # MICROPHONE
        # =================================================

        try:

            self.microphone = sr.Microphone()

        except Exception as e:

            logging.critical(f"Microphone initialization failed: {e}")

            raise

        # =================================================
        # MICROPHONE CALIBRATION
        # =================================================

        try:

            with self.microphone as source:

                self.recognizer.adjust_for_ambient_noise(source, duration=1)

        except Exception as e:

            logging.warning(f"Microphone calibration warning: {e}")

    # =====================================================
    # CREATE TTS ENGINE
    # =====================================================

    def create_tts_engine(self):

        engine = pyttsx3.init("sapi5")

        engine.setProperty("rate", 170)

        engine.setProperty("volume", 1.0)

        # -----------------------------------------
        # Select a suitable voice
        # -----------------------------------------

        try:

            voices = engine.getProperty("voices")

            if voices:

                selected_voice = None

                for voice in voices:

                    name = str(getattr(voice, "name", "")).lower()

                    if "zira" in name or "female" in name:

                        selected_voice = voice.id
                        break

                if selected_voice is None:

                    selected_voice = voices[0].id

                engine.setProperty("voice", selected_voice)

        except Exception as e:

            logging.warning(f"Voice selection warning: {e}")

        return engine

    # =====================================================
    # SPEAK
    # =====================================================

    def speak(self, text: str):

        if text is None:
            return

        text = str(text).strip()

        if not text:
            return

        # Show response in terminal
        logging.info(f"Anni: {text}")

        engine = None

        try:

            # -----------------------------------------
            # Create a NEW TTS engine every time
            # -----------------------------------------

            engine = self.create_tts_engine()

            engine.say(text)

            engine.runAndWait()

            # Make sure Windows releases the speech queue
            engine.stop()

            # Small pause before microphone starts again
            time.sleep(0.2)

        except Exception as e:

            logging.error(f"TTS error: {e}")

        finally:

            # Explicit cleanup
            try:

                if engine is not None:

                    engine.stop()

            except Exception:
                pass

            engine = None

    # =====================================================
    # LISTEN
    # =====================================================

    def listen(self) -> str:

        try:

            with self.microphone as source:

                logging.info("Listening...")

                audio = self.recognizer.listen(
                    source, timeout=8, phrase_time_limit=self.phrase_time_limit
                )

        except sr.WaitTimeoutError:

            return ""

        except Exception as e:

            logging.error(f"Listening error: {e}")

            return ""

        try:

            text = self.recognizer.recognize_google(audio)

            text = text.strip()

            if text:

                logging.info(f"User said: {text}")

            return text

        except sr.UnknownValueError:

            return ""

        except sr.RequestError as e:

            logging.error(f"Speech recognition service error: {e}")

            return ""

        except Exception as e:

            logging.error(f"Speech recognition error: {e}")

            return ""
