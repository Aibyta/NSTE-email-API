from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        date = data.get('date')
        slot = data.get('slot')

        sender = os.environ.get("EMAIL_ADDRESS")
        password = os.environ.get("EMAIL_PASSWORD")

        subject = f"🎾 Booking Confirmation for {date}"
        html = f"""
        <html>
        <body>
            <h2>Hi {name},</h2>
            <p>Your booking for <b>{slot}</b> on <b>{date}</b> is confirmed!</p>
            <p>- NSTE Team</p>
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

# ✅ This is the critical fix for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
