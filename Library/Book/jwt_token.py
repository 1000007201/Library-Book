from jwt import decode
from django.conf import settings
from .utils import Utils
from functools import wraps
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


def token_required(f):
    try:
        @wraps(f)
        def token_decode(request, *args, **kwargs):
            # token = request.headers.get('Authorization')
            short_token = request.headers.get('Token')
            if not short_token:
                short_token = request.query_params.get('token')
            if not short_token:
                return JsonResponse({'Error': 'Token is missing!', 'Code': 409})
            index = short_token.find('.')
                # data = decode(token.split()[1], settings.SECRET_KEY, 'HS256')
            if index == -1:
                token = Utils.true_token(short_token)
            else:
                token = short_token
            data = decode(token, settings.SECRET_KEY, 'HS256')
            user_id = data['user_id']
            return f(request, user_id, *args, **kwargs)
        return token_decode
    except Exception as e:
        return JsonResponse({'Error': str(e), 'Code': 409})