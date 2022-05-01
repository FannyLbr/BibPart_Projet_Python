# Import des modules/ packages utiles au fonctionnement des routes
# Relation templates et routes, manipulation requêtes et réponses HTTP, envoi de messages flash, redirection
from flask import render_template, request, flash, redirect
# Pour la gestion des comptes utilisateurs
from flask_login import login_user, logout_user, current_user, login_required
# Import de la variable app
from BibPart.app import app
# Import pour la pagination
from .constantes import RESULTATS_PAR_PAGE
# Import permettant d'utiliser l'opérateur booléen or
from sqlalchemy import or_
# Import de l'ensemble des modèles de classe utiles
from .modeles.donnees import Oeuvre, Partition, Compositeur, Type, Instrument, Forme, Institution_conservation
from .modeles.utilisateurs import Utilisateur


# ROUTES PERMETTANT L'AFFICHAGE DES PAGES ACCUEIL ET EN SAVOIR PLUS

@app.route("/")
def accueil():
    """
    Route permettant l'affichage de la page accueil
    :returns : affichage du template accueil.html
    :rtype: page html
    """
    oeuvres = Oeuvre.query.filter(Oeuvre.id_oeuvre).all()
    partitions = Partition.query.filter(Partition.id_partition).all()
    compositeurs = Compositeur.query.filter(Compositeur.id_compositeur).all()
    return render_template("pages/accueil.html", nom="BibPart", oeuvres=oeuvres, partitions=partitions,
                           compositeurs=compositeurs)


@app.route("/ensavoirplus")
def ensavoirplus():
    """ Route permettant l'affichage de la page En savoir plus
    :returns : affichage du template ensavoirplus.html
    :rtype: page html
    """
    return render_template("pages/ensavoirplus.html")


# ROUTES PERMETTANT L'AFFICHAGE DES INDEX

@app.route("/index_oeuvres")
def index_oeuvres():
    """ Route permettant l'affichage de l'index des oeuvres
    :returns: affichage du template index_oeuvres.html
    :rtype: page html
    """
    alloeuvres = Oeuvre.query.all()

    if len(alloeuvres) == 0:
        return render_template("pages/index_oeuvres.html", var_groupe_oeuvres=alloeuvres)
    else:
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    alloeuvres = Oeuvre.query.order_by(Oeuvre.titre_oeuvre).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_oeuvres.html", nom="BibPart", var_groupe_oeuvres=alloeuvres)


@app.route("/index_partitions")
def index_partitions():
    """ Route permettant l'affichage de l'index des partitions
    :returns: affichage du template index_partitions.html
    :rtype: page html
    """
    allpartitions = Partition.query.all()

    if len(allpartitions) == 0:
        return render_template("pages/index_oeuvres.html", var_groupe_partitions=allpartitions)
    else:
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    allpartitions = Partition.query.order_by(Partition.titre_partition).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_partitions.html", nom="BibPart", var_groupe_partitions=allpartitions)


