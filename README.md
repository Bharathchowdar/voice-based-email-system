# 🎙️ Voice-Based Email System for Visually Impaired

A fully hands-free AI-powered email client for blind and visually impaired users. Compose, read, reply, and manage emails entirely through voice — no visual interface required.

---

## 🚀 Features

- 🎤 Voice command recognition (read, compose, reply, delete)
- 📬 Fetch and read emails aloud using text-to-speech
- 🖼️ Image captioning using InceptionV3 (CNN) — describes image attachments
- 📝 OCR support via Pytesseract for text in images
- 🤖 OpenAI API for intelligent email response generation
- 🔊 Full text-to-speech output for all content

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| Speech Recognition | SpeechRecognition, PyAudio |
| Text-to-Speech | pyttsx3 |
| Image Captioning | TensorFlow, InceptionV3 |
| OCR | Pytesseract |
| AI Response | OpenAI API (GPT-3.5) |
| Frontend | HTML, CSS, JavaScript |
| Email Protocol | IMAP (receive), SMTP (send) |

---

## 📁 Project Structure

```
voice_email/
├── app.py                  # Flask main application
├── voice_handler.py        # Speech recognition & TTS
├── email_handler.py        # IMAP/SMTP email operations
├── image_captioner.py      # InceptionV3 image captioning
├── templates/
│   └── index.html          # Web frontend
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/voice-email-system.git
cd voice-email-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR
- **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in:
- Your Gmail address and App Password (not your regular password)
- Your OpenAI API key

> **Gmail Setup:** Enable 2FA → Google Account → Security → App Passwords → Generate one for "Mail"

### 5. Run the application
```bash
python app.py
```
Open your browser at `http://localhost:5000`

---

## 🎯 Voice Commands

| Command | Action |
|---------|--------|
| "Read my emails" | Fetches and reads inbox aloud |
| "Compose email" | Start composing a new email |
| "Reply" | Reply to current email |
| "Delete" | Delete current email |
| "Inbox" | List all emails |

---

## 👨‍💻 Developer

**Bharath Gurujala** — AI/ML Engineer  
📧 bharathchowdary1560@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/bharath-gurujala-40093b229)
