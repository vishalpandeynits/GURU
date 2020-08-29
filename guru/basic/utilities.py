from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class TokenGenerator(PasswordResetTokenGenerator):
    def make_token(self, user):
        return (
            six.text_type(user.pk) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()