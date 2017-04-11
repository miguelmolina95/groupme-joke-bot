#Name: Will Shellabarger
#uniqname: wnshell


from bs4 import BeautifulSoup
import urlparse
import sys, os, urllib2
import time


def appropriateJoke(tags): 
	if "racist" in tags or "dirty" in tags or "sex" in tags: 
		return False 
	return True 


if __name__ == "__main__":
	#timekeeping
	start_time = time.time()

	#get seed document and number to stop at 
	seedURLs = sys.argv[1]
	numToCrawl = int(sys.argv[2])

	#initialize empty list of URLs to try
	urlList = []

	#keep list of URLs that were actually visited
	visited = []

	#print directed edge pairs for pagerank.py
	jokes = open('jokes.txt', 'w')

	#place all seed URLs into list
	with open(seedURLs) as file:
		urlList = file.readlines()
		urlList = [x.strip() for x in urlList]

	#iterate through URL frontier and collect links
	i = 0
	jokeIDs = []
	while i < len(urlList) and len(visited) < numToCrawl and len(jokeIDs) < 3000:
		#how far along are we
		if(len(visited) % 100 == 0):
			print "---- " + str(len(visited)) + " pages visited ----\n"

		#cache url for faster indexing
		url = urlList[i]

		#set timeout for visiting links to speed up crawler
		try:
			webPage = urllib2.urlopen(url, timeout=3.05)
		except:
			#if http doesn't work, try with https
			try:
				urlSecure = url.replace('http', 'https', 1)
				webPage = urllib2.urlopen(urlSecure, timeout=3.05)
			except:
				#continue past this page if unable to open
				i += 1
				continue
				

		#only crawl HTML pages
		if 'html' in webPage.headers.getheader('Content-Type'):
			content = webPage.read()
			soup = BeautifulSoup(content, 'html.parser')

			#if an HTML page, add to list of 'visited' links
			visited.append(url)

			for joke in soup.find_all("div", { "class" : "oneliner" }):
				jokeID = joke.find('b').get('id')

				# Taking out inappropriate jokes 
				tags = joke.find('span', {'class' : 'links'})
				jokeTags = tags.text.replace("Tags: ", "").encode('utf-8').strip() + '\n'	

				if appropriateJoke(jokeTags): 
					if jokeID not in jokeIDs:
						jokeIDs.append(jokeID)
						jokes.write(joke.find('p').text.encode('utf-8').strip() + "|")
						tags = joke.find('span', {'class' : 'links'})
						jokes.write(tags.text.replace("Tags: ", "").encode('utf-8').strip() + '\n')

			#find all href links in that page
			for link in soup.find_all('a', href=True):

				#incorporate relative paths from links
				link = urlparse.urljoin(url, link['href'])

				#remove fragments
				link = urlparse.urldefrag(link)[0]

				#normalize all links to use http rather than https, remove trailing slash
				link = link.replace('https', 'http', 1).strip('/')

				#get rid of unicode from bs4
				link = link.encode('utf-8')

				#only add to frontier if eecs.umich domain and not already seen and not 'www' duplicate (probably causing slow runtime)
				if 'onelinefun' in urlparse.urlparse(link).netloc: 
					#append to end of list for breadth first search 
					urlList.append(link)
		i += 1

	out = open("crawler.output", "w")
	for link in visited:
		out.write(link + '\n')
	print "---- " + str(len(visited)) + " pages visited ----"
	print "--- %s seconds ---" % (time.time() - start_time)















