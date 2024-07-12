from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def driver_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='uber_drivers').exists():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
