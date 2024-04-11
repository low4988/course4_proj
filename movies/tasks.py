'''
# For a function to be turned into a task it must be registered to the Celery app
# For this reason, Celery provides a special decorator called shared_task (celery.shared_task). 
# This will register the task to the app defined by celery_app in __init__.py
    # project/celery/__init__.py
        #The contents of __init__.py in the project directory should be:
        #from .celery import app as celery_app

        #__all__ = ("celery_app",)
# Settings.py
    #app = Celery("course4_proj")

# @shared_task Decorated functions now have a new attribute: delay(). 
# This is used to send the function off to be run in the Celery worker rather than the current process.
'''

from celery import shared_task

from movies import omdb_integration
# ADMINS address tuple, settings.py
from django.core.mail import mail_admins

@shared_task
def search_and_save(search):
    return omdb_integration.search_and_save(search)

# notify by mail when new search term is used
# by save new value hook post_save signal
 # from django.db.models.signals import post_save
 # @receiver(post_save, sender=SearchTerm, dispatch_uid="search_term_saved")
@shared_task
def notify_of_new_search_term(search_term):
    # notify by mail when new search term is used
    mail_admins("New Search Term", f"A new search term was used: '{search_term}'")
'''
Since task functions can be called normally 
(i.e. even if decorated we can still 
call search_and_save() instead of 
search_and_save.delay()) 
we could choose to move the functions 
from omdb_integration.py to 
tasks.py. 

Having them segregated like this can make it more 
clear which functions you intend to run as tasks, asyncronously.
'''