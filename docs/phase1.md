# Johdanto datatieteeseen – harjoitystyön vaihe 1

## Google Cloud Platform (GCP) -palvelun käyttöönotto
Päätin valista harjoitustyön kehitysympäristöksi oman pilviympäristön Google Cloud Platformin tarjoamana virtuaalikoneena. Vaikka olen käyttänyt aiemmin jo Amazon Web Services (AWS) -palvelua, päätin kokeilla GCP:tä, koska AWS:n ilmainen kokeilujakso oli minulla jo päättynyt ja Google tarjoaa uusille käyttäjilleen vastaavanlaisen 12kk kokeilun. Kustannustehokkuuden lisäksi minua houkutteli tutustua GCP:n käyttöön ja vertailla sitä AWS:n käyttökokemukseen, koska en ollut aiemmin käyttänyt GCP:tä.

## GCP:n virtuaalikoneen luominen
Loin GCP:n hallintapaneelista uuden projektin "JODATUT", johon loin uuden virtuaalikoneen "jodatut-1". Instanssiin käsiksi pääsemiseksi SSH-yhteyden avulla lisäsin oman julkisen SSH-avaimeni instanssiin paneelista kohdasta `instance > metadata > SSH keys`. Tämän jälkeen pääsin sisään SSH-yhteydellä komentoriviltä:
```
$ ssh leotoikka1@xx.xxx.xx.xxx
Linux jodatut-1 4.9.0-8-amd64 #1 SMP Debian 4.9.144-3.1 (2019-02-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Mar 25 14:04:33 2019 from 185.112.82.236
leotoikka1@jodatut-1:~$
```

