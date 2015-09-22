from my_project.settings.settings import *

# DEBUG = False
ALLOWED_HOSTS = ['localhost']

#THIS IS WHERE ALL THE STATIC FILES ARE COPIED TO WHEN COLLECT STATIC IS RUN
#NGINX SOULD POINT TO THIS FILE TO FIND THE STATIC FILES
STATIC_ROOT = os.path.join(os.getcwd(), "static")


