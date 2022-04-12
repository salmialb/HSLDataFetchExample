# SanomaPythonTest
Assignment for the Junior Data Engineer position at Sanoma.
The code contains comments.

# Instructions
Run the script from a terminal by being in the project directory and running the command: ***python main.py***
The CSV will be saved in the working directory.

### Docker
If running via Docker use the commands below:

***docker build -t pythontest .***

***docker run --name pythontest --mount source=pythonTestVol,target=/app pythontest*** <- This will save the csv into a volume named pythonTestVol



If you don't want to get access to the csv file simply run:

***docker build -t pythontest .***

***docker run pythontest***

# Dependencies
requests

pandas

datetime

os

# Script explanation

## getData()
Fetches the data for March 2020 by generating a range of dates and iterating through them. 
One call per iteration.
Responses are stored in a list.
Checks that the response contains something filtering out days when the train doesn't run.

## normalizeData()
Normalizes the data using pandas normalize.
Handling of the nested list "timetableRowa" by first exploding it and then applying putting it back into individual columns.

## saveToCsv()
Saves the normalized data to a .csv in the working directory.

***!!!If running via Docker, the file has to be stored in a volume(check instructions).!!!***

## avgActualArrivalTime()
Calculate the average actual arrival time at the end station.

1. Filter for arrivals at end station HKI
2. Define variable for storing arrival times as timedelta. timedelta makes it simple to do calculations on time.
3. Split the string to get rid of the empty milliseconds fields and the timezone indicator Z and the days & years
4. Convert the string to timedelta, including microseconds for a more accurate average
5. Sum up the arrival times
6. Calculate the average arrival time by dividing the sum with the amount of arrivals
