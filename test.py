import requests as r
import os
import zipfile
url='http://web.mta.info/persdashboard/perxml/MTA_Performance_Datall.zip'
with open("Performance.zip", "wb") as code:
    code.write(r.get(url).content)
zipfile.ZipFile('Performance.zip').extractall('Perfermance')
os.remove("Performance.zip")