# -*- coding: utf-8 -*-
# @Author: Leo
# @Date:   2019-03-29 21:12:04
# @Last Modified by:   Leo Toikka
# @Last Modified time: 2019-04-30 14:03:10

import pandas as pd
import numpy as np
from glob import glob
from zipfile import ZipFile
import os

def getData():
    y = [] # y will contain the mean amount that the train is late during its trip
    X = [] # X will contain information about the date, train model, train category, total trip duration and weather conditions.
    y_filename = 'y.csv'
    X_filename = 'X.csv'

    X_df = None
    y_df = None

    # Prefer to read cached values, but if there are none, we have to read the full
    # dataset.
    if os.path.isfile(X_filename) and os.path.isfile(y_filename):
        X_df = pd.read_csv(X_filename, index_col=0)
        y_df = pd.read_csv(y_filename, index_col=0)
    return (X_df, y_df)


if __name__ == '__main__':
    # Read the weather from known stations
    weather_df = pd.DataFrame()
    for file in glob('weatherdata/*'):
        station_name = os.path.basename(file).split('.')[0]
        df = pd.read_csv(file, dtype='unicode', engine='python')
        df['stationName'] = station_name
        weather_df = weather_df.append(df)

    # Use a better date format with GMT+2 applied instead of UTC
    weather_df['year'] = weather_df['Vuosi']
    weather_df['month'] = weather_df['Kk']
    weather_df['day'] = weather_df['Pv']
    weather_df['date'] = pd.to_datetime(weather_df[['year', 'month', 'day']]) + pd.to_timedelta(weather_df['Klo'] + ':00') + pd.DateOffset(hours=2)

    weather_df = weather_df.drop(columns=['Aikavyöhyke', 'Vuosi', 'Kk', 'Pv', 'Klo', 'year', 'month', 'day'])
    weather_df = weather_df.fillna(0)

    # Only use these stations as train departure stations
    allowed_stations = weather_df['stationName'].unique()

    # Read trains JSON data
    for file in glob('traindata/digitraffic-rata-trains-*.zip'):
        zip_file = ZipFile(file)
        for json_file in zip_file.infolist():
            df = pd.io.json.read_json(zip_file.open(json_file.filename))

            # We are only interested in trains that can be publicly used, because it doesn't matter if e.g. service trains are late
            df = df[df['trainCategory'].isin(['Commuter', 'Long-distance'])]

            for train in df.itertuples():
                train_type = train.trainType
                train_category = train.trainCategory
                timetable_rows = pd.DataFrame(train.timeTableRows)

                # We need to have at least 2 stations
                if len(timetable_rows) < 2:
                    continue

                departure_station = timetable_rows.iloc[0]['stationShortCode']
                if departure_station not in allowed_stations:
                    continue

                # We can't rely on the difference in minutes to be present each time, so default to 0
                how_late_on_average = 0
                if 'differenceInMinutes' in timetable_rows.columns:
                    how_late_on_average = timetable_rows['differenceInMinutes'].mean()
                y.append(how_late_on_average)

                timetable_rows['scheduledTime'] = timetable_rows['scheduledTime'].astype('datetime64[ns]')
                departure_time = timetable_rows['scheduledTime'][0]
                how_long_trip = timetable_rows['scheduledTime'].iloc[-1] - timetable_rows['scheduledTime'][0]
                row = {
                    'departureTime': departure_time,
                    'type': train_type,
                    'tripDuration': how_long_trip.total_seconds()/60,
                    'departureStation': departure_station
                }

                # Find the closest weather measurement time of the departure station
                departure_station_weather = weather_df.loc[weather_df['stationName'] == departure_station]
                weather_closest_to_departure = departure_station_weather.loc[departure_station_weather['date'] == departure_time.round('H')]
                if len(weather_closest_to_departure) == 1:
                    row['rainIntensity'] = weather_closest_to_departure['Sateen intensiteetti (mm/h)'].values[0]
                    row['snowDepth'] = weather_closest_to_departure['Lumensyvyys (cm)'].values[0]
                    row['temperature'] = weather_closest_to_departure['Ilman lämpötila (degC)'].values[0]
                    row['visibility'] = weather_closest_to_departure['Näkyvyys (m)'].values[0]
                    row['windSpeed'] = weather_closest_to_departure['Tuulen nopeus (m/s)'].values[0]

                    X.append(row)

    pd.DataFrame(X).to_csv(X_filename)
    pd.DataFrame(y, columns=['averageDelayInMinutes']).to_csv(y_filename)
