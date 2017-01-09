# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

filename = 'test.html'
def row2txt(row):
    row_texts = [td.text for td in row.find_all('div')]
    return row_texts 

def get_filename(room,building,week,year,filetype='html'):
    return '{0}/{1}{2}week{3}yr{4}.{0}'.format(filetype,building,
                                               room,week,year)
def get_current_week():
    import datetime
    return datetime.date.today().isocalendar()[1]
     
def get_current_year():
    import datetime
    return datetime.date.today().isocalendar()[0]

def get_url(room, building, week, year):
    base ='https://tp.uio.no/timeplan/romutskrift.php?id={2}&room={2}{0}&week={1}&year={3}'
    return base.format(room,week,building,year)

def download_room(room_name,week=None,building ='BL24',year=None, verbose = True):
    import os
    places = {'storefy':['BL24','V343'],
             'sophuslie':['BL15','101']}
    if room_name in places:
        building, room = places[room_name]
    else:
        room = room_name
    if not week:
        week = get_current_week()
    if not year:
        year = get_current_year()
    
    url = get_url(room,building,week,year)
    outfile = get_filename(room,building,week,year)
    cmd = "wget '{}' -O '{}' -q".format(url, outfile)
    print 'executing command: \n'+cmd+'\n'
    result = os.system(cmd)
    
    if result == 256:
        raise IOError, 'Could not access folder %s ' %folder
        raise IOError, 'Could not download file'
    if verbose:
        roomstr = '{}, {},'.format(room, room_name) if room!=room_name else room
        print '-'*60
        print "Successfully downloaded html for room {} in \nbuilding {}, week {}, {}".format(roomstr, building, week, year)
        print '-'*60
    return outfile


def html2df(filename, verbose = True):
    if verbose:
        print '-'*60
        print ("Converting html '{}' to data frame".format(filename))
        print '-'*60
    try:
        page = open(filename) 
    except IOError:
        import sys
        print("Failed to load file '{}', exiting".format(filename))
        sys.exit()
    soup = BeautifulSoup(page, 'html.parser')
    page.close()

    tables = soup.find_all('div',  {'class': 'tp-table' })
    if len(tables) == 0:
        raise IOError, 'Something is wrong with web page, found no tables'
    dfs = []
    for table in tables:
        trs = table.find_all('div', {'class':'tp-row'})
        th = row2txt(trs[0]) 
        trs = [row2txt(tr) for tr in trs[1:]]
        #for tr in trs[1:]:
         #   print (row2txt(tr))
        df = pd.DataFrame(trs, columns = th, index=range(len(trs)))
        dfs.append(df)
    dager = ['mandag','tirsdag','onsdag','torsdag','fredag']
    df = pd.concat(dfs, keys = dager)
    df.columns = [s.lower() for s in df.columns]
    #df.reset_index(level=1, drop=True)
    s = df.tid
    interval = s.values
    start,stop = np.array([t.split('-') for t in s.values]).T
    start = [s.replace(' ','') for s in start]
    stop = [s.replace(' ','') for s in stop]
    df.insert(0, 'fra', start)
    df.insert(1, 'til', stop)
    df = df.drop('tid', axis = 1)
    df = df.reset_index(level=1,drop=True)
    return df



def create_csv(room):
    html_file  = download_room(room)
    df = html2df(html_file)

    csv_file = html_file[:-4]+'csv' 
    # outfile.replace('html','csv') was considered dangerous if 
    # string contains html elsewhere
    df.to_csv(csv_file)
    print df


if __name__ == "__main__":
    import sys 
    import argparse

    parser = argparse.ArgumentParser()

    if len(sys.argv) > 1:
        room = sys.argv[1]
    else:
        room = 'storefy'
    html_file  = download_room(room)
    df = html2df(html_file)

    csv_file = html_file.replace('html','csv') 
    print '-'*60
    print "Saving csv to file '%s'"% csv_file 
    df.to_csv(csv_file)
    print '-'*60
    print df


