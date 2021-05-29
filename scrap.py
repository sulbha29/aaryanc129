     
 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("C:/Users/HOME/3D Objects/c127/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink"]
planet_data = []
newplanetdata = []
def scrape():
    for i in range(1,439):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentpageno = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
            if currentpageno<i:
                 browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpageno>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_link_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_link_tag.find_all("a",href = True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i}pagedone")
def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(browser.page_source,"html.parser")
        temp_list = []
        for trtag in soup.find_all("tr",attrs = {"class":"fact_row"}):
            tdtag = trtag.find_all("td")
            for x in tdtag:
                try:
                    temp_list.append(x.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        newplanetdata.append(temp_list)
    except:
        time.sleep(2)
        scrapmoredata(hyperlink)
scrape()
for index,data in enumerate(planet_data):
    scrapmoredata(data[5])
    print(f"{index+1} pagedata")        
finalplanetdata = []
for index,data in enumerate(planet_data):
    newplanetdataelement = newplanetdata[index]
    newplanetdataelement = [elem.replace("\n","") for elem in newplanetdataelement]
    newplanetdataelement = newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)
    
        
with open("final.csv", "w") as f:
    
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)
