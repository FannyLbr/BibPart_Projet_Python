from warnings import warn

# Variable stockant le nombre de résultats par page
RESULTATS_PAR_PAGE = 3

# Variable nécessaire pour la gestion des sessions, génère des clefs d'encryptage  pour conserver les informations des
# utilisateurs de page en page
SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