@app.route("/index_compositeurs")
def index_compositeurs():
    """ Route permettant l'affichage de l'index des compositeurs
    :returns: affichage du template index_compositeurs.html
    :rtype: page html
    """
    allcompositeurs = Compositeur.query.all()

    if len(allcompositeurs) == 0:
        return render_template("pages/index_oeuvres.html", var_groupe_partitions=allcompositeurs)
    else:
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    allcompositeurs = Compositeur.query.order_by(Compositeur.nom_compositeur).paginate(page=page,
                                                                                       per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_compositeurs.html", nom="BibPart", var_groupe_compositeurs=allcompositeurs)


# ROUTES PERMETTANT L'AFFICHAGES DES NOTICES

@app.route("/notice_oeuvre/<int:id_oeuvre>")
def notice_oeuvre(id_oeuvre):
    """
    Route permettant d'afficher la notice d'une oeuvre
    :param id_oeuvre: id de l'oeuvre
    :type id_oeuvre: int
    :return: affichage du template notice_oeuvre.html
    :rtype: page html
    """
    unique_oeuvre = Oeuvre.query.get(id_oeuvre)
    compositeur = unique_oeuvre.compositeurs
    forme = unique_oeuvre.formes
    type = unique_oeuvre.types
    instrument = unique_oeuvre.instruments
    partition = unique_oeuvre.partitions
    return render_template("pages/notice_oeuvre.html", nom="BibPart", var_oeuvre_unique=unique_oeuvre,
                           var_compositeur=compositeur, var_forme=forme, var_type=type, var_instrument=instrument,
                           var_partition=partition)


@app.route("/notice_partition/<int:id_partition>")
def notice_partition(id_partition):
    """
    Route permettant d'afficher la notice d'une partition
    :param id_partition: id de la partition
    :type id_partition: int
    :returns: affichage du template notice_partition.html
    :rtype: page html
    """
    unique_partition = Partition.query.get(id_partition)
    audio = unique_partition.oeuvres
    institution = unique_partition.institutions_conservation
    oeuvre = unique_partition.oeuvres
    return render_template("pages/notice_partition.html", nom="BibPart", var_partition_unique=unique_partition,
                           var_audio=audio, var_institution=institution, var_oeuvre=oeuvre)


@app.route("/notice_compositeur/<int:id_compositeur>")
def notice_compositeur(id_compositeur):
    """
    Route permettant d'afficher la notice d'un compositeur
    :param id_compositeur: id du compositeur
    :type id_compositeur: int
    :returns: affichage du template notice_compositeur.html
    :rtype: page html
    """
    unique_compositeur = Compositeur.query.get(id_compositeur)
    oeuvrecompo = unique_compositeur.oeuvres
    return render_template("pages/notice_compositeur.html", nom="BibPart", var_compositeur_unique=unique_compositeur,
                           var_oeuvrecompo=oeuvrecompo)


# ROUTES PERMETTANT UNE RECHERCHE RAPIDE ET AVANCÉE

@app.route("/recherche", methods=["GET"])
def recherche():
    """
       Route permettant de faire une recherche rapide sur les notices d'oeuvre
       :returns : affichage des templates correspondant aux barres de recherches et aux résultats de la recherche rapide
       :rtype: pages html
       """
    # Gestion de la page courante
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    keyword = request.args.get("keyword", None)
    # Création d'une liste vide permettant de stocker les mots-clefs s'ils existent, sinon elle reste vide
    resultats = []

    # Méthode "GET" utilisée : les mots clefs recherchés apparaîssent dans l'URL
    if keyword:
        resultats = Oeuvre.query.filter(or_(
            Oeuvre.id_oeuvre.like("%{}%".format(keyword)),
            Oeuvre.titre_oeuvre.like("%{}%".format(keyword)),
            Oeuvre.date_oeuvre.like("%{}%".format(keyword)),
            Oeuvre.compositeurs.has(Compositeur.nom_compositeur.like("%{}%".format(keyword))),
            Oeuvre.types.has(Type.label_type.like("%{}%".format(keyword))),
            Oeuvre.formes.has(Forme.label_forme.like("%{}%".format(keyword))))
        ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        titre = "Résultat pour la recherche `" + keyword + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=keyword)


@app.route('/rechercheavancee', methods=["POST", "GET"])
def rechercheavancee():
    """
    Route permettant de faire une recherche avancée
    :returns : affichage des templates correspondant aux formulaires et aux résultats de la recherche avancée
    :rtype: pages html
    """
    # Gestion de la page courante
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # Condition pour la méthode "POST" : cette méthode permet de ne pas inscrire les données dans l'URL, contrairement
    # à la méthode "GET"
    if request.method == "POST":
        # Création de 3 listes vides permettant de stocker par type de notice (oeuvre, partition, compositeur)
        # les mots-clefs s'ils existent, sinon elles restent vides
        resultatsA = []
        resultatsB = []
        resultatsC = []
        keyword = request.form.get("keyword", None)
        # Variable appelée dans le template des résultats pour la recherche avancée
        titre = "Résultat(s) de la recherche avancée"

        questionOeuvre = Oeuvre.query
        questionPartition = Partition.query
        questionCompositeur = Compositeur.query

        # Notice oeuvre
        titre_oeuvre = request.form.get("titreOeuvre", None)
        compositeur_oeuvre = request.form.get("compoOeuvre", None)
        date_oeuvre = request.form.get("dateOeuvre", None)
        type_oeuvre = request.form.get("typeOeuvre", None)
        forme_oeuvre = request.form.get("formeOeuvre", None)
        instrument_oeuvre = request.form.get("instrumentOeuvre", None)

        # Notice partition
        titre_partition = request.form.get("titrePartition", None)
        sous_titre_partition = request.form.get("soustitrePartition", None)
        format_partition = request.form.get("formatPartition", None)
        page_partition = request.form.get("nbpagePartition", None)
        statut_partition = request.form.get("statutPartition", None)
        institution_partition = request.form.get("nomInstitutionConservation", None)

        # Notice compositeur
        prenom_compo = request.form.get("prenomCompo", None)
        nom_compo = request.form.get("nomCompo", None)
        naissance_compo = request.form.get("naissanceCompo", None)
        mort_compo = request.form.get("mortCompo", None)

        # Notice oeuvre
        if titre_oeuvre:
            resultatsA = questionOeuvre.filter(Oeuvre.titre_oeuvre.like("%{}%".format(titre_oeuvre)))
        if compositeur_oeuvre:
            resultatsA = questionOeuvre.filter(
                Oeuvre.compositeurs.has(Compositeur.nom_compositeur.like("%{}%".format(compositeur_oeuvre))))
        if date_oeuvre:
            resultatsA = questionOeuvre.filter(Oeuvre.date_oeuvre.like("%{}%".format(date_oeuvre)))
        if type_oeuvre:
            resultatsA = questionOeuvre.filter(Oeuvre.types.has(Type.label_type.like("%{}%".format(type_oeuvre))))
        if forme_oeuvre:
            resultatsA = questionOeuvre.filter(Oeuvre.formes.has(Forme.label_forme.like("%{}%".format(forme_oeuvre))))
        if instrument_oeuvre:
            resultatsA = questionOeuvre.filter(Oeuvre.instruments.any(
                Instrument.label_instrument.like("%{}%".format(instrument_oeuvre))))

        # Notice partition
        if titre_partition:
            resultatsB = questionPartition.filter(Partition.titre_partition.like("%{}%".format(titre_partition)))
        if sous_titre_partition:
            resultatsB = questionPartition.filter(
                Partition.nom_sous_partie_partition.like("%{}%".format(sous_titre_partition)))
        if format_partition:
            resultatsB = questionPartition.filter(Partition.format_partition.like("%{}%".format(format_partition)))
        if page_partition:
            resultatsB = questionPartition.filter(Partition.page_partition.like("%{}%".format(page_partition)))
        if statut_partition:
            resultatsB = questionPartition.filter(Partition.statut_partition.like("%{}%".format(statut_partition)))
        if institution_partition:
            resultatsB = questionPartition.filter(Partition.institutions_conservation.has(
                Institution_conservation.nom_institution_conservation.like("%{}%".format(institution_partition))))

        # Notice compositeur
        if prenom_compo:
            resultatsC = questionCompositeur.filter(Compositeur.prenom_compositeur.like("%{}%".format(prenom_compo)))
        if nom_compo:
            resultatsC = questionCompositeur.filter(
                Compositeur.nom_compositeur.like("%{}%".format(nom_compo)))
        if naissance_compo:
            resultatsC = questionCompositeur.filter(
                Compositeur.annee_naissance_compositeur.like("%{}%".format(naissance_compo)))
        if mort_compo:
            resultatsC = questionCompositeur.filter(Compositeur.annee_mort_compositeur.like("%{}%".format(mort_compo)))

        if resultatsA:
            resultatsA = resultatsA.paginate(page=page)
        if resultatsB:
            resultatsB = resultatsB.paginate(page=page)
        if resultatsC:
            resultatsC = resultatsC.paginate(page=page)
        return render_template("pages/rechercheavancee.html", keyword=keyword, titre=titre, resultatsA=resultatsA,
                               resultatsB=resultatsB, resultatsC=resultatsC)
    return render_template("pages/rechercheavancee.html", nom="BibPart")


# ROUTES PERMETTANT L'INSCRIPTION, LA CONNEXION, LA DÉCONNEXION

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """
    Route permettant l'inscription d'un utilisateur
    :returns: redirection vers template accueil.html si succès ou vers template inscription.html si erreur
    :rtype: pages html
    """
    if request.method == "POST":
        # Application de la fonction creer présente dans le fichier utilisateurs.py
        statut, donnees = Utilisateur.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None))

        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees) + ".", "danger")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """
    Route permettant la connexion d'un utilisateur
    :returns: redirection vers template accueil.html si succès ou vers template connexion.html si erreur
    :rtype: pages html
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")

    if request.method == "POST":
        # Application de la fonction identification présente dans le fichier utilisateurs.py
        user = Utilisateur.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None))
        if user:
            flash("Connexion réussie", "success")
            login_user(user)
            return redirect("/")
        else:
            flash("Le login ou le mot de passe est incorrect.", "danger")

    return render_template("pages/connexion.html")


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """
    Route permettant la déconnexion d'un utilisateur
    :returns: redirection vers template accueil.html
    :rtype: page html
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


