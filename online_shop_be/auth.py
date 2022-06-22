import jwt
from bson import ObjectId
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from online_shop_be import settings
from users.models import User


class JWTAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return None
        try:
            user_payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ENCRYPTION_METHOD)
        except (jwt.exceptions.InvalidSignatureError, jwt.ExpiredSignatureError, jwt.exceptions.DecodeError) as e:
            raise AuthenticationFailed('Invalid Authentication token')
        else:
            user_id = user_payload.get('user_id')
            try:
                user = User.objects.get(_id=ObjectId(user_id))
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid Authentication token')
            else:
                return (user, token)


class IsRetailer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     return obj._id == request.user._id
