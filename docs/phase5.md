Leo Toikka
leo.toikka@tuni.fi
# Johdanto datatieteeseen – harjoitustyön vaihe 5
Harjoitustyön viidennessä vaiheessa oli tarkoitus soveltaa dataan koneoppimista.

## Koneoppiminen
Ensimmäiseksi tuli mieleen lähestyä junan myöhästymisen ennustamisen ongelmaa eri attribuuttien ja myöhästymisajan välisellä korrelaatiolla. Suurin korrelaatio myöhästymisen kanssa oli kuitenkin matkan kestolla.
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
Koska edellisessä visualisointiin liittyvässä vaiheessa huomattiin, että `visibility`-attribuutissa on lähes 40000 NaN-arvoa, on attribuutti järkevää poistaa: NaN-arvot sisältävät rivit on kuitenkin poistettava ennen koneoppimista, eikä vähintään 40000 datarivin poistaminen olisi mielekästä.
```
X_join_y_subset = X_join_y.drop(columns=['visibility'])
X_join_y_subset = X_join_y_subset.dropna() # Poistetaan NaN arvot
y_clean = X_join_y_subset['averageDelayInMinutes'].to_frame()
X_clean = X_join_y_subset.drop(columns=['averageDelayInMinutes'])
```
Tämän jälkeen kokeiltiin erilaisia sklearnin tarjoamia malleja ja käytettiin lisäksi Cross-validation -tekniikkaa tulosten validoimiseksi. Tätä ennen tuli kuitenkin muuttaa kategoriset muuttujat ns. hot-encoded -tyyppisiksi, eli eri attribuuttien eri arvovaihtoehdot ovat uusia attribuutteja, jotka ovat joko 0 tai 1 sen mukaan, onko kyseinen arvo kyseessä (esim. `{"Station": "HKI"}` => `{"Station_HKI": 1, "Station_VS": 0, "Station_XXX": 0...}`:
```
>>> X_hot_encoded = pd.get_dummies(X_clean.drop(columns=['departureTime']))
>>> X_hot_encoded.head()
   rainIntensity  snowDepth  temperature  tripDuration  windSpeed  ...  departureStation_PRI  departureStation_VS  type_IC  type_P  type_S
0            0.0        0.0          2.8         257.0        2.8  ...                     0                    0        1       0       0
1            0.0        0.0          2.1         263.0        2.4  ...                     0                    0        1       0       0
2            0.0        0.0          1.7         263.0        2.0  ...                     0                    0        1       0       0
4            0.0        0.0          1.3         246.0        2.2  ...                     0                    0        1       0       0
6            0.0        0.0          1.0         265.0        2.2  ...                     0                    0        0       0       1

[5 rows x 16 columns]
```
Ohessa ote koneoppimiseen käytetystä koodista:
```
print("--> Initializing estimators...")
estimators = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'Elastic Net': ElasticNet(),
    'Bayesian Ridge': BayesianRidge(),
    'Orthogonal Matching Pursuit': OrthogonalMatchingPursuit(),
    'Random Forest': RandomForestRegressor(n_estimators=300, max_depth=10, n_jobs=-1)
}

print("--> Fitting estimators...")
n_splits = 5
rs = ShuffleSplit(n_splits=n_splits, test_size=0.25)
rs.get_n_splits(X_hot_encoded)

# Initialize results data structure
results = {}

cv = 1
for train_index, test_index in rs.split(X_hot_encoded):
    print(f"--> On split {cv}/{n_splits}...")
    X_train = X_hot_encoded.values[train_index]
    y_train = y.values[train_index]
    X_test = X_hot_encoded.values[test_index]
    y_test = y.values[test_index]

    # Use all estimators with this data
    for name, estimator in estimators.items():
        print(f"-----> Testing '{name}'...")
        results.setdefault(name, [])
        estimator.fit(X_train, np.ravel(y_train))
        results[name].append(median_absolute_error(y_test, estimator.predict(X_test)))

    cv += 1

results = pd.DataFrame(results)
print(results.describe())
```
Ja tulokset:
```
       Linear Regression     Ridge     Lasso  Elastic Net  Bayesian Ridge  Orthogonal Matching Pursuit  Random Forest
count           5.000000  5.000000  5.000000     5.000000        5.000000                     5.000000       5.000000
mean            2.945479  2.945434  2.957228     2.956825        2.953763                     2.953756       2.793672
std             0.020127  0.020103  0.018483     0.017423        0.017332                     0.018966       0.023402
min             2.922621  2.922593  2.934694     2.934041        2.931476                     2.931809       2.766669
25%             2.933224  2.933315  2.944700     2.947169        2.944878                     2.947680       2.778106
50%             2.947636  2.947411  2.959095     2.958830        2.956192                     2.947922       2.789160
75%             2.947815  2.947781  2.965241     2.963833        2.957965                     2.958169       2.810483
max             2.976099  2.976070  2.982409     2.980252        2.978306                     2.983198       2.823940
```
Tuloksista huomataan, että pienimmän virheen ennustuksissa tekee Scikit-learnin `RandomForestRegressor`, joka saa virheen keskiarvoksi 2.793672. Kun käytetään Mean Absolute Error -arvoa, tämä tarkoittaa, että ennustukset heittävät keskimäärin n. 3 minuutilla. Tässä vielä vertailuna myöhästymisen jakauma:
![Screen Shot 2019-05-03 at 0.11.32.png](https://www.dropbox.com/s/u3xea9vpvec6eea/Screen%20Shot%202019-05-03%20at%200.11.32.png?dl=0&raw=1)
Eli suurin osa junista on ajallaan, kuten pitääkin, jolloin 3 minuutilla pieleen ennustaminen ei ole kovinkaan tehokasta. Johtopäätöksenä tästä koneoppimisen vaiheesta voidaankin kenties tehdä, etteivät sääolosuhteet juurikaan korreiloi junien myöhästymisen kanssa vaan se on enemmän satunnaista, vaikka usein mielletäänkin, että esimerkiksi suuri lumisateen määrä aiheuttaa junien myöhästymistä. Oikeastaan pienempi virhe ennustuksissa saatiin, kun säätiedot poistettiin kokonaan häiritsemästä, mutta tällöinkin virhe junan myöhästymismäärässä oli `RandomForestRegressor`-luokittelijalla keskimäärin n. 2,2 minuuttia.

## Hyödylliset linkit
- https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ShuffleSplit.html
- https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
- https://datascience.stackexchange.com/questions/39137/how-can-i-check-the-correlation-between-features-and-target-variable

## Vaikeat/helpot asiat
- Vaikea: parhaan estimaattorin löytäminen (RandomForestRegressor)
- Helppo: sklearnin estimaattoreiden miellyttävä rajapinta (`estimator = Estimator()` => `estimator.fit(...)` => `estimator.predict(...)`)
- Vaikea: miten saan parannettua tulosta, eli pienennettyä virheen määrää? Päätin jossakin vaiheessa vaan luovuttaa, koska tulokset eivät parantuneet (ei voi pakottaa jotakin riippuvuussuhdetta, jos sitä ei ole...)


