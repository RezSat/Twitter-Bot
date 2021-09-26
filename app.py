import tweepy
import requests
from bs4 import BeautifulSoup
import argparse
import json
import random
import os
import sys
import time
from user_agent import generate_user_agent
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


# Authenticate to Twitter
auth = tweepy.OAuthHandler("API KEY", "API SECRET")
auth.set_access_token("ACCESS TOKEN", "ACCESS TOKEN SECRET")
api = tweepy.API(auth)


def jokes():
  my_file = 'jokes.json'
  with open(my_file,'rb') as g:
    j = json.load(g)
  stop = len(j)
  start = 0
  x = random.randint(start, stop)
  return (j[x]["body"])


def quotes():  
  my_file = 'quotes.json'
  with open(my_file) as f:
    q = json.load(f)
  stop = len(q)
  start = 0
  x = random.randint(start, stop)
  quote = q[x]["text"]+"\n\t- "+q[x]["author"]
  return quote
  
@sched.scheduled_job('interval', minutes=120)
def Twitter(keyword=''):
	r = requests.get("https://thoughts.sushant-kumar.com/"+keyword).content
	p = BeautifulSoup(r, 'html.parser')
	tweet = (p.text.splitlines()[26])[1:-1]
	api.update_status(tweet)
	
sched.start()