# ROUTES PERMETTANT L'AJOUT DE NOTICES

@app.route("/accueil_ajout", methods=["GET", "POST"])
def accueil_ajout():
    """
    Route permettant l'affichage de la page d'accueil pour l'ajout
    :return : affichage du template accueil_ajout.html
    :rtype : page html
    """
    return render_template("pages/accueil_ajout.html", nom="BibPart")


@app.route("/ajout_compositeur", methods=["GET", "POST"])
def ajout_compositeur():
    """
    Route permettant l'ajout d'un compositeur et les données qui lui sont associées dans la BDD
    :return: affichage du template ajout_compositeur.html
    :rtype: page html
    """
    if request.method == "POST":
        statut, donnees_compo = Compositeur.ajouter_compositeur(
            ajout_nom_compo=request.form.get("ajout_nom_compo", None),
            ajout_prenom_compo=request.form.get("ajout_prenom_compo", None),
            ajout_naissance_compo=request.form.get("ajout_naissance_compo", None),
            ajout_mort_compo=request.form.get("ajout_mort_compo", None),
            ajout_bio_compo=request.form.get("ajout_bio_compo", None),
            ajout_portrait_compo=request.form.get("ajout_portrait_compo", None))

        if statut is True:
            flash("Ajout réussi !", "success")
            return render_template("pages/ajout_compositeur.html", nom="BibPart")

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees_compo), "danger")
            return render_template("pages/ajout_compositeur.html")

    return render_template("pages/ajout_compositeur.html", nom="BibPart")


