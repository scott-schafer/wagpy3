from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-!wrxu=8rtogpjjf=025b-b=mj1m4r8qz=c__!jnqb(i0copcrz"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]



EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
