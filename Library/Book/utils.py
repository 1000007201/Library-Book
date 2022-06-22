import base64
from django.contrib.auth.models import User


class Utils:

    @staticmethod
    def token_short(token):
        token_string_bytes = token.encode("ascii")

        base64_bytes = base64.b64encode(token_string_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string

    @staticmethod
    def true_token(token_):
        base64_bytes = token_.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return 

    @staticmethod
    def check_superuser(user_id):
        user_obj = User.objects.get(pk=user_id)
        if not user_obj.is_superuser:
            return {'Error': 'You are not permitted', 'Code': 404}

