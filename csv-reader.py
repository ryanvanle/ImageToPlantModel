import csv

results = []

with open('plants.csv', 'r') as csv_file:
  csv_reader = csv.reader(csv_file)

  for line in csv_reader:
    results.append(line[0])

print(results)
