from django.shortcuts import render

import urllib.parse

from celery.exceptions import TimeoutError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from course4_proj.celery import app
from movies.models import Movie
from movies.tasks import search_and_save

# Create your views here.

''' search()
 
It retrieves the search term from the 
search_term query string parameter, 

then uses it to search_and_save.delay(search_term). 

It then waits two seconds for a result, 

If none is received, 
it redirects to the 
-waiting view, 
with the ID of the task for later reference. 

If search results are received within two seconds 
(for example, if there aren't many results 
or the results have already been cached) 
then it redirects straight to the 
-search results view.
'''
def search(request):
    search_term = request.GET["search_term"]
    res = search_and_save.delay(search_term)
    try:
        res.get(timeout=2)
    except TimeoutError:
        return redirect(
            reverse("search_wait", args=(res.id,))
            + "?search_term="
            + urllib.parse.quote_plus(search_term)
        )
    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term),
        permanent=False,
    )

''' search_wait() view
It accepts the task UUID as an argument, 
then uses that to fetch the AsyncResult(). 

It tries to get the result. 
By using a timeout of -1 it will return immediately 
if there's no result: 
using a timeout of 0 actually means 
it will wait forever for a result 
which is not what we want.

If the get() does timeout 
(i.e. there's no result available immediately) 
then a TimeoutError will be raised. 

It's caught and a message is returned 
to the browser telling the user 
to refresh the page to check again. 

If a result is returned 
(which means the task has finished), 

then a redirect to the results pages is returned. 
'''

def search_wait(request, result_uuid):
    search_term = request.GET["search_term"]
    res = app.AsyncResult(result_uuid)

    try:
        res.get(timeout=-1)
    except TimeoutError:
        return HttpResponse("Task pending, please refresh.", status=200)

    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term)
    )

''' search_results view 

It queries the database for the search term and 
returns all the results as a plain text list: 
'''

def search_results(request):
    search_term = request.GET["search_term"]
    movies = Movie.objects.filter(title__icontains=search_term)
    return HttpResponse(
        "\n".join([movie.title for movie in movies]), content_type="text/plain"
    )
'''
Minimal implementation
Note that the intention of these views is to be 
a minimal implementation to demonstrate Celery. 

You'll probably spot several ways 
to raise exceptions. 
For example, if search_term is missing. 
If we were implementing this in a production 
app we'd have much better error handling.'''