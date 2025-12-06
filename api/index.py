import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soil_analysis.settings')

# Configure Django settings for Vercel
if not settings.configured:
    settings.configure(
        DEBUG=False,
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'corsheaders',
            'api.apps.ApiConfig',
        ],
        MIDDLEWARE=[
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF='soil_analysis.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
            },
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.path.dirname(__file__), '..', 'backend', 'db.sqlite3'),
            }
        },
        SECRET_KEY='django-insecure-x@a4^s8-1jtr*&46$2n73#+1%+@!!dkn5g(75)af*ixs1(gl&k',
    )

app = get_wsgi_application()
