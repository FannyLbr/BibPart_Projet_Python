# Import de Flask du module flask
from flask import Flask
# Import de SQLAlchemy de flask_sqlalchemy pour interagir avec la BDD
from flask_sqlalchemy import SQLAlchemy
# Import du package LoginManager pour gérer les sessions utilisateurs
from flask_login import LoginManager
# Import de SECRET_KEY à partir du fichier constantes.py
from .constantes import SECRET_KEY
# Import du package os permettant d'agir avec les différents systèmes d'exploitation
import os

# Définition des chemins :
# Stockage du chemin du fichier courant
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# Stockage du chemin vers le dossier templates
templates = os.path.join(chemin_actuel, "templates")
# Stockage du chemin vers le dossier static
statics = os.path.join(chemin_actuel, "static")

# Création de l'application en tant qu'instance de la classe Flask
app = Flask("Application",
            template_folder=templates,
            static_folder=statics)

# Configuration du secret
app.config['SECRET_KEY'] = SECRET_KEY

# Configuration de la BDD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db_BibPart.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initiation de l'extension
db = SQLAlchemy(app)

# Gestion d'utilisateur
login = LoginManager(app)

from .routes import accueil, ensavoirplus, index_partitions, index_oeuvres, index_compositeurs, notice_oeuvre, \
    notice_compositeur, notice_partition, inscription, deconnexion, connexion, recherche, rechercheavancee, \
    accueil_ajout, ajout_compositeur, ajout_forme, ajout_institution, ajout_instrument, ajout_oeuvre, ajout_partition, \
    maj_oeuvre, maj_partition, maj_compositeur, supprimer_oeuvre, supprimer_partition, supprimer_compositeur

from .gestion_erreur import not_found
