Leo Toikka
leo.toikka@tuni.fi
# Johdanto datatieteeseen – harjoitustyön vaihe 2
Harjoitustyön toisessa vaiheessa tarkoituksena oli kerätä data. Pitkän mietiskelyn jälkeen päädyin valitsemaan harjoitustyöni aiheeksi tarkastella junan lähtöaseman säätilan vaikutusta myöhästymisen määrään, jopa mahdollisesti pyrkiä ennustamaan junien myöhästymismäärää säätilan ja junadatan yhdistelmänä saatujen piirteiden avulla. Tätä varten tarvitsisin junien kulkutiedoista ja junien lähtöaseman paikkakunnalta säädataa.

## Datan kerääminen
Valmista datasettiä, joka sisältäisi junien kulkutietojen lisäksi säädatan, ei oletetusti löytynyt, joten tarpeeseen tulisi tehdä juna- ja säädatan yhdistelyä. Vanhojen junien kulkutietoja löytyi [Digitrafficin arkistoista](https://rata.digitraffic.fi/api/v1/trains/dumps/list.html). Arkistossa oli kaikkien junien kulkutiedot vuodesta 2015 lähtien, mutta valtavan datamäärän vuoksi päädyin lataamaan sieltä vain vuosien 2017 ja 2018 junien kulkutiedot. Säädata vastaaville vuosille löytyi [Ilmatieteen laitoksen latauspalvelusta](https://ilmatieteenlaitos.fi/havaintojen-lataus#!/). VR:n verkksivuilla olevasta [kaukoliikenteen ratakartasta](https://www.vr.fi/cs/vr/fi/kaukoliikenteen-reittikartta) löytyi tärkeimmät asemat, joten päädyin lataamaan Ilmatieteen laitoksen sivustolta yhden havaintopaikan datan vuosilta 2017 ja 2018 jokaista tärkeää asemaa kohden. Lopulta datasetit olivat tietokoneellani:
```
$ tree -l .
.
├── traindata
│   ├── digitraffic-rata-trains-2017-01-01.zip
│   ├── digitraffic-rata-trains-2017-02-01.zip
│   ├── digitraffic-rata-trains-2017-03-01.zip
│   ├── digitraffic-rata-trains-2017-04-01.zip
│   ├── digitraffic-rata-trains-2017-05-01.zip
│   ├── digitraffic-rata-trains-2017-06-01.zip
│   ├── digitraffic-rata-trains-2017-07-01.zip
│   ├── digitraffic-rata-trains-2017-08-01.zip
│   ├── digitraffic-rata-trains-2017-09-01.zip
│   ├── digitraffic-rata-trains-2017-10-01.zip
│   ├── digitraffic-rata-trains-2017-11-01.zip
│   ├── digitraffic-rata-trains-2017-12-01.zip
│   ├── digitraffic-rata-trains-2018-01-01.zip
│   ├── digitraffic-rata-trains-2018-02-01.zip
│   ├── digitraffic-rata-trains-2018-03-01.zip
│   ├── digitraffic-rata-trains-2018-04-01.zip
│   ├── digitraffic-rata-trains-2018-05-01.zip
│   ├── digitraffic-rata-trains-2018-06-01.zip
│   ├── digitraffic-rata-trains-2018-07-01.zip
│   ├── digitraffic-rata-trains-2018-08-01.zip
│   ├── digitraffic-rata-trains-2018-09-01.zip
│   ├── digitraffic-rata-trains-2018-10-01.zip
│   ├── digitraffic-rata-trains-2018-11-01.zip
│   └── digitraffic-rata-trains-2018-12-01.zip
├── weatherdata
│   ├── HKI.csv
│   ├── JNS.csv
│   ├── JY.csv
│   ├── KAJ.csv
│   ├── KUO.csv
│   ├── KV.csv
│   ├── LH.csv
│   ├── OL.csv
│   ├── PRI.csv
│   ├── ROI.csv
│   ├── SV.csv
│   ├── TKU.csv
│   ├── TPE.csv
│   └── VS.csv
```
Nyt datat olivat saatavilla, ja jäljelle jäisi niiden yhdistely. Tämä vaatikin sen, että vain tunnettujen lähtöasemien datat huomioitaisiin, ja datasettiä hieman siivoiltaisiin. Tätä varten tehtiin oma skripti, jossa junadatan sisältävät ZIP-tiedostot avattiin ja yhdistettiin säädataan. Myös osa junadatan epärelevanteista piirteistä poistettiin, ja ainoastaan IC-, S- ja P-tyypin lähi- ja kaukojunat otettiin tarkasteluun.

Säädatassa oli suomenkieliset attribuuttinimet, jotka uudelleennimettiin englanniksi, ja havainnon aika/päivämäärä oli erotettu eri attribuuteille yhden datetime-tyyppisen sijaan, jonka muuntaminen datetime-tyyppiseksi vaati hieman kikkailuja. Säädatassa oli myös käytössä UTC-aika, joten se tuli muuttaa GMT+2-aikavyöhykkeelle. Kun muunnokset oli tehty, riitti loopata junadata lävitse ja ottaa uuteen datasettiin mukaan junan lähtöaikaa lähinnä oleva säähavainto junan lähtöasemalta.

Kyseinen skripti on ohessa:
```
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

            # We are only interested in common public train types IC, P and S
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

    df = pd.DataFrame(data)
    y = df['averageDelayInMinutes'].to_frame()
    X = df.drop(columns='averageDelayInMinutes')

    X.to_csv(X_filename)
    y.to_csv(y_filename)
```
Skriptin suorittaminen kestää n. 30-60min suuren datamäärän vuoksi, ja se tallentaa lopuksi tiedot `X.csv`- ja `y.csv`-tiedostoihin, josta ne voidaan hakea jatkokäyttöön. X.csv-tiedosto sisältää mahdollisia piirteitä, kun taas y.csv on enemmänkin "target variable", jota pyritään ennustamaan.
![Screen Shot 2019-05-02 at 14.14.35.png](https://www.dropbox.com/s/k0nx4rdmtrbjaij/Screen%20Shot%202019-05-02%20at%2014.14.35.png?dl=0&raw=1)
![Screen Shot 2019-05-02 at 14.15.19.png](https://www.dropbox.com/s/yks8s0733s0xjk5/Screen%20Shot%202019-05-02%20at%2014.15.19.png?dl=0&raw=1)

## Hyödylliset linkit
- [Digitrafficin dokumentaatio](https://www.digitraffic.fi/rautatieliikenne/#junat)
- [Stockoverflow: Reading zipped JSON files](https://stackoverflow.com/questions/40824807/reading-zipped-json-files)

## Vaikeat asiat
- Harjoitustyön aiheen keksiminen ongelmalähtöisesti datalähtöisyyden sijaan
- Halutunlaisen datan löytäminen, kun valmista datasettiä ei ole saatavilla
- Datan rajaaminen: kuinka pitkältä ajalta data otetaan, ilman että käsittelyaika monikertaistuu


