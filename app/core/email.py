from djoser.email import PasswordResetEmail, PasswordChangedConfirmationEmail
from django.conf import settings

class CustomPasswordResetEmail(PasswordResetEmail):

    template_name = "emails/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["frontend_url"] = settings.FRONTEND_URL
        return context
    

class PasswordResetConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "emails/password_reset_confirmation.html"