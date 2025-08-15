import os
from dotenv import load_dotenv
import mysql.connector

class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')

    def fetch_city_names(self):

        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(Destination) FROM flight.flights
        UNION
        SELECT DISTINCT(Source) FROM flight.flights
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self, source, destination):

        self.mycursor.execute("""
        SELECT Airline,Route,Dep_Time,Duration,Price FROM flight.flights
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source, destination))

        data = self.mycursor.fetchall()

        return data

    def fetch_airline_frequency(self):

        airline = []
        frequency = []

        self.mycursor.execute("""
        SELECT Airline,COUNT(*) FROM flight.flights
        GROUP BY Airline
        """)

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline,frequency

    def busy_airport(self):

        city = []
        frequency = []

        self.mycursor.execute("""
        SELECT Source,COUNT(*) FROM (SELECT Source FROM flight.flights
							UNION ALL
							SELECT Destination FROM flight.flights) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):

        date = []
        frequency = []

        self.mycursor.execute("""
        SELECT Date_of_Journey,COUNT(*) FROM flight.flights
        GROUP BY Date_of_Journey
        """)

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date, frequency