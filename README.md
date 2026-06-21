# MyfinalYearProject-NEXA-
#  AI-Driven Voice Based Intelligent Desktop Control System

An intelligent desktop assistant that enables users to control their computer using natural voice commands. The system combines Speech Recognition, Natural Language Processing (NLP), Context Awareness, and Desktop Automation to provide a hands-free desktop experience.

---

##  Project Overview

The AI-Driven Voice Based Intelligent Desktop Control System allows users to interact with their computer through voice commands instead of traditional keyboard and mouse inputs.

The application captures voice input, converts it into text using speech recognition, identifies user intent through NLP techniques, and performs the corresponding desktop action automatically.

Examples:

- "Open Chrome"
- "Search for Machine Learning on Google"
- "Create a new folder"
- "Shutdown the system"
- "Find my resume PDF"

---

##  Problem Statement

Traditional desktop interaction depends heavily on keyboards and mice, which may not always be convenient.

This project aims to:

- Improve accessibility
- Enable hands-free computer operation
- Increase productivity
- Provide intelligent command understanding
- Support personalized user experiences

---

##  Features

###  Voice Recognition
- Audio Capture
- Noise Reduction
- Speech-to-Text Conversion
- Whisper Model Integration

###  Natural Language Processing
- Intent Detection
- Entity Extraction
- Context Analysis
- Command Parsing

###  Desktop Automation
- Open Applications
- Close Applications
- File Operations
- Web Search Automation
- System Control

###  User Management
- User Authentication
- Session Management
- Voice Authentication
- User Profiles

###  Database Support
- SQLite Database
- User Data Storage
- Command History Tracking
- Profile Management

###  GUI Interface
- Login Window
- Dashboard
- Command Panel
- Voice Visualizer
- Settings Management

###  Security
- Password Encryption
- Secure Session Handling
- User Authentication System

---

##  System Architecture
---
Voice Input
       
       ↓

Speech-to-Text (Whisper)
       
       ↓

Intent Detection
       
       ↓

Entity Extraction
       
       ↓

Context Analysis
       
       ↓

Command Execution
       
       ↓

Desktop Action

---

##  Technologies Used

### Programming Language
- Python 3.8+

### GUI Framework
- PyQt5

### Database
- SQLite
- SQLAlchemy

### Machine Learning & NLP
- Scikit-Learn
- Rule-Based NLP
- Intent Detection

### Speech Processing
- Whisper
- SpeechRecognition
- PyAudio
- Librosa

### Automation
- PyAutoGUI
- Keyboard
- Mouse

### Security
- Cryptography

---

##  Project Structure

```
AI_Voice_Desktop_Control/
│
├── main.py
├── requirements.txt
│
├── data/
│   ├── database/
│   ├── logs/
│   ├── models/
│   └── user_profiles/
│
├── resources/
│   ├── configs/
│   ├── templates/
│   └── icons/
│
├── src/
│   ├── auth/
│   ├── speech_processing/
│   ├── nlp_processing/
│   ├── desktop_control/
│   ├── context_awareness/
│   ├── database/
│   ├── gui/
│   └── core/
│
└── scripts/
```


##  Installation

### Clone Repository

git clone https://github.com/yourusername/AI-Voice-Desktop-Control.git
cd AI-Voice-Desktop-Control

Create Virtual Environment
python -m venv venv

Activate environment:
Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

## Run Project
python main.py

## Workflow
# Step 1: Voice Capture
The system records user voice input using the microphone.

# Step 2: Speech Recognition
Audio is processed and converted into text using Whisper Speech Recognition.

# Step 3: Intent Detection
The NLP engine identifies the user's intent.

# Examples:
Open Application

File Search

Web Search

System Control

# Step 4: Entity Extraction
Important entities such as:
Application Names
File Names
Search Queries
are extracted.

# Step 5: Context Analysis
User history and preferences are considered.

# Step 6: Command Execution
The requested action is executed automatically.

## Example Commands
Voice Command	Action

Open Chrome	Launches Chrome

Close Notepad	Closes Notepad

Search AI on Google	Opens browser and searches

Create Folder Projects	Creates folder

Shutdown Computer	Shuts down system

## Future Enhancements
* Deep Learning-based Intent Classification

* GPT-based Conversational Assistant

* Multi-language Voice Support

* Smart Task Scheduling

* Voice Biometrics Authentication

* Cloud Synchronization

## Testing
Run tests using:
pytest

## Learning Outcomes
Through this project:

Implemented Speech Recognition

Built NLP-based Intent Detection

Developed Desktop Automation Features

Created PyQt5 GUI Applications

Integrated Database Management

Applied Software Engineering Principles
