from django.db import models
from django.contrib.auth.models import User, UserManager

class Profile(User):
    refresh_token = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    asana_id = models.CharField(max_length=100)
    asana_email = models.CharField(max_length=200)
    
    objects = UserManager()

    class Meta:
        app_label= 'insana'

    @classmethod
    def create_new_user(klass, username, name, asana_id, access_token, refresh_token, email):
        names = name.split()
        if len(names) >= 2:
            first_name = name[0]
            last_name = " ".join(names[1:])
        else:
            raise Exception('oo shit something wrong')

        profile = klass(username=username, first_name=first_name, last_name=last_name, asana_id=asana_id, asana_access_token=access_token, asana_refresh_token=refresh_token, asana_email=email)
        profile.save()
        return profile
