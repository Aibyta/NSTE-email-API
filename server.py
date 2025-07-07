from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

@app.route('/send-event-invite', methods=['POST'])
def send_event_invite():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        eventName = data.get('eventName')
        date = data.get('date')
        time = data.get('time')
        organizer = data.get('organizer')
        eventId = data.get('eventId')

        sender = os.environ.get("EMAIL_ADDRESS")
        password = os.environ.get("EMAIL_PASSWORD")

        subject = f"🎾 You've been matched for {eventName}!"
        html = f"""
        <html>
        <body>
            <h2>Hi {name},</h2>
            <p>Our AI system has matched you with an upcoming event:</p>
            
            <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin:15px 0;">
                <h3>{eventName}</h3>
                <p><b>Date:</b> {date}</p>
                <p><b>Time:</b> {time}</p>
                <p><b>Organizer:</b> {organizer}</p>
            </div>
            
            <p>To confirm your participation, please reply to this email with "Confirm" in the subject line.</p>
            
            <p>Alternatively, you can click the button below to send a confirmation email automatically:</p>
            
            <p>
                <a href="mailto:{sender}?subject=Confirm%20Participation%20for%20{eventName.replace(' ', '%20')}&body=I%20confirm%20my%20participation%20in%20{eventName.replace(' ', '%20')}%20on%20{date}%20at%20{time}." 
                   style="background:#0d6efd;color:white;padding:10px 15px;border-radius:5px;text-decoration:none;">
                    Confirm Participation
                </a>
            </p>
            
            <p>- NSTE AI Matchmaking System</p>
        </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.sendmail(sender, email, msg.as_string())

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
