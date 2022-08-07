import re
import csv
import requests
import pprint
plant_names = []
with open('plants.csv', 'r') as csv_file:
  csv_reader = csv.reader(csv_file)

  for line in csv_reader:

    regexLine = re.search("\(([^()]+)\)", line[0]).group()
    regexLine = regexLine.replace("(","")
    regexLine = regexLine.replace(")","")

    print(regexLine)
    plant_names.append(regexLine)

print(plant_names)

# url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG/1280px-Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG"
# split = url.split("/")
# last_item = split[-1]

# second_split = last_item.split("?")

# if len(second_split) > 1:
#   last_item = second_split[0]

# print(last_item)

# third_split = last_item.split("!")

# if len(third_split) > 1:
#   last_item = third_split[0]

#   print(last_item)


# four_split = last_item.split("px-")

# if len(four_split) > 1:
#   last_item = four_split[-1]

# print(last_item)

# web_header = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

# result = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG/1280px-Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG", headers=web_header);

# pprint.pprint(result)




