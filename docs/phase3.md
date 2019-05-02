Leo Toikka
leo.toikka@tuni.fi
# Johdanto datatieteeseen – harjoitustyön vaihe 3
Tässä vaiheessa harjoitustyötä oli tavoitteena jalostaa dataa paremmin hyödynnettävään muotoon. Tämä vaihe menee osittain päällekäin edellisen kanssa, sillä suuri osa jalostamisesta tapahtuu jo datasettien yhdistelyssä.

## Datan jalostaminen
Itse sää- ja junadatasettien yhdistelyssä osittain jalostettiin dataa, koska turhaa dataa ei kannata säilyttää. Toimenpiteet, jotka tehtiin yhdistelyssä (ks. 2. vaiheen skripti):
- Uudelleennimettiin suomenkieliset säädatan attribuutit englanniksi
- Muutettiin säädatan eritellyt vuosi-, kuukausi- ja päiväattribuutit yhdeksi datetime-tyyppiseksi attribuutiksi
- Muutettiin säädatan UTC-aikavyöhykkeen aika GMT+2-ajaksi, koska junadata on GMT+2 aikavyöhykkeeltä
- Junadatasta ottiin vain `Commuter` ja `Long-distance` -junatyypit (ei esimerkiksi huoltoajossa olevia) sekä tyypit `IC`, `S` ja `P` (lienevät yleisimmät kotimaan matkustusliikenteessä)
- Vain niiltä lähtöasemilta lähtevät junat, joista on saatavilla säädataa
- Vain sellaiset junat, joiden reitillä on vähintään 2 asemaa (lähtö- ja saapumisasema)
- Puuskanopeutta, tuulen suuntaa, kastepistettä, suhteellista kosteutta ja pilvien määrää ei otettu mukaan säädatasta, sillä niiden ei arveltu vaikuttavan junien kulkuun
- Laskettiin junien kulkutietojen perusteella junan keskimääräinen myöhässä eri asemapysähdyksillä
- Otettiin junien attribuuteista mukaan myöhästymismäärän lisäksi tyyppi, lähtöaika, matkan kesto ja lähtöasema, joten turhat attribuutit kuten `operatorShortCode` ja `timetableAcceptanceDate` jäivät pois
Lisäksi huomasin, että junan lähtöaika ei ollut datetime-tyyppinen, joten se muunnettiin:
![Screen Shot 2019-05-02 at 14.56.18.png](https://www.dropbox.com/s/kopy0x45cdab8de/Screen%20Shot%202019-05-02%20at%2014.56.18.png?dl=0&raw=1)
## Hyödylliset linkit
- Pandasin [DataFramen dokumentaatio](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)

## Vaikeat/helpot asiat
- Vaikeaa: Mitä kaikkia attribuutteja pitäisi ottaa dataan mukaan
- Vaikeaa: Tutustuminen Pandasin käyttöön, jatkuvasti täytyy googlata "how to ... in pandas"
- Helppoa: Pandas helpottaa huomattavasti datan laadun tutkimista: mitä attribuutteja, mikä niiden tyyppi on jne.

