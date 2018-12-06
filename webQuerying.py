from time import gmtime, strftime
import time
import configparser
import geocoder
import urllib.request
import requests, json 
import sys
import os

def finddistance():
  noError = True
  while noError:
    try:
      # Take source as input 
      source = input("Enter your locatio: ") 
        
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
      print("Check your spelling")
      continue

def main():
  finddistance()



main()