@app.route("/ajout_forme", methods=["GET", "POST"])
def ajout_forme():
    """
    Route permettant l'ajout d'une forme dans la BDD
    :return: affichage du template ajout_forme.html
    :rtype: page html
    """
    if request.method == "POST":
        statut, donnees_forme = Forme.ajouter_forme(
            ajout_label_forme=request.form.get("ajout_label_forme", None))

        if statut is True:
            flash("Ajout réussi !", "success")
            return render_template("pages/ajout_forme.html", nom="BibPart")

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees_forme), "danger")
            return render_template("pages/ajout_forme.html", nom="BibPart")

    return render_template("pages/ajout_forme.html", nom="BibPart")


@app.route("/ajout_institution", methods=["GET", "POST"])
def ajout_institution():
    """
    Route permettant l'ajout d'une institution de conservation dans la BDD
    :return: affichage du template ajout_institution.html
    :rtype: page html
    """
    if request.method == "POST":
        statut, donnees_insti = Institution_conservation.ajouter_institution(
            ajout_nom_institution=request.form.get("ajout_nom_institution", None),
            ajout_ville_institution=request.form.get("ajout_ville_institution", None))

        if statut is True:
            flash("Ajout réussi !", "success")
            return render_template("pages/ajout_institution.html", nom="BibPart")

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees_insti), "danger")
            return render_template("pages/ajout_institution.html", nom="BibPart")
    return render_template("pages/ajout_institution.html", nom="BibPart")


@app.route("/ajout_instrument", methods=["GET", "POST"])
def ajout_instrument():
    """
    Route permettant l'ajout d'un instrument dans la BDD
    :return : affichage du template ajout_instrument.html
    :rtype: page html
    """
    if request.method == "POST":
        labelInstrument = request.form.get("ajout_label_instrument", None)
        Instrument.ajouter_instrument(labelInstrument)

        flash("Ajout réussi !", "success")
        return render_template("pages/ajout_instrument.html", nom="BibPart")

    return render_template("pages/ajout_instrument.html", nom="BibPart")