## Jupyterin asennus ja käyttönotto
Alla on esitettynä kokonaisuudessaan Jupyterin asennus vaiheittain tekstikaappauksina komentorivi-ikkunasta. Koska [Jupyterin asennusohjeissa](https://jupyter.org/install) neuvotaan käyttämään Anaconda-jakelua asentamiseen, haettiin Anacondan Python 3.7 -version asentamiseen käytettävä shell-skripti:
```
leotoikka1@jodatut-1:~$ wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
--2019-03-25 14:08:17--  https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.130.3, 104.16.131.3, 2606:4700::6810:8303, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.130.3|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 684237703 (653M) [application/x-sh]
Saving to: ‘Anaconda3-2018.12-Linux-x86_64.sh’

Anaconda3-2018.12-Linux-x86_64.sh       100%[=============================================================================>] 652.54M  83.3MB/s    in 6.7s

2019-03-25 14:08:24 (97.6 MB/s) - ‘Anaconda3-2018.12-Linux-x86_64.sh’ saved [684237703/684237703]
```
Tämän jälkeen kyseiselle shell-skriptille annettiin suoritusoikeudet (execute, `+x`) jonka jälkeen se suoritettiin:
```
leotoikka1@jodatut-1:~$ chmod +x Anaconda3-2018.12-Linux-x86_64.sh && ./Anaconda3-2018.12-Linux-x86_64.sh
WARNING: bzip2 does not appear to be installed this may cause problems below

Welcome to Anaconda3 2018.12

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>>

...

./Anaconda3-2018.12-Linux-x86_64.sh: 353: ./Anaconda3-2018.12-Linux-x86_64.sh: bunzip2: not found
tar: This does not look like a tar archive
tar: Exiting with failure status due to previous errors
leotoikka1@jodatut-1:~$ bunzip2
-bash: bunzip2: command not found
```
Tämä ei suoraan toiminutkaan puuttuvan bzip2-ohjelman vuoksi, koska GCP:n virtuaaliympäristö on mahdollisimman suppea valmiiksi asennettujen ohjelmien suhteen. Asennetaan täten siis puuttuva bunzip2:
```
leotoikka1@jodatut-1:~$ sudo apt-get update && sudo apt-get install bzip2

```
Ja kokeillaan uudestaan:
```
leotoikka1@jodatut-1:~$ rm -rf anaconda3/ && ./Anaconda3-2018.12-Linux-x86_64.sh

Welcome to Anaconda3 2018.12

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>>

...
...

Do you wish the installer to initialize Anaconda3
in your /home/leotoikka1/.bashrc ? [yes|no]
[no] >>> yes

Initializing Anaconda3 in /home/leotoikka1/.bashrc
A backup will be made to: /home/leotoikka1/.bashrc-anaconda3.bak


For this change to become active, you have to open a new terminal.

Thank you for installing Anaconda3!

===========================================================================

Anaconda is partnered with Microsoft! Microsoft VSCode is a streamlined
code editor with support for development operations like debugging, task
running and version control.

To install Visual Studio Code, you will need:
  - Administrator Privileges
  - Internet connectivity

Visual Studio Code License: https://code.visualstudio.com/license

Do you wish to proceed with the installation of Microsoft VSCode? [yes|no]
>>> no

```
Tämän jälkeen Jupyterin pitäisi toimia komentoriviltä `jupyter`-komennolla:
```
leotoikka1@jodatut-1:~$ jupyter notebook
-bash: jupyter: command not found

```
Koska asennuksen jälkeen ei kirjauduttu SSH:sta ulos, PATH-muuttujan sisällössä ei vielä ollut Anacondan asentamia pakettaja. Ajetaan siis uudelleen `~/.bashrc` ennen komennon suorittamista:
```
leotoikka1@jodatut-1:~$ . ~/.bashrc && jupyter notebook
[I 14:20:42.553 NotebookApp] Writing notebook server cookie secret to /home/leotoikka1/.local/share/jupyter/runtime/notebook_cookie_secret
[I 14:20:42.984 NotebookApp] JupyterLab extension loaded from /home/leotoikka1/anaconda3/lib/python3.7/site-packages/jupyterlab
[I 14:20:42.984 NotebookApp] JupyterLab application directory is /home/leotoikka1/anaconda3/share/jupyter/lab
[I 14:20:42.986 NotebookApp] Serving notebooks from local directory: /home/leotoikka1
[I 14:20:42.986 NotebookApp] The Jupyter Notebook is running at:
[I 14:20:42.986 NotebookApp] http://localhost:8888/?token=d0bf534c5b69b054e178fc2e7598155c17cbdced208dc99a
[I 14:20:42.986 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 14:20:42.990 NotebookApp] No web browser found: could not locate runnable browser.
[C 14:20:42.990 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/leotoikka1/.local/share/jupyter/runtime/nbserver-26966-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=d0bf534c5b69b054e178fc2e7598155c17cbdced208dc99a
```
Nyt Jupyter neuvoo avamaan URL:n localhostissa, mutta koska tämä hosti on GCP:ssä, niin täytyy käyttää oikeaa ulkoista IP-osoitetta (jota myös käytettiin SSH:n kanssa). Lisäksi täytyy avata portti 8888 VM-instanssin [palomuuriasetuksista](https://cloud.google.com/vpc/docs/using-firewalls) GCP:n admin-paneelista. Avasin portin kaikille IP-osoitteelle CIDR-blokilla 0.0.0.0/0.

Tämän jälkeen en kuitenkaan vielä päässyt käsiksi Jupyterin hallintanäkymään verkkoselaimessani, joten kokeilin käyttää hostin omaa hostnamea `jodatut-1`, joka löytyi myös /etc/hosts-tiedostosta:
```
leotoikka1@jodatut-1:~$ sudo cat /etc/hosts
127.0.0.1 localhost
::1   localhost ip6-localhost ip6-loopback
ff02::1   ip6-allnodes
ff02::2   ip6-allrouters

10.166.0.2 jodatut-1.europe-north1-a.c.jodatut.internal jodatut-1  # Added by Google
169.254.169.254 metadata.google.internal  # Added by Google
leotoikka1@jodatut-1:~$ jupyter notebook --ip=jodatut-1
[I 14:41:08.608 NotebookApp] JupyterLab extension loaded from /home/leotoikka1/anaconda3/lib/python3.7/site-packages/jupyterlab
[I 14:41:08.608 NotebookApp] JupyterLab application directory is /home/leotoikka1/anaconda3/share/jupyter/lab
[I 14:41:08.610 NotebookApp] Serving notebooks from local directory: /home/leotoikka1
[I 14:41:08.611 NotebookApp] The Jupyter Notebook is running at:
[I 14:41:08.611 NotebookApp] http://jodatut-1:8888/?token=6551a2b67808941a0ef2783214b3a3ae7cf055e1198b3bb4
[I 14:41:08.611 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 14:41:08.615 NotebookApp] No web browser found: could not locate runnable browser.
[C 14:41:08.615 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/leotoikka1/.local/share/jupyter/runtime/nbserver-27190-open.html
    Or copy and paste one of these URLs:
        http://jodatut-1:8888/?token=6551a2b67808941a0ef2783214b3a3ae7cf055e1198b3bb4
[I 14:41:20.981 NotebookApp] 302 GET /?token=6551a2b67808941a0ef2783214b3a3ae7cf055e1198b3bb4 (185.112.82.236) 0.66ms
```
Ja ilmeisesti tämä auttoi, ja pääsin nyt Jupyteriin verkkoselaimessani. Käynnistin Jupyterin taustalle pyörimään liittämällä `&`-merkin edellisen käynnistyskomennon perään.

## Nginx reverse-proxyna ja salatun HTTPS-yhteyden käyttö
Koska haluan tehdä harjoitustyön kehityksestä mahdollisimman helppoa, teen kehitystä omaa `.dev` -päätteistä verkkotunnustani käyttäen sovelluksen käyttäessä HTTP-yhteyksien oletusporttia 80 oletuksena asetetun 8888 sijaan (ei tarvitse aina kirjoittaa :8888 URL:n perään). Koska kaikki `.dev`-TLD:n omaavat verkkotunnukset [lisätään automaattisesti HSTS-preload -listaan](https://get.dev/#benefits), tarvitsen myös HTTPS-varmenteen asennettavaksi palvelimelle. On periaatteessa täysin mahdollista, että Jupyteria voi suoraan käyttää porteissa 80/443(HTTPS), mutta olen aiemminkin tehnyt Nginx-palvelimella reverse-proxy -ohjauksia joten valitsin sen vaihtoehdon tälläkin kertaa.

Aivan ensimmäiseksi hankin GCP:n hallintapaneelista virtuaalikoneelleni `jodatut-1` oman dedikoidun ulkoisen IP-osoitteen, johon ohjasin verkkotunnukseni. Dedikoitu ulkoinen IP-osoite mahdollistaa instanssin ulkoisen IP-osoitteen säilymisen mahdollisten uudelleenkäynnistyksen välissä, mikä on tärkeää, sillä verkkotunnukset ohjataan kyseiseen osoitteeseen, eikä ole mielekästä tehdä verkkotunnukselle kovinkaan usein ohjauksia.

Tämän jälkeen asensin Nginx-ohjelmiston palvelimelle, johon tein omanlaisen konfiguraatiotiedoston liikenteen pakottamiseksi salaiseksi ja liikenteen reverse-proxyttamiseksi Jupyterille porttiin 8888. Alla ote konfiguraatiotiedostosta `/etc/nginx/sites-available/default`, jossa liikenne ohjataan Jupyterille:
```
...
    location {
        ...
        proxy_pass http://jodatut-1:8888;
        ...
    }
...
```
Tämän jälkeen asensin certbot-ohjelmiston, ja hankin sen avulla oman Let's Encrypt -HTTPS-varmenteen verkkotunnukselleni komennolla `sudo certbot --nginx -d koodi.dev -d www.koodi.dev`. Jupyteriin mennessä verkkoselaimellani huomasin, että se ei saa yhteyttä python3-kerneliin, vaan tulee virheviesti "Not found". Pikaisen etsiskelyn jälkeen huomasin, että Jupyter käyttää websockets-tekniikkaa, joten proxy-konfiguraatioon tarvitaan vähän viilausta, ainakin lähetettyjen HTTP-otsakkeiden suhteen. Onneksi tähän löytyi [kätevät valmiit ohjeet](https://aptro.github.io/server/architecture/2016/06/21/Jupyter-Notebook-Nginx-Setup.html). Lopulta pääsin vaivattomasti Jupyteriin verkkoselaimellani:
![Screen Shot 2019-03-29 at 14.57.52.png](https://www.dropbox.com/s/5ui31mxa3anbsq1/Screen%20Shot%202019-03-29%20at%2014.57.52.png?dl=0&raw=1)

## Hyödyllisiä linkkejä
- [Jupyterin asennusohjeet](https://jupyter.org/installation)
- [Google Cloud Platformin dokumentaatio](https://cloud.google.com/vpc/docs/)
- [Certbotin dokumentaatio](https://certbot.eff.org/docs/intro.html#how-to-run-the-client)

## Kolme vaikeaa/helppoa asiaa
1. Virtuaalikoneen käyttöönotto Google Cloud Platformilta oli hyvin nopeaa: tunnistautumiseen riitti muutamat klikkaukset kun oli jo valmiiksi olemassa oleva Google-tili
2. Ongelmia aiheutti Jupyterin käyttämä Websockets-teknologia Python-kernelin kanssa kommunikoimiseen: tietyt HTTP-otsakkeet piti lisätä Nginx-palvelimen määrittelytiedostoon
3. HTTPS-varmenteen käyttöönotto on nykyään hyvin nopeaa Let's Encryptin ja Certbotin kanssa