import requests
from bs4 import BeautifulSoup, SoupStrainer
import mysql.connector
import re
import datetime
import time

link_base = "https://calendar.parliament.uk/calendar/"
links = []
dates = []
for i in range(0,10):
    future_date_raw = datetime.datetime.utcnow().date() + datetime.timedelta(days=i)
    #print(future_date_raw)
    day = future_date_raw.strftime('%a')
    if day == "Sat":
        break
    else:
        future_date = future_date_raw.strftime('%Y/%m/%d')
        dates.append(future_date)
        dates.append(future_date) #nb, done twice as there is a day in the Commons and a day in the Lords
        link_1 = link_base + "Commons/All/" + future_date + "/Daily"
        links.append(link_1)
        link_2 = link_base + "Lords/All/" + future_date + "/Daily"
        links.append(link_2)
#print(links)
#print(dates)
"""dates.append("2020/5/18")
links.append("https://calendar.parliament.uk/calendar/Commons/All/2020/5/18/Daily")"""

events_list = []
for i in range(0, len(links)):

    daily_agenda = []

    day_today = datetime.datetime.strptime(dates[i], '%Y/%m/%d').strftime('%A')
    daily_agenda.append(day_today)

    webpage = requests.get(links[i])
    soup = BeautifulSoup(webpage.content, "html.parser")

    all_events = soup.select("table[class=table] > tr")
    for event in all_events:
        #print(event)

        mycounter = 0

        #get event time
        house_times = event.select("td[class=col-xs-3] > p[class=parl-calendar-event-time]")
        if house_times:
            for house_time in house_times:
                house_times_list = house_time.text.split()
                str1 = ""
                for item in house_times_list:
                    str1 += str(item)
                #print(str1)
                daily_agenda.append(str1)
                mycounter += 1
        else:
            #print("THEN")
            daily_agenda.append("THEN")
            mycounter += 1

        #get event name
        house_events_subs = event.select("td[class=col-xs-9] > p[class=parl-calendar-event-title] > span[class=parl-calendar-event-subtitle]")
        if len(house_events_subs) != 1:
            #print("Title")
            house_events = event.select("td[class=col-xs-9] > p[class=parl-calendar-event-title]")
            for house_event in house_events:
                #print(house_event)
                for item in house_event:
                    #print(item.strip())
                    daily_agenda.append(item.strip())
                    mycounter += 1
        else:
            #print("Subtitle")
            house_events = event.select("td[class=col-xs-9] > p[class=parl-calendar-event-title]")
            for house_event in house_events:
                #print(house_event)
                mylist = []
                for item in house_event:
                    mylist.append(item)
                #print(mylist[0].strip())
                daily_agenda.append(mylist[0].strip())
                mycounter += 1
            for house_event in house_events_subs:
                #print(house_event)
                for item in house_event:
                    #print(item.strip())
                    daily_agenda.append(item.strip())
                    mycounter += 1

        #get event description
        house_events_description = event.select("td[class=col-xs-9] > p[class=parl-calendar-event-description]")
        for house_event in house_events_description:
            #print(house_event)
            str1 = ""
            for item in house_event:
                if len(item)==0:
                    continue
                elif len(item)==1:
                    str1 += item.text
                else:
                    str1 += item.strip()
            daily_agenda.append(str1)
            mycounter += 1

        #print(mycounter)
        if mycounter == 2:
            daily_agenda.append("Private")

    events_list.append(daily_agenda)
    #print(daily_agenda)
#print(events_list)

