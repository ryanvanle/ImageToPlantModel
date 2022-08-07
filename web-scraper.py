from urllib import response
import requests
import time
import os
import pprint
import csv

# there are two API bugs (with my code) I cannot figure out, nextOffset missing can occur when the values from the
# search request is empty. Second is that it can infinity loop due to the nextOffset not updating
# the current offset even though it is initialized outside the while loop.

plant_names = []
with open('plants-science.csv', 'r') as csv_file:
  csv_reader = csv.reader(csv_file)

  for line in csv_reader:
    plant_names.append(line[0])

for plant in plant_names:

  print(plant)

  #put your own key here
  api_key = ""
  endpoint = "https://api.bing.microsoft.com/"
  url = f"{endpoint}/v7.0/images/search"
  headers = {"Ocp-Apim-Subscription-Key": api_key}

  params = {
    "q": plant,
    "license": "ModifyCommercially",
    "imageType": "photo",
    "safeSearch": "Strict",
  }

  contentUrls = []

  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()

  result = response.json()

  new_offset = 0
  counter = 0

  while new_offset <= 100:
    if (counter > 3):
      break

    # pprint.pprint(result)

    params["offset"] = new_offset

    # print(new_offset)

    if "nextOffset" not in result:
      break

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    result = response.json()

    time.sleep(1)

    new_offset = result["nextOffset"]

    print("current")
    print(result["currentOffset"])

    print("next")
    print(result["nextOffset"])

    print("counter")
    print(counter)
    counter = counter + 1

    for item in result["value"]:
      # print(item["contentUrl"])
      contentUrls.append(item["contentUrl"])

  dir_path = f'./plants/{plant}'

  if not os.path.exists(dir_path):
    os.makedirs(dir_path)

  for url in contentUrls:
    print(url)
    split = url.split("/")
    last_item = split[-1]

    second_split = last_item.split("?")

    if len(second_split) > 1:
      last_item = second_split[0]

    third_split = last_item.split("!")

    if len(third_split) > 1:
      last_item = third_split[0]

    path = os.path.join(dir_path, last_item)

    try:
      with open(path, "wb") as f:
        web_header = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}
        image_data = requests.get(url, headers=web_header)
        #image_data.raise_for_status()

        f.write(image_data.content)
    except OSError:
      pass