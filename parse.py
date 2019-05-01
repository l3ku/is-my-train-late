# -*- coding: utf-8 -*-
# @Author: Leo
# @Date:   2019-03-29 21:12:04
# @Last Modified by:   Leo Toikka
# @Last Modified time: 2019-05-01 09:55:32

import pandas as pd
import numpy as np
from glob import glob
from zipfile import ZipFile
import os

def getData():
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
    data = []
    y_filename = 'y.csv'
    X_filename = 'X.csv'

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

    # Only use these stations as train departure stations
    allowed_stations = weather_df['stationName'].unique()

    # Read trains JSON data
    glob_index = 0
    for file in glob('traindata/digitraffic-rata-trains-*.zip'):
        glob_index += 1
        print("- Opening train data archive {} ({}/{})...".format(file, glob_index, len(glob('traindata/digitraffic-rata-trains-*.zip'))))
        zip_file = ZipFile(file)
        json_file_index = 0
        for json_file in zip_file.infolist():
            json_file_index += 1
            print("  - Working on file {} ({}/{})...".format(json_file.filename, json_file_index, len(zip_file.infolist())))
            df = pd.io.json.read_json(zip_file.open(json_file.filename))
            # We are only interested in trains that can be publicly used, because it doesn't matter if e.g. service trains are late
            df = df[df['trainCategory'].isin(['Commuter', 'Long-distance'])]

            # We are only interested in common public train types IC, S and P
            df = df[df['trainType'].isin(['IC', 'S', 'P'])]

            # We need to have at least 2 stations
            df = df[df['timeTableRows'].apply(lambda x: len(x) >= 2)]

            total_trains = len(df)
            current_train = 0
            for train in df.itertuples():
                current_train += 1
                print("    - Train {}/{}".format(current_train, total_trains), end="\r")
                train_type = train.trainType
                train_category = train.trainCategory
                timetable_rows = pd.DataFrame(train.timeTableRows)

                departure_station = timetable_rows.iloc[0]['stationShortCode']
                if departure_station not in allowed_stations:
                    continue

                # We can't rely on the difference in minutes to be present each time, so default to 0
                how_late_on_average = 0
                if 'differenceInMinutes' in timetable_rows.columns:
                    how_late_on_average = timetable_rows['differenceInMinutes'].mean()

                timetable_rows['scheduledTime'] = timetable_rows['scheduledTime'].astype('datetime64[ns]')
                departure_time = timetable_rows['scheduledTime'][0]
                how_long_trip = timetable_rows['scheduledTime'].iloc[-1] - timetable_rows['scheduledTime'][0]
                row = {
                    'departureTime': departure_time,
                    'type': train_type,
                    'tripDuration': how_long_trip.total_seconds()/60,
                    'departureStation': departure_station,
                    'averageDelayInMinutes': how_late_on_average
                }

                # Find the closest weather measurement time of the departure station
                departure_station_weather = weather_df.loc[weather_df['stationName'] == departure_station]
                date_diff = weather_df['date'] - departure_time
                indexmax = date_diff[date_diff < pd.to_timedelta(0)].idxmax()

                if indexmax < len(departure_station_weather):
                    weather_closest_to_departure = departure_station_weather.iloc[indexmax]

                    row['rainIntensity'] = weather_closest_to_departure['Sateen intensiteetti (mm/h)']
                    row['snowDepth'] = weather_closest_to_departure['Lumensyvyys (cm)']
                    row['temperature'] = weather_closest_to_departure['Ilman lämpötila (degC)']
                    row['visibility'] = weather_closest_to_departure['Näkyvyys (m)']
                    row['windSpeed'] = weather_closest_to_departure['Tuulen nopeus (m/s)']
                    data.append(row)

    df = pd.DataFrame(data).dropna().reset_index(drop=True)
    y = df['averageDelayInMinutes'].to_frame()
    X = df.drop(columns='averageDelayInMinutes')

    X.to_csv(X_filename)
    y.to_csv(y_filename)
