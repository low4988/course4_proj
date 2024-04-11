from django.db.models.signals import post_save
'''
django.db.models.signals.pre_save
django.db.models.signals.post_save: 
Sent before/after a model's save() method is called.
'''
from django.dispatch import receiver
# SearchTerm model, term is unique TextField
from movies.models import SearchTerm
# task function, asyncronous
from movies.tasks import notify_of_new_search_term


''' search_term_saved() listener function
## sender=SearchTerm 
We use the sender argument,  on the receiver decorator 
so that the hook is ONLY called when a save to SearchTerm model

## dispatch_uid: 
although the method we're using to set up the receiver 
should protect against receivers being set up multiple times, 
This is additional safety based on dispatch_uid
''' 

''' sender=SearchTerm, here a class
sender can be just about anything, 
provided that the receiver has access to that particular object. 
The sender can be a class, 
but shouldn't be an instance of a class, 
as the receiver may not have access to the particular instance.
'''

# arg1 post_save signal, arg2 model that is saved to,  
@receiver(post_save, sender=SearchTerm, dispatch_uid="search_term_saved")
def search_term_saved(sender, instance, created, **kwargs):
    # instance is the SearchTerm that was saved 
    #  instance.term, search string
    # created is a boolean indicating .get_or_create()
    #  if the SearchTerm was new -> created (True), or updated (False).
    if created:
        # new SearchTerm was created

        # call asyncronous task triggered by signal: post_save call to SearhTerm model
        # tasks in celery worker
        notify_of_new_search_term.delay(instance.term) # arg1 what was the term string
        
        # prints syncronoysly, waiting until finished, to terminal by signal post_save call
        #print(f"A new SearchTerm was created: '{instance.term}'")
        
    
    '''
    Save method
    We could also get the same result by implementing the save() method 
    on the SearchTerm MODEL directly, instead of instance.term,
    however you could argue that doing that would tie the model class 
    too closely to the behavior of the project as a whole, 
    and so it's a violation of separation of concerns.
    '''

'''
In theory, handlers and their registration calls 
could be put anywhere in your project. 

However a good convention is to place them in a 
signals module or signals.py file inside the app that they're for.

movies/signals.py

To make sure our handler is set up, 
all we need to do is import the signals.py file. 

A good place to do this is in the ready() method 
of the AppConfig class for the app. 

movies/apps.py

This method is called once the app is ready to use.
For example, the MoviesConfig class is in movies/apps.py. 

It was mostly automatically created when the 
app was started with the startapp command. 

We just need to add the ready() method containing the import:

This should limit the import of 
movies/signals.py 
per this app to once only
-additional safety by dispatch_uid

'''