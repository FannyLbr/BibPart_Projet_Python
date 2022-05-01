# BibPart 
**BibPart** est une application développée par [Fanny Lebreton](https://github.com/FannyLbr) dans le cadre de l'évaluation du module **Introduction au développement applicatif** du [Master 2 "Technologies numériques appliquées à l'histoire"](https://www.chartes.psl.eu/fr/cursus/master-technologies-numeriques-appliquees-histoire), promotion 2021-2022.

**Consignes du devoir :**
> une application avec base de données relationnelle, comprenant formulaire pour ajout, suppression, édition. Il doit être possible de naviguer dans la collection, d'y faire une recherche simple voire complexe, un index doit y être inclus.

**Notation du devoir :**
> Le code sera noté en fonction:
> - de sa propreté;
> - de son fonctionnement;
> - de sa documentation (installation et fonctions);
> - de sa validité (la beauté du design ne sera pas prise en compte);
> - de son architecture;
> - et bien sûr des consignes.

## Projet : une bibliothèque numérique de partitions manuscrites authographes
**BibPart** recense un ensemble de partitions manuscrites authographes.

Cette application offre la possibilité de :
- **consulter** des informations bibliographiques sur une oeuvre musicale, sur la ou les partition(s) qui la constitue(nt) et sur son compositeur,
- **visionner** l'ensemble des pages de la partition, 
- **écouter** l'oeuvre grâce à la mise à disposition de vidéos.

## Fonctionnement de l'application
### Comment est construit BibPart ?
L'application a été créée avec :
- Python 3 (framework Flask),
- HTML et CSS (framework Bootstrap),
- base de données SQLite.

### Quelles sont ses fonctionnalités ?
Les fonctionnalités mises en place sont les suivantes : 
- 3 index pour :
  - les oeuvres, 
  - les partitions, 
  - les compositeurs.

- ensemble de notices biblioraphiques pour : 
  - les oeuvres, 
  - les partitions, 
  - les compositeurs.

- recherche rapide

- inscription / connexion / déconnexion

- recherche avancée

- formulaires d'ajout, de modification, de suppression des données.

## Installation et lancement de BibPart
Les commandes sont à effectuer dans un terminal.  
**Pour installer l'application :** 
- Installer Python 3
- Cloner ce dépôt : `git clone https://github.com/FannyLbr/BibPart_Projet_Python.git`
- Se déplacer dans le dossier cloné : `cd [nom du dossier]`
- Installer l'environnement virtuel : `virtualenv -p python3 env`
- Activer l'environnement virtuel : `source env/bin/activate`
- Installer les librairies nécessaires au fonctionnement de l'application : `pip install -r requirements.txt`

**Pour lancer l'application après l'installation :** 
- Lancer l'application : `python3 run.py`
- Cliquer sur le lien proposé.

**Pour lancer l'application :**
- Activer l'environnement virtuel : `source env/bin/activate`
- Lancer l'application : `python3 run.py`
- Cliquer sur le lien proposé.

