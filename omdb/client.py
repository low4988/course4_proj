import logging

import requests

logger = logging.getLogger(__name__)

OMDB_API_URL = "https://www.omdbapi.com/"

class OmdbMovie:
    """A simple class to represent 
    movie data coming back from OMDb
    and transform to Python types.
     A intermediary/transformer between the 
     JSON dictionary returned from OMDb and 
     raw Python data
    •	Validating and transforming the movie's runtime.
    •	Converting the movie's year into and int.
    •	Checking if keys are set and raising exceptions if trying to access detail keys on non-detail response.
    •	Splitting the genre into a list.
    Check that a detail data key is only present for detail views
     - method for detail check, check_for_detail_data_key
"""

    def __init__(self, data):
        """Data is the raw JSON/dict returned from OMDb"""
        self.data = data

    def check_for_detail_data_key(self, key):
        """Some keys are only in the detail response, raise an
        exception if the key is not found."""
        
        if key not in self.data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )
    '''
    class Person(models.Model):
      first_name = models.CharField(max_length=50)
      last_name = models.CharField(max_length=50)
      birth_date = models.DateField()
    
    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)  

    As you see, the function full_name returns a string with the 
    persons first and last name.
    What the @property decorator does,
    is declare that it can be accessed like it's a regular property.
    This means you can call full_name as if it were a member variable 
    instead of a method, like this:
    
    name = person.full_name
    instead of
    name = person.full_name()

    easily update self.data["key"], in case it changes 
    OmdbMovie.title stays the same even if 'title'-key changes to e.g name 
    '''
    @property
    def imdb_id(self):
        return self.data["imdbID"]

    @property
    def title(self):
        return self.data["Title"]

    @property
    def year(self):
        return int(self.data["Year"])

    @property
    def runtime_minutes(self):
        self.check_for_detail_data_key("Runtime")

        rt, units = self.data["Runtime"].split(" ")

        if units != "min":
            raise ValueError(f"Expected units 'min' for runtime. Got '{units}")

        return int(rt)

    @property
    def genres(self):
        self.check_for_detail_data_key("Genre")

        return self.data["Genre"].split(", ")

    @property
    def plot(self):
        self.check_for_detail_data_key("Plot")
        return self.data["Plot"]


class OmdbClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def make_request(self, params):
        """Make a GET request to the API, 
        automatically adding the `apikey` to parameters."""
        # apikey needed to authenticate to api, access only for registered users
        params["apikey"] = self.api_key
        # make_request includes parameters to add to requests
        resp = requests.get(OMDB_API_URL, params=params)
        # check for errors
        resp.raise_for_status()
        return resp

    def get_by_imdb_id(self, imdb_id):
        """use IMDB ID of the movie and fetch the full detail response."""
        logger.info("Fetching detail for IMDB ID %s", imdb_id)
        resp = self.make_request({"i": imdb_id})
        # return a fully python item made by OmdbMovie, 
        # created with response json.data
        return OmdbMovie(resp.json()) 

    def search(self, search):
        """Search for movies by title. 
        This is a generator so all results 
        from all pages will be iterated across.
        create OmdbMovie instance for each"""
        page = 1
        seen_results = 0
        total_results = None

        logger.info("Performing a search for '%s'", search)

        # Iterate until break
        while True:
            logger.info("Fetching page %d", page)
            resp = self.make_request({"s": search, "type": "movie", "page": str(page)})
            resp_body = resp.json()
            # defaults to None
            if total_results is None:
                total_results = int(resp_body["totalResults"])

            for movie in resp_body["Search"]:
                seen_results += 1
                # create OmdbMovie instance for each
                yield OmdbMovie(movie)

            if seen_results >= total_results:
                break

            page += 1