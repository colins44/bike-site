from my_project.settings.settings import *

# DEBUG = False
ALLOWED_HOSTS = ['localhost']
DEBUG = False

#THIS IS WHERE ALL THE STATIC FILES ARE COPIED TO WHEN COLLECT STATIC IS RUN
#NGINX SOULD POINT TO THIS FILE TO FIND THE STATIC FILES
STATIC_ROOT = os.path.join(os.getcwd(), "static")

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'enquiry@youvelo.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'this_is_not_the_password')


EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_ADDRESS
DEFAULT_TO_EMAIL = EMAIL_ADDRESS