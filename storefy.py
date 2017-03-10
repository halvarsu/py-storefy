#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from create_csv import *
import time, os
from datetime import datetime, date

def read_csv():
    places = {'storefy':['BL24','V343'],
             'sophuslie':['BL15','101']}

    building, room = places['storefy']
    week = get_current_week()
    year = get_current_year()
    csv_file = get_filename(room,building,week,year,'csv')
    df = pd.DataFrame.from_csv(csv_file)
    return df


def get_datetime(DOW, week, year, clock):
    return datetime.strptime('{} {} {} {}:00'.format(year, week, DOW, clock), '%Y %W %w %X')

def get_date(DOW, week, year):
    return datetime.strptime('{} {} {}'.format(year, week, DOW), '%Y %W %w')

def getDatesAndDts(series):
    weekdays = {'mandag':1,'tirsdag':2,'onsdag':3,'torsdag':4,'fredag':5}

    DOWs = [weekdays[key] for key in df.fra.keys()]
    week = get_current_week()
    year = get_current_year()

    dts = []
    dates = []

    for DOW, clock in zip(DOWs, series.values):
        dt = get_datetime(DOW, week, year,clock)
        date = get_date(DOW,week,year)
        dts.append(dt)
        dates.append(date)   
    return  dates, dts

df = read_csv()
while True:
    now = datetime.now()
    today = date.today()

    subjects = df['emne/kontaktperson']
    start_dates, start_dts= getDatesAndDts(df.fra)
    stop_dates, stop_dts = getDatesAndDts(df.til)

    timedeltas = np.array([dt - now for dt in start_dts])
    secondsleft = np.array([td.total_seconds() for td in timedeltas])

    tds_next = np.ma.masked_array(secondsleft)
    tds_next[secondsleft < 0] = np.ma.masked
    tds_prev = np.ma.masked_array(secondsleft)
    tds_prev[secondsleft > 0] = np.ma.masked

    next_i =  np.argmin(tds_next)
    time_left = np.amin(tds_next)
    prev_i = np.argmax(tds_prev)
    #time_passed = np.amax(tds_prev)
    os.system('clear')
    if now < stop_dts[prev_i]:
        print "DO NOT ENTER, %s lecture most likely in progress"%ssubjets[prev_i]
    if np.ma.count(tds_next) == 0:
        print "No more lectures this week. Software now needs updating."
    if start_dates[next_i] == today:
        print "Next lecture, %s, starts today at %s, in %d seconds" %(subjects[next_i],start_dts[next_i].time(),time_left)
    else:
        print "Next lecture, %s, starts %s, in %d seconds" %(subjects[next_i], start_dts[next_i],time_left)
    time.sleep(1)
    

