from users.models import CustomUser
from rest_framework import authentication
from rest_framework import exceptions

class EmailAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.META.get('X-Email') # get the username request header
        if not email: # no username passed in request headers
            return None # authentication did not succeed

        try:
            user = CustomUser.objects.get(email=email) # get the user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist 

        return (user, None) # authentication successful