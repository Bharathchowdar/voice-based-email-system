import speech_recognition as sr
import pyttsx3
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

INTENTS = {
    "read": ["read", "open", "check", "show", "listen"],
    "compose": ["compose", "write", "create", "new email", "send"],
    "reply": ["reply", "respond", "answer"],
    "delete": ["delete", "remove", "trash"],
    "inbox": ["inbox", "emails", "messages", "list"],
    "exit": ["exit", "quit", "close", "stop"],
}


class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        """Convert text to speech and play it."""
        print(f"[TTS]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = 5) -> str:
        """Listen for voice input and return transcribed text."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.speak("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio)
                print(f"[Heard]: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please try again.")
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I could not understand. Please repeat.")
                return ""
            except sr.RequestError as e:
                self.speak("Speech recognition service is unavailable.")
                print(f"[Error]: {e}")
                return ""

    def get_intent(self, command: str) -> str:
        """Classify voice command into an intent."""
        command = command.lower()
        for intent, keywords in INTENTS.items():
            if any(kw in command for kw in keywords):
                return intent
        return "unknown"

    def generate_email_body(self, prompt: str) -> str:
        """Use OpenAI to generate an email body from a voice prompt."""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an email assistant. Write a professional email body based on the user's voice instruction."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[OpenAI Error]: {e}")
            return prompt
