from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # Allow all origins (or restrict by domain later)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        date = data.get('date')
        slot = data.get('slot')

        # Email setup
        sender = "your_email@gmail.com"
        password = "your_app_password"  # Use Gmail App Password
        receiver = email

        subject = f"🎾 Booking Confirmed for {date}"
        html = f"""
        <html>
        <body>
            <h2>Hi {name},</h2>
            <p>✅ Your booking for <b>{slot}</b> on <b>{date}</b> is confirmed!</p>
            <p>🏸 See you at the NSTE Court!</p>
            <br><p style='color:gray;'>- NSTE Team</p>
        </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, msg.as_string())

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
