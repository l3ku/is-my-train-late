Leo Toikka
leo.toikka@tuni.fi
# Johdanto datatieteeseen – harjoitustyön vaihe 4
Neljännessä vaiheessa harjoitustyötä tavoitteena oli kuvailla dataa toteuttamalla datan ominaisuuksia kuvaavia visualisointeja. Datan ominaisuuksia kuvaillessa huomaa usein myös epätoivottuja datan ominaisuuksia, joten tämä vaihe menee mielestäni osittain päällekkäin edellisen kanssa ja siten olenkin myös siivonnut/jalostanut dataa tässä vaiheessa.

## Datan kuvailu
Heti ensimmäiseksi käytin Pandasin `DataFrame.describe`-funktiota, sillä se tulostaa jokaiselle datan attribuuteille joukon ominaisuuksia. Koska minulla oli eritelty featuret ja ennustettava suure (`averageDelayInMinutes`), oli järkevää yhdistää ensin ne visualisointeja varten.
![Screen Shot 2019-05-02 at 21.35.26.png](https://www.dropbox.com/s/smxrxyx1pjl7k4q/Screen%20Shot%202019-05-02%20at%2021.35.26.png?dl=0&raw=1)
Yllä olevasta taulukosta on havaittavissa, että `rainIntensity` (sateen intensiteetti) ja `snowDepth` (lumen syvyys) attribuuttien jakauma on hieman kummallinen:
- Miksi pienin mitattu lumen syvyys on negatiivinen (vähintään 25% arvoista negatiivisia)?
- Miksi 75% sateen intensiteetin ja lumen syvyyden arvoista on pienempi tai yhtäsuuri kuin nolla?
- Miten näkyvyys voi olla ainoastaan 80m?

Lisäksi taulukosta nähdään, kuinka paljon attribuuteista puuttuu arvoja taulukon `count`-sarakkeen avulla: kokonaisuudessaan datassa on rivejä 87804 kpl, eli `rainIntensity`- ja `snowDepth`-attribuuteista puuttuu lähes neljäosan verran eli n. 20000 arvoa, kun taas `visibility`-attribuutista jo lähes puolet n. 37000 arvolla. Koneoppimisessa ei täten liene järkevää käyttää näitä attribuutteja. Ilmatieteen laitoksen data on ilmeisesti valitettavan sotkuista.

Parempaa havainnointia varten on järkevää tehdä nk. Scatter-matriisi, josta näkyy attribuuttien väliset korrelaatiot sekä niiden jakaumat:
![Screen Shot 2019-05-02 at 21.58.05.png](https://www.dropbox.com/s/7d99cngyrqhmpyh/Screen%20Shot%202019-05-02%20at%2021.58.05.png?dl=0&raw=1)
Selvää korrelaatiota ei ole minkään piirteen ja junan myöhästymisen keskiarvon (`averageDelayInMinutes`) kanssa. Attribuuttien omat jakaumat asettuvat vasemmasta yläkulmasta oikeaan alakulmaan menevään diagonaaliin, ja niistä nähdään, että suurin osa sateen intensiteetin ja lumensyvyyden arvoista on lähellä nollaa. Toisaalta näkyvyyden (`visibility`) arvot ovat keskittyneet 50000 m läheisyyteen.

Kokeillaan seuraavaksi tarkastella junan lähtöajankohdan vaikutusta lämpötilaan:
![Screen Shot 2019-05-02 at 22.10.35.png](https://www.dropbox.com/s/ff1c7u3mocs5i7b/Screen%20Shot%202019-05-02%20at%2022.10.35.png?dl=0&raw=1)
Näyttää siltä, että datassa on tapahtunut jotakin kummallista 6/2018 jälkeen, sillä näyttäisi, että lämpötilalla on vain muutama eri diskreetti arvo sen sijaan, että se vaihelisi kuten aiemmissa päivämäärissä. Joko alkuperäisessä datassa on ollut jotakin ongelmia tai datasettien yhdistelyssä on tapahtunut virhe, mutta tässä vaiheessa järkevä ratkaisu on yksinkertaisesti poistaa 6/2018 jälkeen kerätty data:
![Screen Shot 2019-05-02 at 22.12.08.png](https://www.dropbox.com/s/kgi253mhovn53uo/Screen%20Shot%202019-05-02%20at%2022.12.08.png?dl=0&raw=1)

### Muita visualisointeja
Mitä junatyyppejä lähtee miltäkin asemalta:
![](https://www.dropbox.com/s/j0wvmt08has3tp3/Screen%20Shot%202019-05-02%20at%2022.23.12.png?dl=0&raw=1)
Kuinka paljon lunta on mihinkin vuodenaikaan:
![Screen Shot 2019-05-02 at 22.23.49.png](https://www.dropbox.com/s/o7yh0es08xdrivo/Screen%20Shot%202019-05-02%20at%2022.23.49.png?dl=0&raw=1)
Kuinka paljon lunta eri asemilla keskimäärin on (nähdään, että esim. Tampereen säähavaintoasemalta puuttuu kokonaan data):
![Screen Shot 2019-05-02 at 22.23.56.png](https://www.dropbox.com/s/5yac5lc8vcj40uo/Screen%20Shot%202019-05-02%20at%2022.23.56.png?dl=0&raw=1)
Kuinka pitkiä matkoja minuuteissa keskimäärin eri junatyypit kulkevat:
![Screen Shot 2019-05-02 at 22.24.12.png](https://www.dropbox.com/s/6v22catra32i1bq/Screen%20Shot%202019-05-02%20at%2022.24.12.png?dl=0&raw=1)
Miten eri junatyypit ovat keskimäärin myöhässä ja miten myöhästymisen jakauma käyttäytyy:
![Screen Shot 2019-05-02 at 22.35.36.png](https://www.dropbox.com/s/mn2mkjz6jtdiemy/Screen%20Shot%202019-05-02%20at%2022.35.36.png?dl=0&raw=1)
Kuinka paljon tietyiltä asemilta lähtevät junat ovat keskimäärin myöhässä minuuteissa:
![Screen Shot 2019-05-02 at 22.27.21.png](https://www.dropbox.com/s/s3qmcl08pnii3h7/Screen%20Shot%202019-05-02%20at%2022.27.21.png?dl=0&raw=1)
## Hyödylliset linkit
- [Holoviewsin dokumentaatio](http://holoviews.org/getting_started/Introduction.html)
- [Visualisointiluennon Jupyter-työkirja](https://github.com/jodatut/2019/blob/master/luentokirjat/Luento%206.ipynb)

## Vaikeat/helpot asiat
- Vaikeaa: sotkuisen datan siivoaminen
- Vaikeaa: scatter-matriisin tulkinta ja eri attribuuttien jakaumien tulkitseminen
- Vaikeaa: järkevien visualisointien keksiminen
- Helppoa: visualisointi Holoviewsin avulla

