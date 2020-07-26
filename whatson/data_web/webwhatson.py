#import results of whatson.py
from whatson import *

import time
import datetime

scrape_date = datetime.datetime.utcnow().date()
#print(scrape_date)
scrape_time = datetime.datetime.utcnow().time().strftime('%H:%M:%S')
#print(scrape_time)

week_big_str = """\
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
""" % (scrape_time, scrape_date, monday_commons_big_str, monday_lords_big_str, tuesday_commons_big_str, tuesday_lords_big_str, wednesday_commons_big_str, wednesday_lords_big_str, thursday_commons_big_str, thursday_lords_big_str, friday_commons_big_str, friday_lords_big_str)

print(week_big_str)
