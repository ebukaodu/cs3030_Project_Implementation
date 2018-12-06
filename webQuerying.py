#!/usr/bin/python3
import time
import urllib
import pygeoip
import configparser
import json
from contextlib import closing
import urllib.request
import sys
import requests
import socket
import re

def finddistance():
  noError = True
  while noError:
    try:
      # Take source as input 
      source = input("Enter your location: ") 
        
      # Take destination as input 
      dest = input("Enter your destination: ") 
      bingMapsKey = "AhVX9FEsa2eAKmaWFGIu6_93KjYMCHJkoGnWG7hUJspEcBzm-EW-KUw_qEgUjpFN"
      #now = datetime.now()
      url = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + source + "&wp.1=" + dest + "&key=" + bingMapsKey
      request = urllib.request.Request(url)
      response = urllib.request.urlopen(request)

      r = response.read().decode(encoding="utf-8")
      result = json.loads(r)
      data = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
      dis = result["resourceSets"][0]["resources"][0]["travelDistance"]
      duration = result["resourceSets"][0]["resources"][0]["travelDuration"]

      for item in data:
        result = (item["instruction"]["text"])
        print(result) 

      print("The distance is " + str(round((0.621371 * dis), 2)) + " miles")
      print("It will take " + time.strftime("%H hours %M minutes %S seconds", time.gmtime(duration)))
      noError = False
    except:
      print("Check your spelling \n Only enter the name of the cities.")
      continue



def getIpLocation(url):
  url = url.split("//")[-1].split("/")[0].split('?')[0]
  url = socket.gethostbyname(url)
  url = 'http://ip-api.com/json/' + url
  
  req = requests.get(url)
  out =  req.json()
  country = out['country']
  region = out['regionName']
  city = out['city']
  zipcod = out['zip']

  lat = out['lat']
  lon = out['lon']
  status = out['status']
  timezone = out['timezone']
  ip = out["query"]

  print (country,region,city,zipcod)
  print(lat,lon,status,timezone,ip)

  

def main():
  finddistance()
  url = "https://www.weber.edu/"
  getIpLocation(url)


main()
