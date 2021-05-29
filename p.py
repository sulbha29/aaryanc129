import csv

data = []

with open("dataset_2.csv", "r") as f:
    csvreader = csv.reader(f)
    for row in csvreader: 
        data.append(row)

headers = data[0]
planetdata = data[1:]

#Converting all planet names to lower case
for i in planetdata:
    i[2] = i[2].lower()

#Sorting planet names in alphabetical order
planetdata.sort(key=lambda planetdata: planetdata[2])


with open("datasetsorted.csv", "a+") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(planetdata)





