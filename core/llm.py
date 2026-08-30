import logging
import os
import random

from groq import Groq

from core.task_planner import TaskPlanner


class AIEngine:

    def __init__(self):

        # =================================================
        # API KEY
        # =================================================

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:

            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:

            raise ValueError("GROQ_API_KEY or OPENAI_API_KEY is missing.")

        # =================================================
        # GROQ
        # =================================================

        self.client = Groq(api_key=api_key)

        # =================================================
        # NORMAL CHAT PROMPT
        # =================================================

        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Anni, a helpful voice assistant. "
                "Answer directly and concisely. "
                "Use one or two plain English sentences. "
                "Do not use markdown, tables, bullets, "
                "or special formatting."
            ),
        }

        self.chat_history = [self.system_prompt]

        # =================================================
        # TASK PLANNER
        # =================================================

        self.task_planner = TaskPlanner(self.client)

    # =====================================================
    # NORMAL CHAT
    # =====================================================

    def chat(self, query: str) -> str:

        if not query or not query.strip():

            return "I did not hear your question."

        self.chat_history.append({"role": "user", "content": query.strip()})

        try:

            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=self.chat_history,
                temperature=0.3,
                max_completion_tokens=512,
                reasoning_effort="low",
                include_reasoning=False,
                stream=False,
            )

            if not response.choices:

                raise RuntimeError("Groq returned no choices.")

            answer = response.choices[0].message.content

            if not answer:

                raise RuntimeError("Groq returned empty content.")

            answer = answer.strip()

            self.chat_history.append({"role": "assistant", "content": answer})

            return answer

        except Exception as e:

            logging.error(f"LLM Chat Error: {e}")

            if self.chat_history and self.chat_history[-1].get("role") == "user":

                self.chat_history.pop()

            return "I am sorry, there was an API error."

    # =====================================================
    # TASK PLAN
    # =====================================================

    def create_task_plan(self, command: str) -> dict:

        return self.task_planner.create_plan(command)

    # =====================================================
    # RESET CHAT
    # =====================================================

    def reset_chat(self):

        self.chat_history = [self.system_prompt]

    # =====================================================
    # SAVE PROMPT
    # =====================================================

    def save_ai_prompt(self, prompt: str) -> str:

        if not prompt or not prompt.strip():

            return "The prompt is empty."

        try:

            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=0.7,
                max_completion_tokens=1024,
                reasoning_effort="low",
                include_reasoning=False,
                stream=False,
            )

            if not response.choices:

                return "Could not generate content."

            answer = response.choices[0].message.content

            if not answer:

                return "Could not generate content."

            os.makedirs("Openai", exist_ok=True)

            filename = "Openai/" f"prompt_{random.randint(1000, 9999)}.txt"

            with open(filename, "w", encoding="utf-8") as file:

                file.write(f"Prompt: {prompt}\n\n" f"{answer}")

            return "File saved."

        except Exception as e:

            logging.error(f"AI Saving Error: {e}")

            return "Could not write file."
