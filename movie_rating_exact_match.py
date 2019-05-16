#!/usr/bin/env python2
import sys, requests, logging

level = logging.INFO
#level = logging.DEBUG
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=level)

def usage(name):
	print "Usage: " + name + " Name of the movie"
	print "Example: " + name + " Guardians of the Galaxy Vol. 2"
def lookup_rating_by_title(title): 
	''' This function returns two variables. The first variable indicates the success of the title against the imdb database. The second variable provides the rating should there be a succcessful 'exact' match.
	We use the type=movie to limit the search to movie type and ignore series and episode types. 
	'''
	base_url="http://www.omdbapi.com/?apikey=8cfbd1c9&type=movie" 
	logging.debug('base_url = ' + base_url)
	title_url = base_url + "&t=" + title
	logging.debug('title_url = ' + title_url)
	response_title = requests.get(title_url)
	logging.debug('response_title = ' + repr(response_title.json()))
	rating = -1 
	rating_bool = False
	if response_title.json()['Response'] == 'True' : 
		ratings_list = response_title.json()['Ratings']
		logging.debug('ratings_list = ' + repr(ratings_list))
		for i in range(len(ratings_list)): 
			logging.debug('index value of ratings_list i = ' + repr(i))
			if ratings_list[i]['Source'] == 'Rotten Tomatoes' : 
				rating_bool = True
				rating = ratings_list[i]['Value']
				logging.debug('rating = ' + rating)
				break
		if rating_bool :
			print 'The movie ' + title + ' has a Rotten Tomatoes rating of ' + rating + '.' 
		else:
			print 'The movie ' + title + ' does not have a Rotten Tomatoes rating.' 
	else:
		logging.error( response_title.json()['Error'])
	return rating_bool, rating
if __name__ == "__main__"  : 
	if len(sys.argv) == 1: 
		usage(sys.argv[0])
	else:
		# Assume the user of this program may or may not put the name of the movie in quotes. This will allow the python program to work with and without quotes. 
		title = sys.argv[1:]
		title = " ".join(title)
		logging.debug("title = " + title)
		rating_bool, rating = lookup_rating_by_title(title)
		logging.debug("rating_bool = " + repr(rating_bool))
		logging.debug("rating = " + repr(rating))