#now clean up the text and shorten things so it's quick to read
events_list_new = []
for day in events_list:
    events_list_day = []
    for item in day:
        #print(item)

        #procedure and terminology
        if " - Private Meeting" in item:
            item = item.replace(" - Private Meeting", "")
        if "- virtual proceeding -" in item:
            item = item.replace("- virtual proceeding -", "- ")
        if "- Virtual proceeding -" in item:
            item = item.replace("- Virtual proceeding -", "- ")
        if "- virtual proceedings -" in item:
            item = item.replace("- virtual proceedings -", "- ")
        if "- Virtual proceedings -" in item:
            item = item.replace("- Virtual proceedings -", "- ")
        if " - Oral evidence" in item:
            item = item.replace(" - Oral evidence", "")
        if "Oral questions" in item:
            item = item.replace("Oral questions", "Orals")
        if "To approve a Statutory Instrument relating" in item:
            item = item.replace("To approve a Statutory Instrument relating", "SI")
        if "Prime Minister's Question Time" in item:
            item = item.replace("Prime Minister's Question Time", "PMQs")
        if "Orders and regulations" in item:
            item = item.replace("Orders & regulations", "Orders and regs")

        #gov and parly
        if "The Government" in item:
            item = item.replace("The Government", "Gov")
        if "Government" in item:
            item = item.replace("Government", "Gov")
        if "government" in item:
            item = item.replace("government", "Gov")
        if "Committee" in item:
            item = item.replace("Committee", "Comm")
        if "Parliamentary" in item:
            item = item.replace("Parliamentary", "Parly")
        if "Parliament" in item:
            item = item.replace("Parliament", "Parly")
        if "Chancellor of the Exchequer" in item:
            item = item.replace("Chancellor of the Exchequer", "Rishi")
        if "House of Commons" in item:
            item = item.replace("House of Commons", "HoC")
        if "House of Lords" in item:
            item = item.replace("House of Lords", "HoL")
        if "(Commons)" in item:
            item = item.replace("(Commons)", "")
        if "(Lords)" in item:
            item = item.replace("(Lords", "")
        if "Secretary of State" in item:
            item = item.replace("Secretary of State", "SoS")

        #government departments
        if "HM Treasury" in item:
            item = item.replace("HM Treasury", "Treasury")
        if "(EU Withdrawal)" in item:
            item = item.replace("(EU Withdrawal)", "Brexit")
        if "Housing, Communities and Local Government" in item:
            item = item.replace("Housing, Communities and Local Government", "HCLG")
        if "Housing, Communities & Local Gov" in item:
            item = item.replace("Housing, Communities & Local Gov", "HCLG")
        if "Work and Pensions" in item:
            item = item.replace("Work and Pensions", "DWP")
        if "Environment, Food and Rural Affairs" in item:
            item = item.replace("Environment, Food and Rural Affairs", "DEFRA")
        if "Digital, Culture, Media and Sport" in item:
            item = item.replace("Digital, Culture, Media and Sport", "DCMS")
        if "Health and Social Care" in item:
            item = item.replace("Health and Social Care", "Health")
        if "Business, Energy and Industrial Strategy" in item:
            item = item.replace("Business, Energy and Industrial Strategy", "BEIS")
        if "International Relations" in item:
            item = item.replace("International Relations", "IR")
        if "Crown Prosecution Service" in item:
            item = item.replace("Crown Prosecution Service", "CPS")

        #coronavirus
        if "Coronavirus (COVID-19)" in item:
            item = item.replace("Coronavirus (COVID-19)", "corona")
        if "Coronavirus (Covid-19)" in item:
            item = item.replace("Coronavirus (COVID-19)", "corona")
        if "the COVID-19 pandemic" in item:
            item = item.replace("the COVID-19 pandemic", "corona")
        if "the Coronavirus Outbreak" in item:
            item = item.replace("the Coronavirus Outbreak", "corona")
        if "coronavirus outbreak" in item:
            item = item.replace("coronavirus outbreak", "corona")
        if "COVID-19" in item:
            item = item.replace("COVID-19", "corona")
        if "Covid-19" in item:
            item = item.replace("Covid-19", "corona")
        if "Coronavirus" in item:
            item = item.replace("Coronavirus", "corona")

        #names and places
        if "Northern Ireland Affairs" in item:
            item = item.replace("Northern Ireland Affairs", "NI")
        if "Northern Ireland" in item:
            item = item.replace("Northern Ireland", "NI")
        if "International" in item:
            item = item.replace("International", "Int'l")
        if "international" in item:
            item = item.replace("international", "int'l")
        if "black, Asian and minority ethnic" in item:
            item = item.replace("black, Asian and minority ethnic", "BAME")
        if "Scottish Affairs" in item:
            item = item.replace("Scottish Affairs", "Scotland")
        if "Scottish" in item:
            item = item.replace("Scottish", "Scot")
        if "European Union" in item:
            item = item.replace("European Union", "EU")

        #other
        if "The " in item:
            item = item.replace("The ", "")
        if " the " in item:
            item = item.replace(" the ", " ")
        if " and " in item:
            item = item.replace(" and ", " & ")
        if " any " in item:
            item = item.replace(" any ", " ")
        if " with " in item:
            item = item.replace(" with ", " w ")
        if "Technology" in item:
            item = item.replace("Technology", "tech")
        if "Technologies" in item:
            item = item.replace("Technologies", "tech")
        if "Economic" in item:
            item = item.replace("Economic", "Econ")
        if "Communications" in item:
            item = item.replace("Communications", "Comms")
        if "Universal Credit" in item:
            item = item.replace("Universal Credit", "UC")
        if "do not" in item:
            item = item.replace("do not", "don't")
        if "-" in item:
            item = item.replace("-", "- ")
        if "-  " in item:
            item = item.replace("-  ", "- ")
        if "Sub- Comm" in item:
            item = item.replace("Sub- Comm", "Sub-Comm")
        if "," in item:
            item = item.replace(",", ", ")
        if ",  " in item:
            item = item.replace(",  ", ", ")
        if "Mr " in item:
            item = item.replace("Mr ", "")

        events_list_day.append(item)
    events_list_new.append(events_list_day)
#print(events_list_new)
events_list = events_list_new
#print(len(events_list))

