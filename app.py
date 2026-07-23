from flask import Flask, render_template, jsonify, request
from email_handler import EmailHandler
from voice_handler import VoiceHandler
from image_captioner import ImageCaptioner

app = Flask(__name__)

email_handler = EmailHandler()
voice_handler = VoiceHandler()
image_captioner = ImageCaptioner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    """Listen for voice command and process it."""
    command = voice_handler.listen()
    intent = voice_handler.get_intent(command)
    return jsonify({'command': command, 'intent': intent})

@app.route('/read_emails', methods=['GET'])
def read_emails():
    """Fetch inbox emails and read them aloud."""
    emails = email_handler.fetch_inbox()
    summaries = []
    for i, mail in enumerate(emails):
        summary = f"Email {i+1}. From {mail['from']}. Subject: {mail['subject']}."
        voice_handler.speak(summary)
        summaries.append(summary)
    return jsonify({'emails': summaries})

@app.route('/read_email/<int:email_id>', methods=['GET'])
def read_email(email_id):
    """Read a specific email aloud including image descriptions."""
    emails = email_handler.fetch_inbox()
    if email_id >= len(emails):
        return jsonify({'error': 'Email not found'}), 404

    mail = emails[email_id]
    body_text = f"From: {mail['from']}. Subject: {mail['subject']}. Body: {mail['body']}"
    voice_handler.speak(body_text)

    # Handle image attachments
    captions = []
    for attachment in mail.get('attachments', []):
        if attachment['type'].startswith('image'):
            caption = image_captioner.caption(attachment['data'])
            voice_handler.speak(f"Image description: {caption}")
            captions.append(caption)

    return jsonify({'body': body_text, 'image_captions': captions})

@app.route('/compose', methods=['POST'])
def compose():
    """Compose and send an email via voice."""
    data = request.json
    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    voice_handler.speak(f"Sending email to {to} with subject {subject}.")
    result = email_handler.send_email(to, subject, body)
    if result:
        voice_handler.speak("Email sent successfully.")
    else:
        voice_handler.speak("Failed to send email. Please try again.")
    return jsonify({'success': result})

@app.route('/reply', methods=['POST'])
def reply():
    """Reply to an email."""
    data = request.json
    email_id = data.get('email_id')
    body = data.get('body')

    emails = email_handler.fetch_inbox()
    if email_id >= len(emails):
        return jsonify({'error': 'Email not found'}), 404

    original = emails[email_id]
    result = email_handler.send_email(original['from'], f"Re: {original['subject']}", body)
    if result:
        voice_handler.speak("Reply sent successfully.")
    return jsonify({'success': result})

@app.route('/delete', methods=['POST'])
def delete():
    """Delete an email."""
    data = request.json
    email_id = data.get('email_id')
    result = email_handler.delete_email(email_id)
    voice_handler.speak("Email deleted." if result else "Could not delete email.")
    return jsonify({'success': result})

if __name__ == '__main__':
    app.run(debug=True)

