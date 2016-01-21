import requests as r
import os
import zipfile
import shutil
from bs4 import BeautifulSoup
from pandas import DataFrame as df

folder_list=['LIRR','MNR','NYCT']
column_order={
    'NYCT':['Collisions with Injury Rate - NYCT Bus', 'Customer Accident Injury Rate - NYCT Bus', 'Customer Injury Rate - Subways', 'Employee Lost Time and Restricted Duty Rate', 'Elevator Availability - Subways', 'Escalator Availability - Subways', 'Bus Passenger Wheelchair Lift Usage - NYCT Bus', '% of Completed Trips - NYCT Bus', '100th Street Depot - % of Completed Trips', '126th Street Depot - % of Completed Trips', 'Casey Stengel Depot - % of Completed Trips', 'Castleton Depot - % of Completed Trips', 'Charleston Depot - % of Completed Trips', 'East New York Depot - % of Completed Trips', 'Flatbush Depot - % of Completed Trips', 'Fresh Pond Depot - % of Completed Trips', 'Grand Avenue Depot - % of Completed Trips', 'Gun Hill Depot - % of Completed Trips', 'Jackie Gleason Depot - % of Completed Trips', 'Jamaica Depot - % of Completed Trips', 'Kingsbridge Depot - % of Completed Trips', 'Manhattanville Depot - % of Completed Trips', 'Meredith Avenue Depot - % of Completed Trips', 'Michael J. Quill Depot - % of Completed Trips', 'Queens Village Depot - % of Completed Trips', 'Ulmer Park Depot - % of Completed Trips', 'West Farms Depot - % of Completed Trips', 'Yukon Depot - % of Completed Trips', 'Mean Distance Between Failures - NYCT Bus', 'Mean Distance Between Failures - Staten Island Railway', 'Mean Distance Between Failures - Subways', 'On-Time Performance - Staten Island Railway', 'On-Time Performance (Terminal)', 'OTP (Terminal) - 1 Line', 'OTP (Terminal) - 2 Line', 'OTP (Terminal) - 3 Line', 'OTP (Terminal) - 4 Line', 'OTP (Terminal) - 5 Line', 'OTP (Terminal) - 6 Line', 'OTP (Terminal) - 7 Line', 'OTP (Terminal) - A Line', 'OTP (Terminal) - B Line', 'OTP (Terminal) - C Line', 'OTP (Terminal) - D Line', 'OTP (Terminal) - E Line', 'OTP (Terminal) - F Line', 'OTP (Terminal) - G Line','OTP (Terminal) - J Z Line', 'OTP (Terminal) - L Line', 'OTP (Terminal) - M Line', 'OTP (Terminal) - N Line','OTP (Terminal) - Q Line','OTP (Terminal) - R Line', 'OTP (Terminal) - S Fkln Line', 'OTP (Terminal) - S Line 42 St.', 'OTP (Terminal) - S Line Rock', 'Subway Wait Assessment', 'Subway Wait Assessment - 1 Line', 'Subway Wait Assessment - 2 Line', 'Subway Wait Assessment - 3 Line', 'Subway Wait Assessment - 4 Line', 'Subway Wait Assessment - 5 Line', 'Subway Wait Assessment - 6 Line', 'Subway Wait Assessment - 7 Line', 'Subway Wait Assessment - A Line', 'Subway Wait Assessment - B Line', 'Subway Wait Assessment - C Line', 'Subway Wait Assessment - D Line', 'Subway Wait Assessment - E Line', 'Subway Wait Assessment - F Line', 'Subway Wait Assessment - G Line', 'Subway Wait Assessment - J Z Line', 'Subway Wait Assessment - L Line', 'Subway Wait Assessment - M Line', 'Subway Wait Assessment - N Line', 'Subway Wait Assessment - Q Line', 'Subway Wait Assessment - R Line', 'Subway Wait Assessment - S 42 St', 'Subway Wait Assessment - S Fkln', 'Subway Wait Assessment - S Rock', 'Wait Assessment - Subways (Inactive, Historic Calculations)', 'Total Paratransit Ridership - NYCT Bus', 'Total Ridership - NYCT Bus', 'Total Ridership - Subways'],
    'MNR':['Customer Injury Rate', 'Employee Lost Time and Restricted Duty Rate', 'Elevator Availability', 'Escalator Availability', 'Harlem Line - OTP', 'Hudson Line - OTP', 'New Haven Line - OTP', 'Pascack Valley Line - OTP', 'Port Jervis Line - OTP', 'On-Time Performance (East of Hudson)', 'On-Time Performance (West of Hudson)', 'Mean Distance Between Failures', 'Total Ridership'],
    'LIRR':['Customer Injury Rate', 'Employee Lost Time and Restricted Duty Rate', 'Elevator Availability', 'Escalator Availability', 'Babylon Branch - OTP', 'Far Rockaway Branch OTP', 'Greenport/Ronkonkoma Branch - OTP', 'Hempstead Branch - OTP', 'Hicksville/Huntington Branch - OTP', 'Long Beach Branch - OTP', 'Montauk Branch - OTP', 'Oyster Bay Branch - OTP', 'Port Jefferson Branch - OTP', 'Port Washington Branch - OTP', 'West Hempstead Branch - OTP', 'On-Time Performance', 'Mean Distance Between Failures', 'Total Ridership']
}
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
        try:
            column=i.parent.parent.parent.parent.indicator_name.text
            index=i.parent.parent.parent.period_year.text+'-'+i.parent.parent.period_month.text
            value=i.text
            table.ix[index,column]=value
        except:
            pass
    table.columns=[i.strip() for i in table.columns.tolist()]
    table[column_order[finaldir]].to_csv(os.path.join(finaldir,'MTA_Performance_Trends_%s.csv'%(finaldir)))
def main():
    load()
    for finaldir in folder_list:
        pause(finaldir)
        trend(finaldir)
if __name__ == '__main__':
    main()