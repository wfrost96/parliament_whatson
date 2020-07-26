import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import datetime

#import results of whatson.py
from whatson import *

scrape_date = datetime.datetime.utcnow().date()
#print(scrape_date)
scrape_time = datetime.datetime.utcnow().time().strftime('%H:%M:%S')
#print(scrape_time)

sender_email = "william.frost.parliament@gmail.com"
receiver_email = "" #you can set a default, should you wish
password = "" #hidden, obviously

#while True:
message = MIMEMultipart("alternative")
message["Subject"] = "Parliamentary agenda - week ahead"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Something went wrong. Please contact the administrator."""

#send a different message depending on what day of the week it is. Sunday send the full week agenda, Monday-Friday send only that day's agenda, Saturday send nothing.
daytoday = datetime.datetime.utcnow().strftime("%A")
#print(daytoday)
daytoday = "Sunday" #this to force send the whole week agenda

if daytoday == "Sunday":
#if daytoday == "Saturday":
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - week ahead</h1>
        <p>Data accurate as of %s on %s.</p>

        <h2>Monday - Commons</h2>
            <p>%s</p>
        <h2>Monday - Lords</h2>
            <p>%s</p>

        <h2>Tuesday - Commons</h2>
            <p>%s</p>
        <h2>Tuesday - Lords</h2>
            <p>%s</p>

        <h2>Wednesday - Commons</h2>
            <p>%s</p>
        <h2>Wednesday - Lords</h2>
            <p>%s</p>

        <h2>Thursday - Commons</h2>
            <p>%s</p>
        <h2>Thursday - Lords</h2>
            <p>%s</p>

        <h2>Friday - Commons</h2>
            <p>%s</p>
        <h2>Friday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, monday_commons_big_str, monday_lords_big_str, tuesday_commons_big_str, tuesday_lords_big_str, wednesday_commons_big_str, wednesday_lords_big_str, thursday_commons_big_str, thursday_lords_big_str, friday_commons_big_str, friday_lords_big_str)
elif daytoday == "Monday":
    #print("Monday")
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - Monday</h1>
        <p>Data accurate as of %s on %s.</p>
        <h2>Monday - Commons</h2>
            <p>%s</p>
        <h2>Monday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, monday_commons_big_str, monday_lords_big_str)
elif daytoday == "Tuesday":
    print("Tuesday")
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - Tuesday</h1>
        <p>Data accurate as of %s on %s.</p>
        <h2>Tuesday - Commons</h2>
            <p>%s</p>
        <h2>Tuesday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, tuesday_commons_big_str, tuesday_lords_big_str)
elif daytoday == "Wednesday":
    print("Wednesday")
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - Wednesday</h1>
        <p>Data accurate as of %s on %s.</p>
        <h2>Wednesday - Commons</h2>
            <p>%s</p>
        <h2>Wednesday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, wednesday_commons_big_str, wednesday_lords_big_str)
elif daytoday == "Thursday":
    print("Thursday")
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - Thursday</h1>
        <p>Data accurate as of %s on %s.</p>
        <h2>Thursday - Commons</h2>
            <p>%s</p>
        <h2>Thursday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, thursday_commons_big_str, thursday_lords_big_str)
elif daytoday == "Friday":
    print("Friday")
    html = """\
    <html>
      <head>
        <style>
          table {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
            }

          table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
          }

          table tr:nth-child(even){background-color: #f2f2f2;}

          table tr:hover {background-color: #ddd;}

          #lords_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #b50938;
            color: white;
          }

          #commons_table thead {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #006e46;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Parliamentary agenda - week ahead</h1>
        <p>Data accurate as of %s on %s.</p>
        <h2>Friday - Commons</h2>
            <p>%s</p>
        <h2>Friday - Lords</h2>
            <p>%s</p>
      </body>
    </html>
    """ % (scrape_time, scrape_date, friday_commons_big_str, friday_lords_big_str)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
#time.sleep(30)

print("Email successfully sent.")
