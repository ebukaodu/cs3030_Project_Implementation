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

status = False


def usage():
    print("URL  Web Querying")
    print("-r Route| --route Route of two cities. This gives detailed directions")
    print("-l Location | --locate The IP address the script should locate.")
    print("-f FILE | --file File containing urls and IP addresses for location look up.")
    print("-v | --verbose prints more verbose output")   
    print("-h | --help prints the usage statement and exit")
    sys.exit()



def finddistance():
  global status
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


      print ("Route: " + source + " to " + dest)
      for item in data:
        result = (item["instruction"]["text"])
        print(result) 
  
      print("The distance is " + str(round((0.621371 * dis), 2)) + " miles")
      print("It will take " + time.strftime("%H hours %M minutes %S seconds", time.gmtime(duration)))
      if status:
        print("The end of Querying the web")
      noError = False
    except:
      print("Check your spelling \n Only enter the name of the cities.")
      continue



def getIpLocation(url):
  global status
  try:
    #removing the https and //
    ip = url.split("//")[-1].split("/")[0].split('?')[0]
    #if a url, get the ip
    ip = socket.gethostbyname(ip)
    #look up information on the ip
    ip = 'http://ip-api.com/json/' + ip
    
    req = requests.get(ip)
    out =  req.json()
    country = out['country']
    region = out['regionName']
    city = out['city']
    zipcod = out['zip']

    lat = out['lat']
    lon = out['lon']
    status = out['status']
    timezone = out['timezone']
    ipAdd = out["query"]

    print ("Country: " + country + "\n" + "State: " + region + "\n" +
    "City: " + city + "\n" + "Zip: " + zipcod)
    if status:
      print("More information on " + url)
      print("Latitude: " + lat + "\n" + "Longitude: "+ lon + "\n" + 
      "Web URL/IP status: " + status + "\n" + "Time Zone: "  + timezone + 
      "\n" + "IP address" + ipAdd )

    if status:
      print("The end of Querying the web")
  except:
    print("Check the URL " + url + "\n Error finding it's geolocation.")

def getIpFile(filename):
  global status
  try:
    with open(filename, 'r') as f:
        for url in f:
          #removing the https and //
          ip = url.split("//")[-1].split("/")[0].split('?')[0]
          #if a url, get the ip
          ip = socket.gethostbyname(ip)
          #look up information on the ip
          ip = 'http://ip-api.com/json/' + ip
    
          req = requests.get(ip)
          out =  req.json()
          country = out['country']
          region = out['regionName']
          city = out['city']
          zipcod = out['zip']

          lat = out['lat']
          lon = out['lon']
          status = out['status']
          timezone = out['timezone']
          ipAdd = out["query"]

          print("Looking up " + url)
          print ("Country: " + country + "\n" + "State: " + region + "\n" + 
          "City: " + city + "\n" + "Zip: " + zipcod)

          if status:
            print("More information on " + url)
            print("Latitude: " + lat + "\n" + "Longitude: "+ lon + "\n" + 
            "Web URL/IP status: " + status + "\n" + "Time Zone: "  + timezone + 
            "\n" + "IP address" + ipAdd )

    if status:
      print("The end of Querying the web")
  except:
    print("Check the URL " + url + "\n Error finding it's geolocation.")


def main():
  global status
  ok = False
  parser = argparse.ArgumentParser(description="Description for my parser", add_help=False)
  parser.add_argument("-r", "--route", action="store_true", help="Example: route argument")
  parser.add_argument("-l", "--locate", help="Example: locate argument", nargs='?')
  parser.add_argument("-f", "--file", help="Example: file argument", nargs='?')
  parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
  parser.add_argument("-h", "--help", action="store_true", help="Example: help argument")
  args = parser.parse_args(sys.argv[1:])

  print("Web Querying:")
  print(strftime("%a, %d %B, %Y %H:%M:%S", gmtime()))

  #the configparser argument handling
  if args.verbose:
    status = True

  if args.route:
    routes = True
  if routes:
    if status:
      print("Query Bing Map to get a route between cities.")
    finddistance()

  if ok:
    if status:
     print("Country Lookup using IPs - Enter an IP address and find the country that IP is registered in. \ni.e. getting the Geo Location of an IP Address")

  if args.locate:
    locate = args.locate
    ok = True
    getIpLocation(locate)

  if args.file:
    fileName = args.file
    ok = True
    getIpFile(fileName)

  if args.help:
    usage()
    

if __name__ == "__main__":
  if sys.argv[1] == '-h' or sys.argv[1] == "--help":
    usage()
  else:
    main()
