from my_project.settings.settings import *

# DEBUG = False
ALLOWED_HOSTS = ['*']
DEBUG = False

#THIS IS WHERE ALL THE STATIC FILES ARE COPIED TO WHEN COLLECT STATIC IS RUN
#NGINX SOULD POINT TO THIS FILE TO FIND THE STATIC FILES
STATIC_ROOT = os.path.join(os.getcwd(), "static")

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get("EMAIL_ADDRESS", 'testing')
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD", 'One_two')
DEFAULT_FROM_EMAIL = 'enquiry@youvelo.com'
DEFAULT_TO_EMAIL = 'enquiry@youvelo.com'
EMAIL_FROM_ADDR = 'enquiry@youvelo.com'