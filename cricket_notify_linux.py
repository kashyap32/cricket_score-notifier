#!/usr/bin/env python

import os
import sys

from time import sleep

import requests
from bs4 import BeautifulSoup
from gi.repository import Notify





cric_info_api = 'http://static.cricinfo.com/rss/livescores.xml'




Notify.init("score-notifier")

def notify(text):
	Notify.Notification.new(text).show()


def fetch():
	url = cric_info_api

	score_data_raw = requests.get(url)
	score_data_soup = BeautifulSoup(score_data_raw.text)
	score_data = score_data_soup.find_all('description')

	if len(score_data) < 2:
		print('\nLooks like no matches are live.')
		sys.exit()

	return score_data	


def main():
	old = None
	score_data = fetch()
	print('\nThese live scores are available now:\n')


	for i, game in enumerate(score_data[1:], 1): 
		print(i, game.text)

	game_indentifier = int(input('\n\nEnter your choice: '))

	if game_indentifier >= len(score_data) or game_indentifier < 1:
		print('\nBye!!!')
		sys.exit()
	f=int(input("Enter freq.in seconds"))
	print ('\n\nGreat! I will update score for every %s \n\n' % (f))

	while True:
		score_data = fetch_score_data()
		score = score_data[game_indentifier].text
		if score != old:
			old = score
			notify(score)
		sleep(f)



if __name__ == '__main__':
	main()
