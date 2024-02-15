"""Authentication"""
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from .models import BlackListedToken

import jwt
from django.conf import settings
secret = settings.JWT_SECRET_KEY

ACCESS_DENIED_MSG = "Access denied" 
class BaseUser():
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.is_authenticated = None
class CustomAuthenticationJwt(BaseAuthentication):



    @staticmethod
    def _init_domain_user(user_info, domain_class):
        try:
            domain_user = domain_class(user_info['id'], user_info['email'])

            return domain_user
        except Exception as err:
            raise AuthenticationFailed(ACCESS_DENIED_MSG) from err

    def detect_user(self, user_info):
        """ returns domain user object """
        domain_class = BaseUser
        domain_user = self._init_domain_user(user_info, domain_class)

        domain_user.is_authenticated = True
        return domain_user, None
    @staticmethod
    def get_auth_method_and_token(request):
        """ extract authentication method and token """
        auth = get_authorization_header(request).decode()
        if not auth:
            # No Authentication header, Anonymous
            return None, None

        try:
            method, token = auth.split(' ')
        except ValueError:
            # Unknown authentication method, Anonymous
            return None, None

        return method, token
    
    def validate_jwt(self, token):
        try:
            payload = jwt.decode(token,  secret, algorithms= ["HS256"])
            return payload
        except Exception as e:
            raise AuthenticationFailed('can not verify the token', e)

    def authenticate(self, request):
        """ authenticate with JWT method """
        method, jwt_token = self.get_auth_method_and_token(request)

        if method == "JWT":
            payload  = self.validate_jwt(jwt_token)
            try:
                email = payload["email"]
                id = payload["id"]
                userinfo = {"email":email, "id":id}
                print('detect_user')
                return self.detect_user(userinfo)
            except Exception as e:
                raise AuthenticationFailed('user is not valid', e)
        return None

class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.user_id            
        is_allowed_user = True
        token = request.META.get('HTTP_AUTHORIZATION', '')
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user