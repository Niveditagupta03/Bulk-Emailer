import smtplib
import ssl
import config

print(f"Testing login for: {config.EMAIL_ADDRESS}")
print(f"Password starts with: {config.EMAIL_APP_PASSWORD[:2]}...")

try:
    context = ssl.create_default_context()
    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(config.EMAIL_ADDRESS, config.EMAIL_APP_PASSWORD)
        print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
