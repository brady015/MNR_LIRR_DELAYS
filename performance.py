import requests as r
import os
import zipfile
import shutil
folder_list=['LIRR','MNR','NYCT']

def load():
    url='http://web.mta.info/persdashboard/perxml/MTA_Performance_Datall.zip'
    with open("Performance.zip", "wb") as code:
        code.write(r.get(url).content)
    zipfile.ZipFile('Performance.zip').extractall(os.path.join('raw_data','Performance'))
    os.remove("Performance.zip")
def movedata(folder_list):
    for finaldir in folder_list:
        if not os.path.exists(finaldir):
            os.makedirs(finaldir)
        os.rename(os.path.join('raw_data','Performance','MTA_Performance_%s.csv'%(finaldir)), os.path.join(finaldir,'MTA_Performance_%s.csv'%(finaldir)))
def main():
    load()
    movedata(folder_list)
if __name__ == '__main__':
    main()