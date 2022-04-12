# -*- coding: utf-8 -*-
import requests
import pandas as pd
import datetime
import os
from requests.exceptions import HTTPError

def main():
    responses = getData()
    df = normalizeData(responses)
    saveToCSV(df)
    avgActualArrivalTime(df)
    

def getData():
    '''
    Fetching data from digitraffic api
    '''
    responses = []                                                  #List for storing the responses
    marchDates = pd.date_range(start='3/1/2020', end='3/31/2020')   #Generate a range of dates for the month of March to loop through
    headers = {'Digitraffic-User': 'Trainguy/PythonTest'}           #Headers
    
    print("Fetching data...")
    for date in marchDates:                                                                             #Loop through March 
        TMS_STATION_URL = 'https://rata.digitraffic.fi/api/v1/trains/{date}/4'.format(date=date.date()) #Change the date for each iteration
        try:                                                                                            #Error handling
            r = requests.get(TMS_STATION_URL, headers=headers)                                          #Make the api call
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print ("Encountered error: {error}" .format(error=e.response.text))
        if len(r.json()) >= 1:                                                                          #No trains on Sundays. Check that there actually is something in the response before appending.
            responses.append(r.json()[0])                                                               #Append the result for each day to the responses list
    print("Fetching of data succesful!")
    return responses
    
def normalizeData(responses):
    '''
    Normalizing the data
    '''
    df = pd.json_normalize(responses).explode('timeTableRows')              #Normalize the data
    df = pd.concat([df, df.pop("timeTableRows").apply(pd.Series)], axis=1)  #Getting the nested list timeTableRows on the same level as the other data
    return df

def saveToCSV(df):
    '''
    Saving the normalized data to .CSV
    '''
    file_dir = os.path.dirname(os.path.abspath(__file__))          #Get path of working directory
    file_path = os.path.join(file_dir, file_dir, 'trainData.csv')  #Join the path of the working directory with the desired file name
    df.to_csv(file_path, encoding='utf-8')                         #Save file
    print("Data saved to CSV at:{path} ".format(path=file_path))

def avgActualArrivalTime(df):
    '''
    Calculate the average acutal arrival time at the end station
    '''
    dfHki = df.loc[df['stationShortCode']=='HKI']                                                                   #Filter for arrivals at end destination
    s = dfHki.reset_index(drop=True)['actualTime']                                                                  #Reset index to be 1,2,3... instead of the old index
    tsum = datetime.timedelta()                                                                                     #Variable for storing the sum of the arrival times
    for time in s:
        t = datetime.datetime.strptime(time.split(".")[0], '%Y-%m-%dT%H:%M:%S').strftime('%H:%M:%S')                #Split the string to get rid of the milliseconds(which are always 0), the  timezone indicator Z(Zulu) and the days & years.
        t = datetime.datetime.strptime(t,'%H:%M:%S')                                                                #The result of the last line is a string. Convert it into datetime
        tdelta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)   # Convert to timedelta for calculations. Include microseconds for a more accurate average.
        tsum = tsum + tdelta                                                                                        # Sum up the arrival times
    taverage = tsum / len(s)                                                                                        # Calculate the average arrival time
    print("Average actual arrival time for March 2020: {time} ".format(time=taverage))                          
        
        
if __name__ == "__main__":
    main()