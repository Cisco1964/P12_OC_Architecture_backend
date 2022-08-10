# Développez une architecture back-end sécurisée en utilisant Django ORM

Ce CRM développé en interne permet aux utilisateurs de Epicevents de créer et mettre à jour une base de données clients, contrats et des évènements liés à ceux-ci.

Une base de donnée sécurisée est mise en œuvre avec Django ORM et PostgreSQL, la base de données PostgresSQL (nom : epiceventsdb) doit être créée avant de lancer le projet, pour l'accès a cette base, voir le fichier settings.py.

Code source complet du projet (Python 3.8.5, Django 4.0.5, psycopg2-binary==2.9.3)

# Pré-requis

Création d'un environnement virtuel ENV  
* python3 -m venv ENV
* activation de l'environnement virtuel : 
    * source ENV/bin/activate (Linux/Mac) 
    * ENV\Scripts\activate (Windows)
* installation des packages : voir le fichier requirements.txt

# Installation de l'application en local

Commandes à saisir pour l'installation :

Sur Windows/Linux/Mac :

```
$ git clone https://github.com/Cisco1964/P12_OC_Architecture_backend.git
$ cd projet_epic
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```


# Utilisation de Postman pour comprendre et utiliser l'API

Lien Postman  https://documenter.getpostman.com/view/18296799/UzJMsFfs

Extraction collection Postman : Epicevents.postman_collection.json

# Notes

La commande DUMPDATA a été utilisée pour extraire les données de la BDD :

```
$ python manage.py dumpdata authenticate.User crm.Clients crm.Contrats crm.Events --indent 2 >  database.json
```

Pour charger la bdd utiliser la commande :

```
$ python manage.py loaddata crm/fixtures/database.json
```


