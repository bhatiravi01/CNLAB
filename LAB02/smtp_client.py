import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ----------------------------
# CONFIGURATION (EDIT THESE)
# ----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Gmail uses 587 with STARTTLS
SENDER_EMAIL ="ravindrabhati1007@gmail.com"          # <-- your Gmail
SENDER_PASSWORD = "zlpo trip wrqx nfwm"     # <-- App Password from Google
RECIPIENT_EMAIL = "ashishayu100@gmail.com"  # <-- recipient email

def send_email():
    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection

        # Login
        print("Logging in...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Create message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "SMTP Lab Test"
        body = "Hello! I am Ravindra Bhati."
        msg.attach(MIMEText(body, "plain"))

        # Send mail
        print("Sending email...")
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email sent successfully!")

        server.quit()

    except Exception as e:
        print("SMTP Error:", e)

if __name__ == "__main__":
    send_email()