@app.route("/ajout_oeuvre", methods=["GET", "POST"])
def ajout_oeuvre():
    """
    Route permettant l'ajout d'une oeuvre et les données qui lui sont associées dans la BDD
    :return: affichage du template ajout_oeuvre.html
    :rtype: page html
    """
    listeoeuvre = Oeuvre.query.order_by(Oeuvre.titre_oeuvre).all()
    listecompositeur = Compositeur.query.order_by(Compositeur.nom_compositeur).all()
    listetype = Type.query.order_by(Type.label_type).all()
    listeforme = Forme.query.order_by(Forme.label_forme).all()
    listeinstrument = Instrument.query.order_by(Instrument.label_instrument).all()

    if request.method == "POST":
        titreOeuvre = request.form.get("ajout_titre_oeuvre", None)
        dateOeuvre = request.form.get("ajout_date_oeuvre", None)
        audioOeuvre = request.form.get("ajout_audio_oeuvre", None)
        compoOeuvre = request.form.get("ajout_compositeur_oeuvre", None)
        typeOeuvre = request.form.get("ajout_type_oeuvre", None)
        formeOeuvre = request.form.get("ajout_forme_oeuvre", None)
        labelInstrument = request.form.get("ajout_label_instrument", None)
        recup = Compositeur.query.filter(Compositeur.nom_compositeur == compoOeuvre).first()
        recup2 = Type.query.filter(Type.label_type == typeOeuvre).first()
        recup3 = Forme.query.filter(Forme.label_forme == formeOeuvre).first()
        id_oeuvre = Oeuvre.ajouter_oeuvre(titreOeuvre, dateOeuvre, audioOeuvre, recup.id_compositeur, recup2.id_type,
                                          recup3.id_forme)
        id_instrument = Instrument.ajouter_instrument(labelInstrument)
        Instrument.association_Oeuvre_Instrument(id_oeuvre, id_instrument)

        flash("Ajout réussi !", "success")
        return render_template("pages/ajout_oeuvre.html", nom="BibPart", Listeoeuvre=listeoeuvre,
                               Listecompositeur=listecompositeur, Listetype=listetype, Listeforme=listeforme,
                               Listeinstrument=listeinstrument)

    return render_template("pages/ajout_oeuvre.html", nom="BibPart", Listeoeuvre=listeoeuvre,
                           Listecompositeur=listecompositeur, Listetype=listetype, Listeforme=listeforme,
                           Listeinstrument=listeinstrument)


@app.route("/ajout_partition", methods=["GET", "POST"])
def ajout_partition():
    """
    Route permettant l'ajout d'une partition et les données qui lui sont associées dans la BDD
    :return : affichage du template ajout_partition.html
    :rtype: page html
    """
    listepartition = Partition.query.all()
    listeoeuvre = Oeuvre.query.all()
    listeinstitution = Institution_conservation.query.all()

    if request.method == "POST":
        titrePartition = request.form.get("ajout_titre_partition", None)
        soustitrePartition = request.form.get("ajout_sous_titre_partition", None)
        formatPartition = request.form.get("ajout_format_partition", None)
        pagePartition = request.form.get("ajout_page_partition", None)
        statutPartition = request.form.get("ajout_statut_partition", None)
        visionneusePartition = request.form.get("ajout_visionneuse_partition", None)
        oeuvrePartition = request.form.get("ajout_oeuvre_partition", None)
        institutionPartition = request.form.get("ajout_institution_partition", None)
        recup = Oeuvre.query.filter(Oeuvre.titre_oeuvre == oeuvrePartition).first()
        recup2 = Institution_conservation.query.filter(
            Institution_conservation.nom_institution_conservation == institutionPartition).first()
        Partition.ajouter_partition(titrePartition, soustitrePartition, formatPartition, pagePartition, statutPartition,
                                    visionneusePartition, recup.id_oeuvre, recup2.id_institution_conservation)

        flash("Ajout réussi !", "success")
        return render_template("pages/ajout_partition.html", nom="BibPart", Listepartition=listepartition,
                               Listeoeuvre=listeoeuvre, Listeinstitution=listeinstitution)

    return render_template("pages/ajout_partition.html", nom="BibPart", Listepartition=listepartition,
                           Listeoeuvre=listeoeuvre, Listeinstitution=listeinstitution)


