# Anni Smart Assistant AI 🤖

Anni Smart Assistant AI is a Python-based voice-controlled desktop assistant designed to interact with Windows applications using natural-language commands.

Anni combines **speech recognition, text-to-speech, Groq AI, Windows application discovery, and GUI automation** to provide a hands-free desktop assistant experience.

## ✨ Features

### 🎙️ Voice Interaction

* Converts speech into text using SpeechRecognition.
* Responds using Windows SAPI5 text-to-speech through `pyttsx3`.
* Supports continuous conversation through a listen → process → speak loop.

### 🧠 AI-Powered Conversation

* Uses Groq's `openai/gpt-oss-20b` model.
* Answers general questions naturally.
* Maintains conversation history.
* Supports resetting the conversation with a voice command.

### 🖥️ Dynamic Windows Application Launching

Anni can dynamically search Windows Start Apps and open applications without maintaining a hard-coded list.

Examples:

```text
Open Notepad
Open Chrome
Open Microsoft Word
Open Excel
Open PowerPoint
Open Spotify
Open WhatsApp
Open Telegram
Open Discord
Open VLC
Open PyCharm
Open Eclipse
Open Calculator
```

Applications are discovered from Windows rather than being restricted to a fixed set of programs.

### 🎯 Current Application Memory

Anni remembers the most recently opened application.

Example:

```text
User: Open Notepad
Anni: Opening Notepad sir.

User: Type Hello Sir
Anni: Done sir.

User: Press Enter
Anni: Done sir.

User: Type This is Anni AI
Anni: Done sir.

User: Save
Anni: Done sir.
```

When another application is opened, it becomes the new current application:

```text
User: Open Excel
Anni: Opening Excel sir.

User: Type Name
Anni: Done sir.
```

This means you do not need to repeat the application name for every command.

### 🖱️ Windows Automation

Anni can perform generic desktop actions on the currently active application, including:

* Type text
* Press keyboard keys
* Keyboard shortcuts
* Click visible UI controls
* Mouse-coordinate clicks
* Save
* Copy
* Paste
* Select all
* Close
* Minimize
* Maximize
* Wait for application startup

The project uses `pywinauto` for Windows UI Automation and `PyAutoGUI` for keyboard and mouse automation.

### 🌐 Browser Search

Anni can open a browser and perform searches.

Examples:

```text
Search for NIT Raipur
Search Python tutorials
Google machine learning
Look up Mininet SDN
```

It can also handle commands such as:

```text
Open Chrome and search NIT Raipur
```

### 📋 Multi-Step Commands

Anni can convert natural-language instructions into structured actions.

Example:

```text
Open Notepad and type Hello Sir
```

or:

```text
Open Notepad, type Hello Sir, press Enter, type This is Anni
```

The AI task planner converts the request into executable actions and executes them in order.

---

# 🏗️ Project Architecture

```text
                         ANNI SMART ASSISTANT
                                  │
                           Voice Recognition
                                  │
                           Natural Language
                                  │
                         ┌────────┴─────────┐
                         │                  │
                    Desktop Task        Normal Question
                         │                  │
                         ↓                  ↓
                   Task Planner           Groq AI
                         │
                  ┌──────┴──────┐
                  │             │
             App Launcher   UI Automation
                  │             │
                  ↓             ↓
           Windows Start Apps   Keyboard
                                Mouse
                                UI Controls
                                  │
                                  ↓
                          Current Application
```

---

# 📁 Project Structure

```text
Anni-Smart-Assistant/
│
├── main.py
├── config.json
├── README.md
│
└── core/
    ├── __init__.py
    ├── audio.py
    ├── llm.py
    ├── task_planner.py
    ├── commands.py
    ├── app_launcher.py
    ├── ui_automation.py
    └── extractor.py
```

## 📌 File Description

| File               | Purpose                                                            |
| ------------------ | ------------------------------------------------------------------ |
| `main.py`          | Main application loop and command routing                          |
| `audio.py`         | Speech recognition and text-to-speech                              |
| `llm.py`           | Groq AI communication and conversation history                     |
| `task_planner.py`  | Converts natural-language desktop commands into structured actions |
| `commands.py`      | Executes desktop tasks and remembers the current application       |
| `app_launcher.py`  | Dynamically finds and launches Windows applications                |
| `ui_automation.py` | Performs keyboard, mouse, and Windows UI automation                |
| `extractor.py`     | Cleans AI responses before they are spoken                         |
| `config.json`      | Optional website configuration                               |

---

# ⚙️ Requirements

* Windows 10 or Windows 11
* Python 3.10+
* Working microphone
* Working speakers/headphones
* Internet connection
* Groq API key

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/ghantibarun/Anni-Smart-Assistant
```

Move into the project directory:

```bash
cd Anni-Smart-Assistant
```

## 2. Create a virtual environment

```powershell
py -3.10 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
python -m pip install -U pip
```

Then:

```powershell
python -m pip install -U groq pyautogui pywinauto python-dotenv SpeechRecognition pyttsx3 PyAudio
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The application also supports:

```env
OPENAI_API_KEY=your_groq_api_key
```

when using the existing project configuration.

