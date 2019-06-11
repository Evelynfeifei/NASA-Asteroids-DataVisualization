import json
import requests
from Asteroid import Asteroid
import datetime
from tkinter import *
from tkinter.tix import *

#test data
#2018-11-01
#2018-11-02
#3836196   NO.1
#3444440   NO.7	

#create a frame with scroll bar
root = Tk()
frame = Frame(width="400",height="400")
frame.pack()
swin = ScrolledWindow(frame, width="400", height="400")
swin.pack()
main_window = swin.window

root.title('NASA ASTEROIDS')
label_title = Label(main_window, text="NASA ASTEROIDS INFO")
label_title.grid(row=0, column=0, sticky=NW) #E=East; S=South; W=west; N=north

label_sDate = Label(main_window, text="Start Date:")     
label_sDate.grid(row=1, column=0, sticky=NW) 
textbox_sDate = Entry(main_window)
textbox_sDate.grid(row=1, column=1)

label_eDate = Label(main_window, text="End Date:")
label_eDate.grid(row=2, column=0, sticky=NW)
textbox_eDate = Entry(main_window)
textbox_eDate.grid(row=2, column=1)

label_searchById = Label(main_window, text="Search By Asteroid Id:")
label_searchById.grid(row=3, column=0, sticky=NW)
textbox_searchById = Entry(main_window)
textbox_searchById.grid(row=3, column=1)

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Input date is not valid..")
			
results = []
button_Asteroid = []
search_button_Asteroid = []
searchResults = []

#create a new window by clicking on the button of the asteroid object
def SeeDtails(number, link, id, name, nasa_jpl_url, mph, miles):
	
	detail_window = Toplevel(root)
	
	detail_window.title('ASTEROID NO.' + str(number))
	
	label_title = Label(detail_window, text='ASTEROID NO.' + str(number))
	label_title.grid(row=0, column=0, sticky=NW,)
	
	label_link = Label(detail_window, text="Link: " + link)
	label_link.grid(row=1, column=0, sticky=NW,)

	label_id = Label(detail_window, text="ID: " + id)
	label_id.grid(row=2, column=0, sticky=NW)

	label_name = Label(detail_window, text="Name: " + name)
	label_name.grid(row=3, column=0, sticky=NW)
	
	label_nasa_jpl_url = Label(detail_window, text="Nasa_jpl_url: " + nasa_jpl_url)
	label_nasa_jpl_url.grid(row=4, column=0, sticky=NW)
	
	label_mph = Label(detail_window, text="Miles_per_hour: " + mph)
	label_mph.grid(row=5, column=0, sticky=NW)
	
	label_miles = Label(detail_window, text="Miles: " + miles)
	label_miles.grid(row=6, column=0, sticky=NW)

#add command to each button of the asteroid object
def addCommand(n):
	global button_Asteroid
	global results
	button_Asteroid[n]['command'] = lambda: SeeDtails(n+1, results[n][1], results[n][2], results[n][3], results[n][4], results[n][5], results[n][6])
	
def addCommand2(n):
	global search_button_Asteroid
	global searchResults
	search_button_Asteroid[n]['command'] = lambda: SeeDtails(n+1, searchResults[n][1], searchResults[n][2], searchResults[n][3], searchResults[n][4], searchResults[n][5], searchResults[n][6])

def ManipulateDate():
	global results
	global button_Asteroid
	
	#destroy the previous buttons of Asteroid NO.n
	for a in button_Asteroid:
		a.destroy()
	#clean and reset variables
	button_Asteroid=[]
	results=[]
	asteroid_NO= 1

	startdate = textbox_sDate.get()
    #validate the date type of the value
	validate(startdate)
	enddate = textbox_eDate.get()
	validate(enddate)
	
	url = ("https://api.nasa.gov/neo/rest/v1/feed?start_date="+startdate+"&end_date="+enddate+"&api_key=YOUR-API-KEY")
	response = requests.get(url)
	json_data = response.json()
	
	asteroids_data = json_data.get('near_earth_objects')
	
	for date in asteroids_data:
		for asteroid in asteroids_data[date]: 
			results.append([asteroid_NO] + Asteroid(asteroid['links']['self'], asteroid['id'], asteroid['name'], asteroid['nasa_jpl_url'], asteroid['close_approach_data'][0]['relative_velocity']['miles_per_hour'], asteroid['close_approach_data'][0]['miss_distance']['miles']).ToList())
			asteroid_NO += 1
			
	for result in results:
		print(result)
		
	print(asteroid_NO)
	
	for n in range(asteroid_NO-1):
		button_a = Button(main_window, text=("Asteroid No." + str(n + 1)), bg="Blue", fg="White")
		button_a.grid(row= n + 5, column=0, sticky=NW)
		button_Asteroid.append(button_a)
		
	for n in range(len(button_Asteroid)):
		addCommand(n)

def Search():
	global results
	global button_Asteroid
	global searchResults
	global search_button_Asteroid
	
	#destroy the previous buttons of Asteroid NO.n
	for a in button_Asteroid:
		a.destroy()
		
	for a in search_button_Asteroid:
		a.destroy()
		
	#clean and reset variables	
	button_Asteroid=[]
	search_button_Asteroid=[]
	searchResults=[]
	
	asteroid_Id = textbox_searchById.get()
	
	for i in range(len(results)):
		if results[i][2] == asteroid_Id:
			searchResults.append(results[i])
			#create button based on the search result
			button_sp = Button(main_window, text=("Asteroid No." + str(results[i][0])), bg="Blue", fg="White")
			button_sp.grid(row=i+5, column=0, sticky=NW)
			search_button_Asteroid.append(button_sp)
	
	for n in range(len(search_button_Asteroid)):
		addCommand2(n)
							
button_getData = Button(main_window, text="Get Data", bg="Blue", fg="White", command=ManipulateDate)
button_getData.grid(row=2, column=2)

button_Search = Button(main_window, text="Search", bg="Blue", fg="White", command=Search)
button_Search.grid(row=3, column=2)

label_subtitle = Label(main_window, text="ASTEROIDS LIST:")
label_subtitle.grid(row=4, column=0, sticky=NW) #E=East; S=South; W=west; N=north
	
# Puts your UI Window in an infinite loop
root.mainloop()  
