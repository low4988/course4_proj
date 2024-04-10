from celery import shared_task

from movies import omdb_integration

@shared_task
def search_and_save(search):
    return omdb_integration.search_and_save(search)

'''
Since task functions can be called normally 
(i.e. even if decorated we can still 
call search_and_save() instead of 
search_and_save.delay()) 
we could choose to move the functions 
from omdb_integration.py to 
tasks.py. 

Having them segregated like this can make it more 
clear which functions you intend to run as tasks.
'''