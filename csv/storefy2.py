
# coding: utf-8

# In[26]:

#from create_csv import *
import time, os
from datetime import datetime, date
import numpy as np

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
    #df = {'columns':[], 
     #     "values": {'mandag':[],'tirsdag':[],
    #                 'onsdag':[],'torsdag':[],'fredag':[]}}
    with open(csv_file) as infile:
        data = infile.readlines()
        #df['columns'] = data[0].replace('\n','').split(',')[1:]
        for line in data[1:]:
            row = line.replace('\n','').split(',')
            dag.append(row[0])
            fra.append(row[1])
            til.append(row[2])
            emne.append(row[4])
            
    #df2 = pd.DataFrame.from_csv(csv_file)
    df = {'dag':dag,'fra':fra,'til':til,'emne':emne}
    return df
df  = read_csv()
print df


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

def figprint(txt):
    os.system("figlet -m 12 '%s' -f big -w 140 | lolcat"  %txt)
df = read_csv()

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
    #time_passed = np.amax(tds_prev)
    os.system('clear')
    if now < stop_dts[prev_i]:
        figprint( "DO NOT ENTER\n%s lecture most likely in progress"%ssubjets[prev_i])
    if np.ma.count(tds_next) == 0:
        figprint( "No more lectures this week. \nSoftware now needs updating.")
    if start_dates[next_i] == today:
        figprint( "Next lecture:\n  %s  \nstarts today at %s (in %d s)" %(subjects[next_i],start_dts[next_i].time(),time_left))
    else:
        figprint( "Next lecture:\n  %s \nstarts %s (in %d s)" %(subjects[next_i], start_dts[next_i],time_left))
    time.sleep(5)
    


# In[ ]:



