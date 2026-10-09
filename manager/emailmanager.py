import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# ---------------------------------------------------
# BREVO
# ---------------------------------------------------
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL", "")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_API_URL = os.getenv("BREVO_API_URL", "https://api.brevo.com/v3/smtp/email")

# ==========================================
# SEND EMAIL
# ==========================================
def send_email(tomail, subject, message):
    try:
        print("========== EMAIL DEBUG ==========")
        print("BREVO API KEY:", BREVO_API_KEY)
        print("BREVO API URL:", BREVO_API_URL)
        print("Sending Email To:", tomail)

        payload = {
            "sender": {
                "email": BREVO_SENDER_EMAIL
            },
            "to": [
                {
                    "email": tomail
                }
            ],
            "subject": subject,
            "textContent": message
        }
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        }
        response = requests.post(
            url=BREVO_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        print("Brevo Status Code: ", response.status_code)
        print("Brevo Response: ", response.text)

        if response.status_code != 201:
            print(f"[Brevo Error] Expected 201 but got {response.status_code}: {response.text}")
            return False

        return True
    except Exception as e:
        print("[Email Exception]: ", e)
        return False

# ==========================================
# SEND OTP EMAIL
# ==========================================
def send_otp_email(email, username, otp):
    subject = "OTP Verification"
    message = (
        f"Dear {username},\n\n"
        f"Your OTP verification code is: {otp}\n\n"
        "Valid for 5 minutes."
    )
    return send_email(email, subject, message)

# ==========================================
# SEND PASSWORD RESET EMAIL
# ==========================================
def send_password_reset_email(email, username, reset_token):
    subject = "Password Reset"
    reset_link = (
        f"{FRONTEND_URL}"
        f"/reset-password"
        f"?email={email}"
        f"&token={reset_token}"
    )

    message = (
        f"Dear {username},\n\n"
        f"Your requested a password reset.\n\n"
        f"Your password reset link is: {reset_link}\n\n"
        f"This link expires in 10 minutes.\n\n"
        f"If you didn't request this, ignor the email."
    )
    return send_email(email, subject, message)
