from django.db import models
from singly import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist




class User(User):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=130, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'))
    first_name = models.CharField(_('first name'), max_length=130, blank=True)
    last_name = models.CharField(_('last name'), max_length=130, blank=True)


class UserProfileManager(models.Manager):

    def get_or_create_user(self, singly_id, access_token):
        endpoint = '/profiles'
        request = {'auth': 'true'}
        profiles = Singly(access_token=access_token).make_request(endpoint, request=request)
        singly_id = profiles['id']
        try:
            user_profile = self.get(singly_id=singly_id)
            user_profile.profiles = profiles
            user_profile.access_token = access_token
            user_profile.save()

        except ObjectDoesNotExist:
            try:
                user = User.objects.get(username=singly_id)
            except ObjectDoesNotExist:
                # Made-up email address included due to convention
                user = User.objects.create_user(singly_id, singly_id + '@singly.com', 'fakepassword')
            user_profile = self.model(
                access_token=access_token,
                singly_id=singly_id,
                profiles=profiles,
                user=user
            )
            user_profile.save()
        return user_profile
