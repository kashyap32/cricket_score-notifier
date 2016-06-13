
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pync import Notifier


cric_info_api = 'http://static.cricinfo.com/rss/livescores.xml'



def notify(text):
	Notifier.notify(text)


def fetch():
	url = cric_info_api

	score_data_raw = requests.get(url)
	score_data_soup = BeautifulSoup(score_data_raw.text)
	score_data = score_data_soup.find_all('description')

	if len(score_data) < 2:
		print('\n\nLooks like no matches are live. Script is exiting!\n\n')
		sys.exit()

	return score_data	


def main():
	old = None
	score = fetch()
	print('\nThese live scores are available now:\n')
	for i, game in enumerate(score[1:], 1): 
		print(i, game.text)

	game_indentifier = int(input('\n\nEnter your choice: '))

	if game_indentifier >= len(score) or game_indentifier < 1:
		print('\nBye!!')
		sys.exit()

	print ('\n\nI will update for every 10 seconds')

	while True:
		score = fetch()
		score = score[game_indentifier].text	
		if score != old:
			old= score
			notify(score)
		time.sleep(10)
	

if __name__ == '__main__':
	main()
