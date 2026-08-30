import json
import logging
import platform
import subprocess
import time


class WindowsAppLauncher:

    def __init__(self):

        if platform.system() != "Windows":

            raise RuntimeError("WindowsAppLauncher requires Windows.")

    # =====================================================
    # GET WINDOWS START APPS
    # =====================================================

    def get_start_apps(self):

        command = "Get-StartApps | " "ConvertTo-Json -Compress"

        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:

            raise RuntimeError(result.stderr.strip())

        output = result.stdout.strip()

        if not output:

            return []

        apps = json.loads(output)

        if isinstance(apps, dict):

            apps = [apps]

        return apps

    # =====================================================
    # FIND APP
    # =====================================================

    def find_app(self, app_name: str):

        if not app_name:
            return None

        requested = app_name.strip().lower()

        apps = self.get_start_apps()

        # -------------------------------------------------
        # Exact match
        # -------------------------------------------------

        for app in apps:

            name = str(app.get("Name", "")).strip()

            if name.lower() == requested:

                return app

        # -------------------------------------------------
        # Starts with
        # -------------------------------------------------

        for app in apps:

            name = str(app.get("Name", "")).strip()

            if name.lower().startswith(requested):

                return app

        # -------------------------------------------------
        # Contains
        # -------------------------------------------------

        for app in apps:

            name = str(app.get("Name", "")).strip()

            if requested in name.lower():

                return app

        return None

    # =====================================================
    # OPEN APP
    # =====================================================

    def open_app(self, app_name: str) -> bool:

        try:

            app = self.find_app(app_name)

            if not app:

                logging.warning(f"Application not found: {app_name}")

                return False

            app_id = app.get("AppID")

            if not app_id:

                return False

            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])

            time.sleep(2)

            logging.info(f"Opened application: {app.get('Name')}")

            return True

        except Exception as e:

            logging.error(f"Could not open {app_name}: {e}")

            return False