Never commit your API key to GitHub.

Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
Openai/
```

---

# ▶️ Running Anni

You can run the assistant using:

```powershell
python main.py
```

or, if your project contains a Makefile:

```powershell
make run
```

When successful, Anni starts with:

```text
Anni: Hello Sir, Anni is online and ready for listening.
```

---

# 🎤 Example Commands

## General Questions

```text
What is the capital of India?
```

```text
Who invented the computer?
```

```text
Explain binary search.
```

These are handled by Groq AI.

---

## Open Windows Applications

```text
Open Notepad
```

```text
Open Chrome
```

```text
Open Excel
```

```text
Open Word
```

```text
Open Spotify
```

```text
Open WhatsApp
```

```text
Open Calculator
```

Applications are searched dynamically through Windows Start Apps.

---

## Work on the Current Application

After:

```text
Open Notepad
```

you can say:

```text
Type Hello Sir
```

```text
Press Enter
```

```text
Type Anni Smart Assistant
```

```text
Select all
```

```text
Copy
```

```text
Paste
```

```text
Save
```

```text
Close
```

Anni remembers that Notepad was the most recently opened application.

---

## Switch Applications

```text
Open Excel
```

Then:

```text
Type Name
```

Then:

```text
Press Tab
```

Then:

```text
Type Barun
```

The commands are directed to Excel because it is now the current application.

---

# 🌐 Browser Commands

```text
Open Chrome
```

Then:

```text
Search NIT Raipur
```

Or directly:

```text
Open Chrome and search NIT Raipur
```

Other examples:

```text
Search Python machine learning
```

```text
Google Dijkstra algorithm
```

```text
Search for Mininet SDN
```

---

# 🧩 Multi-Step Tasks

Anni can process multiple actions in one request.

Example:

```text
Open Notepad and type Hello Sir
```

The planner can interpret it as:

```text
1. Open Notepad
2. Focus Notepad
3. Type "Hello Sir"
```

Another example:

```text
Open Chrome and search NIT Raipur
```

The planner can interpret it as:

```text
1. Open Chrome
2. Focus Chrome
3. Open the address/search area
4. Search for "NIT Raipur"
```

---

# 🧠 How Task Planning Works

Anni does not use a separate hard-coded handler for every application.

Instead:

```text
User Command
     ↓
Groq Task Planner
     ↓
Structured JSON Action Plan
     ↓
Command Handler
     ↓
Windows UI Automation
     ↓
Current Application
```

For example:

```text
"Type Hello Sir"
```

can become:

```json
{
  "app": null,
  "actions": [
    {
      "type": "type",
      "text": "Hello Sir"
    }
  ]
}
```

When `app` is `null`, Anni uses the most recently opened application.

---

# 🔄 Current Application Model

Anni maintains:

```python
current_app
```

Example:

```text
Open Notepad
      ↓
current_app = "Notepad"
```

Then:

```text
Type Hello
```

is executed against Notepad.

When the user says:

```text
Open Excel
```

the state changes:

```text
current_app = "Excel"
```

The following command:

```text
Type Name
```

is executed against Excel.

---

# 🛡️ Safety

The task planner is intentionally restricted from generating arbitrary shell or PowerShell commands.

The planner is instructed not to:

* Execute arbitrary shell commands
* Execute PowerShell commands
* Install software
* Delete files
* Make purchases
* Send messages automatically

The automation layer is intended for controlled desktop actions such as typing, keyboard shortcuts, clicking controls, and application navigation.

For destructive or externally consequential operations, confirmation should be added before execution.

---

# 🐛 Troubleshooting

## Groq import error

Run:

```powershell
py -3.10 -m pip install -U groq
```

Check:

```powershell
python -c "import groq; print(groq.__version__)"
```

---

## PyAutoGUI import error

```powershell
py -3.10 -m pip install -U pyautogui
```

---

## Pywinauto import error

```powershell
py -3.10 -m pip install -U pywinauto
```

---

## PyAudio installation problem

SpeechRecognition requires an audio backend.

Try:

```powershell
py -3.10 -m pip install PyAudio
```

---

## Anni hears only part of a long command

The speech recognizer uses:

```python
pause_threshold
phrase_time_limit
```

inside `core/audio.py`.

Increase the phrase time limit if necessary.

---

## Application opens but action is not performed

Generic Windows automation depends on the application's UI and what controls it exposes.

Check:

1. The application successfully opened.
2. The correct window received focus.
3. The requested control is visible.
4. The action is supported by the current automation layer.

Some applications may require additional UI interaction logic.

---

# 🚀 Future Improvements

Possible future additions include:

* Better Windows UI element detection
* More reliable application focusing
* Clipboard-based text input for special characters
* Screen understanding for GUI actions
* Confirmation for risky actions
* Persistent application/session memory
* File and document management
* Calendar and email integration
* Browser automation
* Better multi-step task execution
* Offline speech recognition
* Wake-word activation
* Voice interruption support
* Task execution history
* GUI dashboard for Anni

---

# 📊 Technologies Used

| Technology                      | Purpose                           |
| ------------------------------- | --------------------------------- |
| Python                          | Main programming language         |
| Groq                            | AI language model API             |
| GPT-OSS 20B                     | AI conversation and task planning |
| SpeechRecognition               | Speech-to-text                    |
| pyttsx3                         | Text-to-speech                    |
| PyAutoGUI                       | Keyboard and mouse automation     |
| pywinauto                       | Windows UI Automation             |
| python-dotenv                   | Environment variable management   |
| PowerShell / Windows Start Apps | Dynamic application discovery     |

---

# 💡 Project Goal

The goal of Anni Smart Assistant AI is to create a personal desktop assistant that allows users to interact with their Windows computer through natural spoken commands.

Instead of requiring commands such as:

```text
Open Excel
```

followed by repeated application names, Anni is designed to support:

```text
Open Excel

Type Name

Press Tab

Type Age

Save
```

with the assistant remembering that Excel is the current application.

The project aims to bridge the gap between a traditional voice assistant and an AI-powered desktop automation agent.

---

# 📜 License

This project is intended for educational and personal use.

---

# 👨‍💻 Author

**Barun Ghanti**

Anni Smart Assistant AI
Python • AI • Voice Assistant • Windows Automation
