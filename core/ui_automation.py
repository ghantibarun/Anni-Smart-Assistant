import ctypes
import logging
import time
import urllib.parse
import webbrowser

import pyautogui
from pywinauto import Desktop


class WindowsUIAutomation:

    def __init__(self):

        pyautogui.PAUSE = 0.15

        # Emergency:
        # Move mouse to top-left corner to stop PyAutoGUI.
        pyautogui.FAILSAFE = True

    # =====================================================
    # GET FOREGROUND WINDOW
    # =====================================================

    def get_foreground_window(self):

        try:

            hwnd = ctypes.windll.user32.GetForegroundWindow()

            if hwnd == 0:

                return None

            desktop = Desktop(backend="uia")

            return desktop.window(handle=hwnd)

        except Exception as e:

            logging.error(f"Could not get foreground window: {e}")

            return None

    # =====================================================
    # FOCUS APPLICATION
    # =====================================================

    def focus_application(self, app_name: str) -> bool:

        if not app_name:
            return False

        requested = app_name.strip().lower()

        try:

            desktop = Desktop(backend="uia")

            windows = desktop.windows(visible_only=True)

            best_window = None

            best_title = ""

            # ---------------------------------------------
            # Prefer window containing app name
            # ---------------------------------------------

            for window in windows:

                try:

                    title = window.window_text().strip()

                    if not title:
                        continue

                    if requested in title.lower():

                        best_window = window
                        best_title = title

                        break

                except Exception:
                    continue

            if best_window is None:
                return False

            try:

                best_window.restore()

            except Exception:
                pass

            best_window.set_focus()

            time.sleep(0.5)

            logging.info(f"Focused: {best_title}")

            return True

        except Exception as e:

            logging.error(f"Could not focus {app_name}: {e}")

            return False

    # =====================================================
    # TYPE TEXT
    # =====================================================

    def type_text(self, text) -> bool:

        if text is None:
            return False

        try:

            pyautogui.write(str(text), interval=0.02)

            return True

        except Exception as e:

            logging.error(f"Typing failed: {e}")

            return False

    # =====================================================
    # PRESS KEY
    # =====================================================

    def press_key(self, key: str) -> bool:

        if not key:
            return False

        key = key.strip().lower()

        aliases = {
            "escape": "esc",
            "return": "enter",
            "spacebar": "space",
            "page up": "pageup",
            "page down": "pagedown",
        }

        key = aliases.get(key, key)

        allowed = {
            "enter",
            "esc",
            "tab",
            "space",
            "backspace",
            "delete",
            "insert",
            "home",
            "end",
            "up",
            "down",
            "left",
            "right",
            "pageup",
            "pagedown",
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f7",
            "f8",
            "f9",
            "f10",
            "f11",
            "f12",
        }

        if key not in allowed:
            return False

        pyautogui.press(key)

        return True

    # =====================================================
    # HOTKEY
    # =====================================================

    def hotkey(self, keys) -> bool:

        if not keys:
            return False

        if isinstance(keys, str):

            keys = keys.replace("+", " ").split()

        keys = [str(key).strip().lower() for key in keys]

        allowed = {
            "ctrl",
            "shift",
            "alt",
            "win",
            "enter",
            "esc",
            "tab",
            "space",
            "a",
            "c",
            "v",
            "x",
            "z",
            "s",
            "f",
            "t",
            "w",
            "n",
            "l",
            "r",
            "p",
            "d",
            "k",
            "q",
        }

        if any(key not in allowed for key in keys):
            return False

        pyautogui.hotkey(*keys)

        return True

    # =====================================================
    # CLICK COORDINATES
    # =====================================================

    def click(self, x, y) -> bool:

        if x is None or y is None:
            return False

        pyautogui.click(int(x), int(y))

        return True

    # =====================================================
    # CLICK CONTROL BY NAME
    # =====================================================

    def click_control(self, control_name: str) -> bool:

        if not control_name:
            return False

        target = control_name.strip().lower()

        window = self.get_foreground_window()

        if window is None:
            return False

        try:

            controls = window.descendants()

            # Exact match first
            for control in controls:

                try:

                    text = control.window_text().strip()

                    if text.lower() == target:

                        control.click_input()

                        return True

                except Exception:
                    continue

            # Partial match second
            for control in controls:

                try:

                    text = control.window_text().strip()

                    if target in text.lower():

                        control.click_input()

                        return True

                except Exception:
                    continue

        except Exception as e:

            logging.error(f"Click control failed: {e}")

        return False

    # =====================================================
    # WAIT
    # =====================================================

    def wait(self, seconds=1) -> bool:

        try:

            seconds = float(seconds)

        except Exception:

            seconds = 1

        seconds = max(0.1, min(seconds, 10))

        time.sleep(seconds)

        return True

    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        return self.hotkey(["ctrl", "s"])

    # =====================================================
    # COPY
    # =====================================================

    def copy(self):

        return self.hotkey(["ctrl", "c"])

    # =====================================================
    # PASTE
    # =====================================================

    def paste(self):

        return self.hotkey(["ctrl", "v"])

    # =====================================================
    # SELECT ALL
    # =====================================================

    def select_all(self):

        return self.hotkey(["ctrl", "a"])

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        return self.hotkey(["alt", "f4"])

    # =====================================================
    # MINIMIZE
    # =====================================================

    def minimize(self):

        return self.hotkey(["win", "down"])

    # =====================================================
    # MAXIMIZE
    # =====================================================

    def maximize(self):

        return self.hotkey(["win", "up"])

    # =====================================================
    # BROWSER SEARCH
    # =====================================================

    def browser_search(self, text: str) -> bool:

        if not text:
            return False

        encoded = urllib.parse.quote_plus(text)

        url = "https://www.google.com/search?q=" + encoded

        webbrowser.open(url)

        return True

    # =====================================================
    # SEARCH CURRENT BROWSER
    # =====================================================

    def current_browser_search(self, text: str) -> bool:

        if not text:
            return False

        self.hotkey(["ctrl", "l"])

        time.sleep(0.3)

        self.type_text(text)

        self.press_key("enter")

        return True
