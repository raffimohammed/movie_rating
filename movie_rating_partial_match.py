#!/usr/bin/env python2
import sys, requests, logging
level = logging.INFO
level = logging.DEBUG
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=level)
base_url="http://www.omdbapi.com/?apikey=8cfbd1c9&type=movie" 
def lookup_rating_by_id(id): 
	base_url="http://www.omdbapi.com/?apikey=8cfbd1c9&type=movie" 
	rating_bool = False
	rating = -1
	title_url = base_url + "&i=" + id
	logging.debug( 'title_url = ' + title_url)
	response_id = requests.get(title_url)
	ratings = response_id.json()['Ratings']
	for i in range(len(ratings)): 
		if ratings[i]['Source'] == 'Rotten Tomatoes': 
			rating = ratings[i]['Value']
			rating_bool = True
	return rating_bool, rating 
def lookup_rating_by_search(title): 
	rating_dict = {} # This is what we will be returning
	logging.debug('title = ' + title)
	logging.debug('base_url = ' + base_url)
	search_url = base_url + "&s=" + title
	logging.debug( "search_url = " + search_url )
	response_search = requests.get(search_url)
	logging.debug('response_search = ' + repr(response_search.json() ))
	if logging.getLogger().level == logging.DEBUG :
		for key, value in response_search.json().items() : 
			logging.debug( repr(key) +  " = " +  repr(value) )

	if response_search.json()['Response'] == "True"  :
		totalResults = response_search.json()['totalResults']
		logging.debug( "totalResults = " + totalResults )
		logging.debug( "response_search.json['totalResults'] = " + response_search.json()['totalResults'] )
		totalResults = int(totalResults)
		modulus = totalResults % 10
		if modulus  == 0: 
			pages = totalResults / 10 
		else: 
			pages = ( totalResults / 10 )  + 1
		logging.debug('pages = ' + str(pages))
		for i in range(pages): 
			search_url_page = search_url +  "&page=" + str(i+1)	
			logging.debug('search_url_page = ' + search_url_page)
			response_search_page = requests.get(search_url_page)
			logging.debug('response_search_page = ' + repr(response_search_page.json()) )
			for j in range(modulus ):	
				logging.debug('j = ' + str(j))
				if response_search_page.json()['Response'] == "True" : 
					rating_bool, rating = lookup_rating_by_id(response_search_page.json()['Search'][j]['imdbID'] )
					if rating_bool == True : 
						print 'The movie ' + response_search_page.json()['Search'][j]['Title'] + ' has a Rotten Tomatoes rating of ' + rating + '.'
						# If the key is already present it just means there could be multiple movies with the same title.
						if response_search_page.json()['Search'][j]['Title'] in rating_dict :
							rating_dict[response_search_page.json()['Search'][j]['Title']].append(rating)
						else:
							# Putting it in a list rather than assinging a value directly as there could be multiple movies with the same title
							temp_rating_list = [rating]
							rating_dict[response_search_page.json()['Search'][j]['Title']] = temp_rating_list
					else:
						print 'The movie ' + response_search_page.json()['Search'][j]['Title'] + ' does not have a Rotten Tomatoes rating.' 
				else:
					logging.error(response_search_page.json()['Error']			)
					
	else:
		logging.error(response_search.json()['Error'] )
	return rating_dict

if __name__ == "__main__" : 
	title = sys.argv[1:]
	title = ' '.join(title)
	rating_dict = lookup_rating_by_search(title)		
	logging.debug( 'rating_dict = ' + repr(rating_dict))