# ROUTES PERMETTANT LA MODIFICATION DES DONNÉES DES NOTICES

@app.route("/maj_oeuvre/<int:identifier>", methods=["GET", "POST"])
@login_required
def maj_oeuvre(identifier):
    """
    Route permettant la modification de la notice d'une oeuvre
    :param identifier: id de l'oeuvre
    :type identifier: int
    :return: redirection vers template index_oeuvres.html si succès ou vers template maj_oeuvre.html si échec
    :rtype: pages html
    """
    listecompositeur = Compositeur.query.all()
    listetype = Type.query.all()
    listeforme = Forme.query.all()
    listeinstrument = Instrument.query.all()

    # Si méthode "GET"
    if request.method == "GET":
        modif_oeuvre = Oeuvre.query.get(identifier)
        modif_oeuvre_compo = modif_oeuvre.compositeurs

        return render_template("pages/maj_oeuvre.html", oeuvre=modif_oeuvre, composi=modif_oeuvre_compo,
                               Listecompositeur=listecompositeur, Listetype=listetype, Listeforme=listeforme,
                               Listeinstrument=listeinstrument)

    # Si méthode "POST"
    else:
        # Application de la fonction modifier_oeuvre présente dans le fichier donnees.py
        statut, donnees = Oeuvre.modifier_oeuvre(
            Id_oeuvre=identifier,
            maj_titre=request.form.get("maj_titre", None),
            maj_compositeur=request.form.get("maj_compositeur", None),
            maj_date_oeuvre=request.form.get("maj_date_oeuvre", None),
            maj_forme=request.form.get("maj_forme", None),
            maj_type=request.form.get("maj_type", None),
            maj_audio=request.form.get("maj_audio", None),
            maj_instrument=request.form.get("maj_instrument", None))

        if statut is True:
            flash("Modification réussie !", "success")
            return redirect("/index_oeuvres")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            modif_oeuvre = Oeuvre.query.get(identifier)
            modif_oeuvre_compo = modif_oeuvre.compositeurs

            return render_template("pages/maj_oeuvre.html", nom="BibPArt", oeuvre=modif_oeuvre,
                                   composi=modif_oeuvre_compo)


@app.route("/maj_partition/<int:identifier>", methods=["GET", "POST"])
@login_required
def maj_partition(identifier):
    """
    Route permettant la modification de la notice d'une partition
    :param identifier: id de la partition
    :type identifier: int
    :return: redirection vers template index_partitions.html si succès ou vers template maj_partition.html si échec
    :rtype: pages html
    """
    listeinstitution = Institution_conservation.query.all()
    listeoeuvre = Oeuvre.query.all()

    # Si méthode "GET"
    if request.method == "GET":
        modif_partition = Partition.query.get(identifier)

        return render_template("pages/maj_partition.html", partition=modif_partition, Listeinstitution=listeinstitution,
                               Listeoeuvre=listeoeuvre)

    # Si méthode "POST"
    else:
        # Application de la fonction modifier_partition présente dans le fichier donnees.py
        statut, donnees = Partition.modifier_partition(
            Id_partition=identifier,
            maj_titre=request.form.get("maj_titre", None),
            maj_sous_titre=request.form.get("maj_sous_titre", None),
            maj_format=request.form.get("maj_format", None),
            maj_page=request.form.get("maj_page", None),
            maj_statut=request.form.get("maj_statut", None),
            maj_institution_conservation=request.form.get("maj_institution_conservation", None),
            maj_notice_oeuvre=request.form.get("maj_notice_oeuvre", None),
            maj_visionneuse=request.form.get("maj_visionneuse", None))

        if statut is True:
            flash("Modification réussie !", "success")
            return redirect("/index_partitions")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "danger")
            modif_partition = Partition.query.get(identifier)

            return render_template("pages/maj_partition.html", nom="BibPArt", partition=modif_partition)


