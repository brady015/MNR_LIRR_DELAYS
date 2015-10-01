#data parser for Metro North Railroad Delayed and Canceled Train Information
import urllib
import urllib2
from datetime import timedelta, date
from bs4 import BeautifulSoup as bs
from pandas import DataFrame as df
import sys
import os

#######lir_parser/mnr_parser---->daterange--->load_page---->save_file

#date generater
def daterange(start_date, end_date):
    for n in range(0,int ((end_date - start_date).days),25):
        yield start_date + timedelta(n),start_date + timedelta(n+24)

#downloading page and converting to beautifulsoup
def mnr_load_page(vDate1,vDate2):
    url = 'http://as0.mta.info/mnr/schedules/latez/demo_late_trains.cfm'
    values = {'vDate1' : vDate1.strftime("%m/%d/%Y"),
              'vDate2' : vDate2.strftime("%m/%d/%Y"),
              'vBranch' : 0 }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = bs(the_page, 'html.parser')
    return soup


#downloading page and converting to beautifulsoup
def lir_load_page(vDate1,vDate2):
    url = 'http://wx3.lirr.org/lirr/LateTrains/'
    values = {'date' : vDate1.strftime("%m/%d/%Y"),
              'to_date' : vDate2.strftime("%m/%d/%Y")}
    the_page=urllib2.urlopen(urllib2.Request('http://wx3z.lirr.org/latetrains/?'+urllib.urlencode(values))).read()
    soup = bs(the_page, 'html.parser')
    return soup

## mnr_file_writer
def save_file(soup,csvfile):
    for i in soup.find_all('tr',class_=["rowza","rowzb"]):
        time=i.td.string
        branch=i.td.next_sibling.next_sibling.string.strip()
        late=i.text.split('\n')[-2]
        csvfile.write(','.join([time,branch,late])+'\n')


## wrap around of web scraping for mnr
def mnr_parser(start_date, end_date,des_dir):
    with open(des_dir, 'w+') as csvfile:
        for vDate1,vDate2 in daterange(start_date, end_date):
        # print vDate1,vDate2
            print '%s~~~~%s'%(vDate1,vDate2)
            soup=mnr_load_page(vDate1,vDate2)
            save_file(soup,csvfile)
    print 'saved\n\n'


## wrap around of web scraping for lirr
def lir_parser(start_date, end_date,des_dir):
    with open(des_dir, 'w+') as csvfile:
        for vDate1,vDate2 in daterange(start_date, end_date):
            print '%s~~~~%s'%(vDate1,vDate2)
            soup=lir_load_page(vDate1,vDate2)
            for i in soup.body.find_all('tr')[1:]:
                date=i.find_all('td')[0].string.strip()
                date=date[0:6]+'20'+date[-2:]
                branch=i.find_all('td')[1].string.strip()
                late=i.find_all('td')[-1].string.strip()
                csvfile.write(','.join([date,branch,late])+'\n')
    print 'saved\n\n'


#trival function for mins switch
def range_switcher(x):
    if 5<x<=10:
        return '6-10'
    elif 10<x<=15:
        return '11-15'
    elif 15<x<=20:
        return '16-20'
    elif 20<x<=25:
        return '21-25'
    elif 25<x<=30:
        return '26-30'
    else:
        return '31+'


#late or cancelled switcher
def formatting(x):
    if 'Late' in x:
        minutes=float(x.split('-')[1].strip().split()[0].strip())
        return range_switcher(minutes)
    else:
        return x

#creating folder of different branchs
def pivot(filename, finaldir):
    table=df.from_csv(filename,header=None,index_col=None)
    table.columns=['date','branch','late']
    table['count']=0
    table.loc[:,'date']=table.date.apply(lambda x:x.split('/')[-1]+'-'+x.split('/')[0])
    table.loc[:,'mins']=table.late.apply(formatting)
    del table['late']
    new_table=table.groupby(by=['branch','date','mins']).agg('count').reset_index()
    new_table['branch-late']=new_table['branch']+'   '+new_table['mins']
    del new_table['mins']
    if not os.path.exists(finaldir):
        os.makedirs(finaldir)
    for branch_ in new_table.branch.unique():
        new_table[new_table['branch']==branch_].pivot(index='date',\
            columns='branch-late',\
            values='count').to_csv('%s/%s.csv'%(finaldir,branch_))

def main():
    for branch in branch_list:
        start_date = start_date_dict[branch]
        parser=parser_dict[branch]
        des_dir='%s.csv'%(branch)
        end_date=date.today()
        #branch / start_date / end_date ready
        parser(start_date,end_date,des_dir)
        print 'start creating folder'
        pivot(des_dir,branch)
        print 'done, please check %s folder\n\n\n\n\n'%(branch)


if __name__ == '__main__':
    ####dictionary stored for switching###3
    
    branch_list=['LIRR','MNR']
    start_date_dict={
        'MNR': date(2014, 1, 1),
        'LIRR': date(2010, 1, 1)
    }
    parser_dict={
        'MNR':mnr_parser,
        'LIRR':lir_parser
    }

    main()