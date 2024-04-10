import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course4_proj.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations

configurations.setup()

app = Celery("course4_proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

'''
The app variable is an instance of the celery.Celery class, 
so we need to import that, among other modules that you would have seen before. Then, we need to set up the environment variables for Django. First DJANGO_SETTINGS_MODULE for the Django settings and then DJANGO_CONFIGURATION so that Django Configurations knows which settings class to use.

We then import configurations and run configurations.setup(), 
to enable Django Configurations. 
We'll get an exception without this step.

Then we instantiate the Celery class with a name 
- in this case we use the project name. 
We call config_from_object() on the instance, 
and tell it to load the settings 
from the settings variable in the django.conf module. 
The namespace argument essentially means the prefix for 
the Celery settings, e.g. broker_url comes from CELERY_BROKER_URL.

Finally we call autodiscover_tasks() on the app. 
This will go through our INSTALLED_APPS and 
look inside the files tasks.py and models.py 
for each of them, loading any tasks it finds. 

'''


'''
celery -A course4_proj worker -l DEBUG

- -A is the application argument, 
in this case we want to import it from the course4_proj module.

- worker is the command to run, 
which means start a worker instance

- -l sets the log level, we set it to INFO. 
You could also use DEBUG, WARN, ERROR, etc.
'''