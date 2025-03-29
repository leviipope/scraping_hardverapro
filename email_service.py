# email_service.py
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os

class EmailService:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.api_instance = None

        # Only initialize if enabled
        if self.enabled:
            # Get API key from environment
            brevo_api_key = os.getenv("BREVO_API_KEY")

            # Check if API key exists
            if brevo_api_key is None:
                print("Warning: BREVO_API_KEY not set. Email notifications disabled.")
                self.enabled = False
                return

            # Configure API client
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = brevo_api_key
            self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_email(self, gpu):
        if not self.enabled or self.api_instance is None:
            print(f"Email notifications disabled. Would have sent email for: {gpu['name']}")
            return False

        subject = f"New GPU Found: {gpu['name']}"
        body = f"""
        <h2>New GPU Listing</h2>
        <p><strong>Price:</strong> {gpu['price']} Ft</p>
        <p><strong>Time:</strong> {gpu['time']}</p>
        <p><a href="{gpu['link']}">View Listing</a></p>
        """

        email_data = {
            "sender": {"name": "GPU Alerts", "email": "leviiytpublick@gmail.com"},
            "to": [{"email": "leviiytpublick@gmail.com"}],
            "subject": subject,
            "htmlContent": body
        }

        try:
            self.api_instance.send_transac_email(email_data)
            print(f"Email sent for GPU: {gpu['name']}")
            return True
        except ApiException as e:
            print(f"Error sending email: {e}")
            return False