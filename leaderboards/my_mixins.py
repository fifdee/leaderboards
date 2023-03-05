from django.views import generic
from django.contrib.auth import authenticate
from django.conf import settings


class CheckIfUserConverted(generic.View):
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.temporary:
            try:
                temp_password_part = settings.TEMP_PASSWORD_PART
                id_part = user.username.split('_')[1]
                password = temp_password_part + '_' + id_part

                temporary = authenticate(self.request, username=user.username, password=password)
                if not temporary:
                    # default credentials don't work - new password was set
                    print('not temporary')
                    user.temporary = False
                    user.save()
            except IndexError:
                ...

        return super(CheckIfUserConverted, self).dispatch(*args, **kwargs)
