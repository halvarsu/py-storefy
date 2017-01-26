"""Prints info about status in store fysiske lesesal from csv-files
TODO: - automatic download of csv-files
      - two-column cow-printing"""
import time, os
from datetime import datetime, date
import numpy as np
import argparse
from cows import Cow

parser = argparse.ArgumentParser()
parser.add_argument("-m","--mode",help="set mode for figlet",
		    default="12")
parser.add_argument("-f","--font",help="set font for figlet",
		    default="big")

def get_current_week():
    import datetime
    return datetime.date.today().isocalendar()[1]
     
def get_current_year():
    import datetime
    return datetime.date.today().isocalendar()[0]
def get_filename(room,building,week,year,filetype='html'):
    return '{0}/{1}{2}week{3}yr{4}.{0}'.format(filetype,building,
                                               room,week,year)

def read_csv():
    places = {'storefy':['BL24','V343'],
             'sophuslie':['BL15','101']}

    building, room = places['storefy']
    week = get_current_week()
    year = get_current_year()
    csv_file = get_filename(room,building,week,year,'csv')
    dag = []
    fra = []
    til = []
    emne = []
    with open(csv_file) as infile:
        data = infile.readlines()
        #df['columns'] = data[0].replace('\n','').split(',')[1:]
        for line in data[1:]:
            row = line.replace('\n','').split(',')
            dag.append(row[0])
            fra.append(row[1])
            til.append(row[2])
            emne.append(row[4])
            
    df = {'dag':dag,'fra':fra,'til':til,'emne':emne}
    return df
df  = read_csv()
print(df)


def get_datetime(DOW, week, year, clock):
    return datetime.strptime('{} {} {} {}:00'.format(year, week, DOW, clock), '%Y %W %w %X')

def get_date(DOW, week, year):
    return datetime.strptime('{} {} {}'.format(year, week, DOW), '%Y %W %w')

def getDatesAndDts(times,dager):
    weekdays = {'mandag':1,'tirsdag':2,'onsdag':3,'torsdag':4,'fredag':5}

    DOWs = [weekdays[key] for key in dager]
    week = get_current_week()
    year = get_current_year()

    dts = []
    dates = []

    for DOW, clock in zip(DOWs, times):
        dt = get_datetime(DOW, week, year,clock)
        date = get_date(DOW,week,year)
        dts.append(dt)
        dates.append(date)   
    return  dates, dts



def toiprint(txt ,border=False):
    #os.system("figlet -m 12 -f big '%s' -t | lolcat"  %txt)
    if border:
    	os.system("toilet -F border -f big '%s' -t | lolcat"  %txt)
    #    os.system("toilet -f pagga -F gay:border -t '%s' "%(txt))
    else:
    	os.system("toilet -f big '%s' -t | lolcat"  %txt)
    #    os.system("toilet -f pagga -F gay -t '%s' "%(txt))


df = read_csv() 

cow = Cow()


while True:
    now = datetime.now()
    today = date.today()

    subjects = df['emne']
    start_dates, start_dts= getDatesAndDts(df['fra'],df['dag'])
    stop_dates, stop_dts = getDatesAndDts(df['til'],df['dag'])

    timedeltas = np.array([dt - now for dt in start_dts])
    secondsleft = np.array([td.total_seconds() for td in timedeltas])

    tds_next = np.ma.masked_array(secondsleft)
    tds_next[secondsleft < 0] = np.ma.masked
    tds_prev = np.ma.masked_array(secondsleft)
    tds_prev[secondsleft > 0] = np.ma.masked

    next_i =  np.argmin(tds_next)
    time_left = np.amin(tds_next)
    prev_i = np.argmax(tds_prev)
    os.system('clear')

    if time_left:
        mins = int((time_left // 60)%60)
        hours = int(time_left     // 3600)
        time_str = "%s"
        time_str %= str(hours) + " hours %s" if hours else "%s"
        time_str %= str(mins) + " mins left." if mins else "."
        if time_str == '.':
            time_str = "NOW!"
    print("Klokken er naa "+str(now)[11:19])

    #The different cases of printing
    if now < stop_dts[prev_i]:
        toiprint("DO NOT ENTER", border = True)
        toiprint( "%s lecture \nmost likely in progress." %(subjects[prev_i]))
        cow.speak( "Lecture ends %s"%(stop_dts[prev_i].time()),
                   lolcat=True, width = 100)
    elif np.ma.count(tds_next) == 0:
        cow.speak( "No more lectures this week. ",
                  lolcat=True, width = 100)
    else:
        cow.speak("kl %s "%(start_dts[next_i]).time()
                +'  %s '%subjects[next_i] , 
                 lolcat =True, width = 100)
        toiprint(time_str )
    time.sleep(60)
