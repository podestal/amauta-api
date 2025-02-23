from djoser.email import PasswordResetEmail
from django.conf import settings

class CustomPasswordResetEmail(PasswordResetEmail):

    template_name = "emails/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["frontend_url"] = settings.FRONTEND_URL
        return context