import json
import logging


class TaskPlanner:

    def __init__(self, client):

        self.client = client

    # =====================================================
    # CREATE PLAN
    # =====================================================

    def create_plan(self, command: str) -> dict:

        schema = {
            "name": "windows_task",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "app": {"type": ["string", "null"]},
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        "type",
                                        "press",
                                        "hotkey",
                                        "click",
                                        "wait",
                                        "save",
                                        "copy",
                                        "paste",
                                        "select_all",
                                        "close",
                                        "minimize",
                                        "maximize",
                                        "browser_search",
                                        "current_browser_search",
                                    ],
                                },
                                "text": {"type": ["string", "null"]},
                                "key": {"type": ["string", "null"]},
                                "keys": {
                                    "type": ["array", "null"],
                                    "items": {"type": "string"},
                                },
                                "control": {"type": ["string", "null"]},
                                "x": {"type": ["integer", "null"]},
                                "y": {"type": ["integer", "null"]},
                                "seconds": {"type": ["number", "null"]},
                            },
                            "required": [
                                "type",
                                "text",
                                "key",
                                "keys",
                                "control",
                                "x",
                                "y",
                                "seconds",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["app", "actions"],
                "additionalProperties": False,
            },
        }

        system_prompt = """
You are Anni, a Windows desktop task planner.

Convert the user's command into a structured desktop task.

APPLICATION RULES:

1. If the user explicitly says to open, launch, or start
   an application, put that application name in "app".

2. If the user does NOT mention an application, set "app" to null.

3. When "app" is null, the action will be executed on the
   most recently opened application.

4. NEVER create an action with type "open".

5. Opening an application is controlled by the "app" field.

ACTION RULES:

6. Use "type" when the user wants text entered.

7. Use "press" for a single keyboard key.

8. Use "hotkey" for keyboard shortcuts.

9. Use "click" for a visible control or explicit coordinates.

10. Use "wait" when an application needs time to load.

11. Use "save" for saving.

12. Use "copy" for copying.

13. Use "paste" for pasting.

14. Use "select_all" for selecting everything.

15. Use "close" to close the current application.

16. Use "minimize" to minimize the current window.

17. Use "maximize" to maximize the current window.

BROWSER:

18. For a web search use "browser_search" when opening
    Google is appropriate.

19. If Chrome, Edge, or another browser is explicitly being
    opened and then searched, use "current_browser_search".

20. Example:
    "Open Chrome and search NIT Raipur"

    app = "Chrome"

    action:
    current_browser_search
    text = "NIT Raipur"

CURRENT APPLICATION:

21. If the user says:
    "Type Hello"

    app = null
    action = type
    text = "Hello"

22. If the user says:
    "Press Enter"

    app = null
    action = press
    key = "enter"

23. If the user says:
    "Save"

    app = null
    action = save

24. If the user says:
    "Close"

    app = null
    action = close

25. If the user says:
    "Select all and copy"

    app = null

    actions:
    select_all
    copy

IMPORTANT:

26. Keep actions in exact order.

27. Do not invent application-specific actions.

28. Do not create shell commands.

29. Do not create PowerShell commands.

30. Do not install software.

31. Do not delete files.

32. Do not send emails or messages.

33. Do not make purchases.

34. Do not use browser search for a normal application action.

35. If a task cannot be represented using the available generic
    actions, return the closest safe generic action rather than
    inventing an unsupported action.
"""

        try:

            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command},
                ],
                temperature=0,
                max_completion_tokens=700,
                reasoning_effort="low",
                include_reasoning=False,
                response_format={"type": "json_schema", "json_schema": schema},
            )

            if not response.choices:

                raise RuntimeError("Groq returned no choices.")

            content = response.choices[0].message.content

            if not content:

                raise RuntimeError("Groq returned empty task plan.")

            plan = json.loads(content)

            return plan

        except Exception as e:

            logging.error(f"Task planning failed: {e}")

            return {"app": None, "actions": []}