monday_commons_big_str = ""
tuesday_commons_big_str = ""
wednesday_commons_big_str = ""
thursday_commons_big_str = ""
friday_commons_big_str = ""
monday_lords_big_str = ""
tuesday_lords_big_str = ""
wednesday_lords_big_str = ""
thursday_lords_big_str = ""
friday_lords_big_str = ""

for i in range(0, len(events_list)):
    #print(i)
    if i % 2 == 0: #this is commons
        #print("commons")
        #print(events_list[i])
        if events_list[i][0] == "Monday":
            #print("this is monday")
            monday_commons_agenda = events_list[i]
            monday_commons_agenda.pop(0)
            mynumber = int((len(monday_commons_agenda))/3)
            item = "<table id='commons_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(monday_commons_agenda[0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            monday_commons_big_str += item
            #print(monday_commons_big_str)
        elif events_list[i][0] == "Tuesday":
            #print("this is tuesday")
            tuesday_commons_agenda = events_list[i]
            tuesday_commons_agenda.pop(0)
            mynumber = int((len(tuesday_commons_agenda))/3)
            item = "<table id='commons_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(tuesday_commons_agenda[0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            tuesday_commons_big_str += item
            #print(tuesday_commons_big_str)
        elif events_list[i][0] == "Wednesday":
            #print("this is wednesday")
            wednesday_commons_agenda = events_list[i]
            wednesday_commons_agenda.pop(0)
            mynumber = int((len(wednesday_commons_agenda))/3)
            item = "<table id='commons_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(wednesday_commons_agenda[0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            wednesday_commons_big_str += item
            #print(wednesday_commons_big_str)
        elif events_list[i][0] == "Thursday":
            #print("this is thursday")
            thursday_commons_agenda = events_list[i]
            thursday_commons_agenda.pop(0)
            mynumber = int((len(thursday_commons_agenda))/3)
            item = "<table id='commons_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(thursday_commons_agenda[0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            thursday_commons_big_str += item
            #print(thursday_commons_big_str)
        else:
            #print("this is friday")
            friday_commons_agenda = events_list[i]
            friday_commons_agenda.pop(0)
            mynumber = int((len(friday_commons_agenda))/3)
            item = "<table id='commons_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(friday_commons_agenda[0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            friday_commons_big_str += item
            #print(friday_commons_big_str)
    else: #this is lords
        #print("lords")
        #print(events_list[i])
        if events_list[i][0] == "Monday":
            #print("this is monday")
            monday_lords_agenda = events_list[i]
            monday_lords_agenda.pop(0)
            #print(monday_lords_agenda)
            mynumber = int((len(events_list[i])/3))
            #print(mynumber)
            item = "<table id='lords_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(events_list[i][0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            #print(item)
            monday_lords_big_str += item
            #print(monday_lords_big_str)
        elif events_list[i][0] == "Tuesday":
            #print("this is tuesday")
            tuesday_lords_agenda = events_list[i]
            tuesday_lords_agenda.pop(0)
            #print(tuesday_lords_agenda)
            mynumber = int((len(events_list[i])/3))
            #print(mynumber)
            item = "<table id='lords_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(events_list[i][0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            #print(item)
            tuesday_lords_big_str += item
            #print(tuesday_lords_big_str)
        elif events_list[i][0] == "Wednesday":
            #print("this is wednesday")
            wednesday_lords_agenda = events_list[i]
            wednesday_lords_agenda.pop(0)
            #print(wednesday_lords_agenda)
            mynumber = int((len(events_list[i])/3))
            #print(mynumber)
            item = "<table id='lords_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(events_list[i][0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            #print(item)
            wednesday_lords_big_str += item
            #print(wednesday_lords_big_str)
        elif events_list[i][0] == "Thursday":
            #print("this is thursday")
            thursday_lords_agenda = events_list[i]
            thursday_lords_agenda.pop(0)
            #print(thursday_lords_agenda)
            mynumber = int((len(events_list[i])/3))
            #print(mynumber)
            item = "<table id='lords_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(events_list[i][0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            #print(item)
            thursday_lords_big_str += item
            #print(thursday_lords_big_str)
        else:
            #print("this is friday")
            friday_lords_agenda = events_list[i]
            friday_lords_agenda.pop(0)
            #print(friday_lords_agenda)
            mynumber = int((len(events_list[i])/3))
            #print(mynumber)
            item = "<table id='lords_table'><thead><td><p>Time</p></td><td><p>Event</p></td><td><p>Description</p></td></thead><tbody>"
            for j in range(0, mynumber):
                item += "<tr>"
                for k in range(0, 3):
                    item += "<td>"
                    item += str(events_list[i][0])
                    item += "</td>"
                    events_list[i].pop(0)
                item += "</tr>"
            item += "</tbody><table>"
            #print(item)
            friday_lords_big_str += item
            #print(friday_lords_big_str)
