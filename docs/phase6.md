Leo Toikka
leo.toikka@tuni.fi
# Johdanto datatieteeseen – harjoitustyön vaihe 6 (Toimeenpano)
Vaikka harjoitustyössä ei pystyttykään ennustamaan kovinkaan tarkasti junien myöhästymistä säätietojen avulla, kuten oli arvattavissakin, niin kuitenkin toimeenpanon kannalta saatiin arvokasta tietoa, etenkin visualisointien muodossa. Raportti on myös saatavilla interaktiivisemmassa muodossa englanniksi Jupyter-työkirjana [GitHub-repositoriossa](https://github.com/l3ku/is-my-train-late/blob/master/main.ipynb).

Esimerkiksi eri junatyyppien myöhästymisdata voisi olla päättäjille mielenkiintoinen data:
![Screen Shot 2019-05-03 at 0.41.42.png](https://www.dropbox.com/s/4k29x3a3fupzhr4/Screen%20Shot%202019-05-03%20at%200.41.42.png?dl=0&raw=1)
Siitä näkee suoraan esimerkiksi, että IC-junat ovat olleet keskimäärin n. 4 minuuttia myöhässä aikataulustaan, kun taas pendolinot vain 3 minuuttia. On myös huomattavaa, että jokin IC-juna on ollut jopa 300 minuuttia myöhässä.

Eräs toinen hyödyllinen tieto on nähdä, miten eri juna-asemilta lähtevät junat myöhästyvät:
![Screen Shot 2019-05-03 at 0.47.47.png](https://www.dropbox.com/s/8vihb6oy23ftmg7/Screen%20Shot%202019-05-03%20at%200.47.47.png?dl=0&raw=1)
Taulukosta voi huomata, että Helsingistä on lähtenyt jopa 37000 junaa ja seuraavaksi eniten Tampereelta n. 10000 junalla. Lahdesta on kerätty vain 3 kpl datariviä, joten siitä tehtyä arviota ei ehkä voida pitää luotettavana. Helsingistä on jokin juna ollut keskimäärin jopa 30 minuuttia etuajassa. Kaikilla asemilla kuitenkin junat ovat keskimäärin myöhässä yli 2 minuuttia.

Tarjolla olevasta numeerisesta datasta eniten junan myöhässäolon kanssa korreloi junamatkan pituus:
```
>>> corr_matrix = X_join_y.corr()
>>> print(corr_matrix['averageDelayInMinutes'].sort_values(ascending=False))
averageDelayInMinutes    1.000000
tripDuration             0.126311
snowDepth                0.050012
rainIntensity            0.032606
windSpeed               -0.006721
temperature             -0.041612
visibility              -0.055399
```
Eli toisin sanoen pidemmälle matkalle mennessä kannattaisi valmistautua myöhästymään enemmän, mikä käy myös maalaisjärkeen.

Vaikka se ei suoraan toimeenpanoon liitykään, niin mielestäni mielenkiintoinen kaavio syntyi lumen määrästä:
![Screen Shot 2019-05-03 at 0.53.36.png](https://www.dropbox.com/s/huqzks8jelcolr6/Screen%20Shot%202019-05-03%20at%200.53.36.png?dl=0&raw=1)
Kuvasta näkee esimerkiksi, että vuonna 2018 on ollut suurempi lumihangen syvyysennätys (lähes 80 cm) kuin talvella 2017 (vain 60 cm) käytössä olevien säämittausasemien datoista.

## Vaikeat/helpot asiat
- Vaikeaa: keksiä, minkä johtopäätöksen työstä voisi tehdä, koska koneoppimisesta ei saanut niin paljoa irti
- Helppoa: harjoitustyössä oppi ymmärtämään, että kuinka tärkeää toimiala-osaaminen olisi datan jalostamisvaiheessa
- Helppoa: katsoa vinkkiä, mitä muut ovat Slackissa raportoineet ja ohjata siten omaa työskentelyä


