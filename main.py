import requests
from bs4 import BeautifulSoup
import lxml
from spotifyActions import SpotifyMachine


URL = "https://www.billboard.com/charts/hot-100/"


#Input date to check song titles
# date = input("Which date do you want to travel to? No wrong answers! Please type in this format YYYY-MM-DD: ")
date = "2000-08-12"
URL += date

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

titles = []

#Get info only from the results table
results_list = soup.find(name="div", class_="chart-results-list")

#Get info only from the appropriate rows
results_list = results_list.find_all("li", class_="o-chart-results-list__item")
for tag in results_list:
    title = tag.find(name="h3", id="title-of-a-story", class_="c-title")
    #If it doesnt find a title,gets None which we dont want,also the format for the title is \ntitle\n so we have to get rid of \n
    if title != None : titles.append(title.getText().split("\n")[1])

print(titles)

machine = SpotifyMachine(titles,date)
machine.create_top_100()