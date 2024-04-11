from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    '''
    To make sure our handler is set up, 
    all we need to do is import the signals.py file. 
    
    A good place to do this is in the ready() 
    method of the AppConfig class for the app. 
    
    This method is called once the app is ready to use.

    For example, the MoviesConfig class is in movies/apps.py. 
    
    It was mostly automatically created when the app was 
    started with the 
    startapp command. 
    We just need to add the ready() method containing the import:
    '''
    def ready(self):
      import movies.signals  # noqa
      # The # noqa at the end of the import line 
      # instructs linters to ignore this line 
      # when checking the code format.
      # could get an error or warning that the import is not used