@app.route("/maj_compositeur/<int:identifier>", methods=["GET", "POST"])
@login_required
def maj_compositeur(identifier):
    """
    Route permettant la modification de la notice d'un compositeur
    :param identifier: id du compositeur
    :type identifier: int
    :return: redirection vers template index_compositeurs.html si succès ou vers template maj_compositeur.html si échec
    :rtype: pages html
    """
    # Si méthode "GET"
    if request.method == "GET":
        modif_compositeur = Compositeur.query.get(identifier)

        return render_template("pages/maj_compositeur.html", compositeur=modif_compositeur)
    # Si méthode "POST"
    else:
        # Application de la fonction modifier_compositeur présente dans le fichier donnees.py
        statut, donnees = Compositeur.modifier_compositeur(
            Id_compositeur=identifier,
            maj_prenom=request.form.get("maj_prenom", None),
            maj_nom=request.form.get("maj_nom", None),
            maj_naissance=request.form.get("maj_naissance", None),
            maj_mort=request.form.get("maj_mort", None),
            maj_bio=request.form.get("maj_bio", None),
            maj_url=request.form.get("maj_url", None))

        if statut is True:
            flash("Modification réussie !", "success")
            return redirect("/index_compositeurs")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "danger")
            modif_compositeur = Compositeur.query.get(identifier)

            return render_template("pages/maj_compositeur.html", nom="BibPArt", compositeur=modif_compositeur)


# ROUTES PERMETTANT LES SUPPRESSIONS DE NOTICES

@app.route("/supprimer_oeuvre/<int:id_oeuvre>", methods=["POST", "GET"])
@login_required
def supprimer_oeuvre(id_oeuvre):
    """
    Route permettant la suppression d'une oeuvre et de ses données dans la BDD
    :param id_oeuvre : id de l'oeuvre
    :type id_oeuvre: int
    :return: redirection vers template index_oeuvres.html si succès ou vers template supprimer_oeuvre.html si échec
    :rtype: pages html
    """
    suppr_oeuvre = Oeuvre.query.get(id_oeuvre)

    if request.method == "POST":
        # Application de la fonction supprimer_oeuvre présente dans le fichier donnees.py
        statut = Oeuvre.supprimer_oeuvre(id_oeuvre=id_oeuvre)

        if statut is True:
            flash("Suppression réussie !", "success")
            return redirect("/index_oeuvres")
        else:
            flash("La suppression a échoué. Réessayez !", "danger")
            return redirect("/")
    else:
        return render_template("pages/supprimer_oeuvre.html", nom="BibPart", suppr_oeuvre=suppr_oeuvre)


@app.route("/supprimer_partition/<int:id_partition>", methods=["POST", "GET"])
@login_required
def supprimer_partition(id_partition):
    """
    Route permettant la suppression d'une partition et de ses données dans la BDD
    :param id_partition : id de la partition
    :type id_partition: int
    :return: redirection vers template index_partitions.html si succès ou vers template supprimer_partition.html si échec
    :rtype: pages html
    """
    suppr_partition = Partition.query.get(id_partition)

    if request.method == "POST":
        # Application de la fonction supprimer_partition présente dans le fichier donnees.py
        statut = Partition.supprimer_partition(id_partition=id_partition)

        if statut is True:
            flash("Suppression réussie !", "success")
            return redirect("/index_partitions")
        else:
            flash("La suppression a échoué. Réessayez !", "danger")
            return redirect("/")
    else:
        return render_template("pages/supprimer_partition.html", nom="BibPart", suppr_partition=suppr_partition)


@app.route("/supprimer_compositeur/<int:id_compositeur>", methods=["POST", "GET"])
@login_required
def supprimer_compositeur(id_compositeur):
    """
    Route permettant la suppression d'un compositeur et de ses données dans la BDD
    :param id_compositeur : id du compositeur
    :type id_compositeur: int
    :return: redirection vers template index_compositeurs.html si succès ou vers template supprimer_compositeur.html si échec
    :rtype: pages html
    """
    suppr_compositeur = Compositeur.query.get(id_compositeur)

    if request.method == "POST":
        # Application de la fonction supprimer_compositeur présente dans le fichier donnees.py
        statut = Compositeur.supprimer_compositeur(id_compositeur=id_compositeur)

        if statut is True:
            flash("Suppression réussie !", "success")
            return redirect("/index_compositeurs")
        else:
            flash("La suppression a échoué. Réessayez !", "danger")
            return redirect("/")
    else:
        return render_template("pages/supprimer_compositeur.html", nom="BibPart", suppr_compositeur=suppr_compositeur)
