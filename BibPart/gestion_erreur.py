# Gestion de l'erreur 404
# Import du module render_template pour la relation entre les templates et les routes
from flask import render_template
# Import de la variable app
from BibPart.app import app


# Erreur 404
@app.errorhandler(404)
def not_found(erreur):
    """
        Route permettant l'affichage de l'erreur 404
        :returns : affichage du template erreur404.html
        :rtype: page html
        """
    return render_template("pages/erreur404.html"), 404
