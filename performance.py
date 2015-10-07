import requests as r
import os
import zipfile
import shutil
from bs4 import BeautifulSoup
from pandas import DataFrame as df

folder_list=['LIRR','MNR','NYCT']

def load():
    url='http://web.mta.info/persdashboard/perxml/MTA_Performance_Datall.zip'
    with open("Performance.zip", "wb") as code:
        code.write(r.get(url).content)
    zipfile.ZipFile('Performance.zip').extractall(os.path.join('raw_data','Performance'))
    os.rename(
        os.path.join('raw_data','Performance','Performance_MNRR.xml'),\
         os.path.join('raw_data','Performance','Performance_MNR.xml'))
    os.remove("Performance.zip")
def pause(finaldir):
    if not os.path.exists(finaldir):
        os.makedirs(finaldir)
    shutil.copyfile(\
        os.path.join('raw_data','Performance','MTA_Performance_%s.csv'%(finaldir)),\
         os.path.join(finaldir,'MTA_Performance_Pause_%s.csv'%(finaldir)))
def trend(finaldir):
    if not os.path.exists(finaldir):
        os.makedirs(finaldir)
    table=df()
    with open(os.path.join('raw_data','Performance','Performance_%s.xml'%(finaldir))) as f:
        xml=f.read()
    soup = BeautifulSoup(xml)
    for i in soup.findAll('monthly_actual'):
        column=i.parent.parent.parent.parent.indicator_name.text
        index=i.parent.parent.parent.period_year.text+'-'+i.parent.parent.period_month.text
        value=i.text
        table.ix[index,column]=value
    table.to_csv(os.path.join(finaldir,'MTA_Performance_Trends_%s.csv'%(finaldir)))
def main():
    for finaldir in folder_list:
        pause(finaldir)
        trend(finaldir)
if __name__ == '__main__':
    main()