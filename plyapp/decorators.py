from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
            
        else:
            return HttpResponseRedirect(reverse('admin:login'))  # Redirect to admin login page
    return _wrapped_view
