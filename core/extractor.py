import re


class AnswerExtractor:

    def __init__(self):
        pass

    def get_spoken_material(self, text: str) -> str:

        if not text or not text.strip():

            return "I am sorry, I got no response."

        # Remove markdown
        clean_text = re.sub(r"[*#`_~|]", "", text)

        # Normalize spaces
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        if not clean_text:

            return "I am sorry, I got no response."

        # First sentence
        sentences = re.split(r"(?<=[.!?])\s+", clean_text)

        spoken = sentences[0].strip() if sentences else clean_text

        # Limit speech length
        if len(spoken) > 150:

            spoken = spoken[:150].rsplit(" ", 1)[0] + "."

        return spoken
