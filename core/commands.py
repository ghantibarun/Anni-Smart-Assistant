import logging

from core.app_launcher import WindowsAppLauncher
from core.ui_automation import WindowsUIAutomation


class CommandHandler:

    def __init__(self, llm):

        self.llm = llm

        self.launcher = WindowsAppLauncher()

        self.ui = WindowsUIAutomation()

        # =================================================
        # MOST RECENTLY OPENED APPLICATION
        # =================================================

        self.current_app = None

    # =====================================================
    # CURRENT APPLICATION
    # =====================================================

    def get_current_app(self):

        return self.current_app

    # =====================================================
    # OPEN APPLICATION
    # =====================================================

    def open_application(self, app_name: str) -> str:

        if not app_name:

            return "I could not identify the application."

        logging.info(f"Anni task: opening {app_name}")

        success = self.launcher.open_app(app_name)

        if not success:

            return f"Sorry, I could not find or open {app_name}."

        # -----------------------------------------
        # Remember this as current application
        # -----------------------------------------

        self.current_app = app_name

        # Wait for startup
        self.ui.wait(2)

        # Focus application
        self.ui.focus_application(app_name)

        self.ui.wait(0.5)

        return f"Opening {app_name} sir."

    # =====================================================
    # EXECUTE ONE ACTION
    # =====================================================

    def execute_action(self, action: dict) -> bool:

        action_type = action.get("type")

        try:

            # -----------------------------------------
            # TYPE
            # -----------------------------------------

            if action_type == "type":

                return self.ui.type_text(action.get("text"))

            # -----------------------------------------
            # PRESS
            # -----------------------------------------

            if action_type == "press":

                return self.ui.press_key(action.get("key"))

            # -----------------------------------------
            # HOTKEY
            # -----------------------------------------

            if action_type == "hotkey":

                return self.ui.hotkey(action.get("keys"))

            # -----------------------------------------
            # CLICK
            # -----------------------------------------

            if action_type == "click":

                control = action.get("control")

                if control:

                    return self.ui.click_control(control)

                x = action.get("x")

                y = action.get("y")

                if x is not None and y is not None:

                    return self.ui.click(x, y)

                return False

            # -----------------------------------------
            # WAIT
            # -----------------------------------------

            if action_type == "wait":

                return self.ui.wait(action.get("seconds") or 1)

            # -----------------------------------------
            # SAVE
            # -----------------------------------------

            if action_type == "save":

                return self.ui.save()

            # -----------------------------------------
            # COPY
            # -----------------------------------------

            if action_type == "copy":

                return self.ui.copy()

            # -----------------------------------------
            # PASTE
            # -----------------------------------------

            if action_type == "paste":

                return self.ui.paste()

            # -----------------------------------------
            # SELECT ALL
            # -----------------------------------------

            if action_type == "select_all":

                return self.ui.select_all()

            # -----------------------------------------
            # CLOSE
            # -----------------------------------------

            if action_type == "close":

                success = self.ui.close()

                if success:

                    self.current_app = None

                return success

            # -----------------------------------------
            # MINIMIZE
            # -----------------------------------------

            if action_type == "minimize":

                return self.ui.minimize()

            # -----------------------------------------
            # MAXIMIZE
            # -----------------------------------------

            if action_type == "maximize":

                return self.ui.maximize()

            # -----------------------------------------
            # BROWSER SEARCH
            # -----------------------------------------

            if action_type == "browser_search":

                return self.ui.browser_search(action.get("text"))

            # -----------------------------------------
            # CURRENT BROWSER SEARCH
            # -----------------------------------------

            if action_type == "current_browser_search":

                return self.ui.current_browser_search(action.get("text"))

            logging.warning(f"Unknown action: {action_type}")

            return False

        except Exception as e:

            logging.error(f"Action execution error: {e}")

            return False

    # =====================================================
    # EXECUTE COMPLETE TASK
    # =====================================================

    def execute_task(self, command: str) -> str:

        plan = self.llm.create_task_plan(command)

        app = plan.get("app")

        actions = plan.get("actions", [])

        # =================================================
        # EXPLICIT APPLICATION
        # =================================================

        if app:

            response = self.open_application(app)

            # -----------------------------------------
            # Only opening app
            # -----------------------------------------

            if not actions:

                return response

        # =================================================
        # NO APP = USE RECENT APP
        # =================================================

        else:

            if not actions:

                return None

            # -----------------------------------------
            # No recently opened application
            # -----------------------------------------

            if not self.current_app:

                return "Please open an application first."

            # -----------------------------------------
            # Focus recently opened application
            # -----------------------------------------

            focused = self.ui.focus_application(self.current_app)

            if not focused:

                logging.warning(f"Could not focus current app: " f"{self.current_app}")

        # =================================================
        # EXECUTE ACTIONS
        # =================================================

        completed = 0

        for action in actions:

            action_type = action.get("type")

            logging.info(f"Executing: {action_type}")

            success = self.execute_action(action)

            if not success:

                logging.warning(f"Action failed: {action}")

                return "I could not complete the requested action."

            completed += 1

            self.ui.wait(0.3)

        # =================================================
        # RESPONSE
        # =================================================

        if app and actions:

            return f"I opened {app} and completed " f"the requested task."

        return "Done sir."

    # =====================================================
    # TASK DETECTION
    # =====================================================

    def looks_like_task(self, query: str) -> bool:

        text = query.lower().strip()

        task_phrases = [
            "open ",
            "launch ",
            "start ",
            "type ",
            "write ",
            "enter ",
            "put ",
            "press ",
            "click ",
            "save",
            "copy",
            "paste",
            "select all",
            "close",
            "minimize",
            "maximize",
            "search ",
            "search for ",
            "google ",
            "look up ",
            "play ",
            "and type",
            "and press",
            "and click",
            "and save",
            "and search",
            "in chrome",
            "in edge",
            "in spotify",
            "on chrome",
            "on edge",
            "on spotify",
        ]

        return any(phrase in text for phrase in task_phrases)

    # =====================================================
    # PROCESS COMMAND
    # =====================================================

    def process_system_command(self, query: str) -> str | None:

        if not query:

            return None

        if not self.looks_like_task(query):

            return None

        return self.execute_task(query)
