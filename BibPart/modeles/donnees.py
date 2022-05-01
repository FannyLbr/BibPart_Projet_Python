from ..app import db
# Import de current_user() afin de suivre les activités de l'utilisateur connecté
from flask_login import current_user
# Import du module datetime pour spécifier un format de date
import datetime

# Création des modèles d'après la BDD db_BibPart.sqlite

# TABLES DE RELATION

# Table reliant la table des oeuvres et la table des instruments
Relation_oeuvre_instrument = db.Table("relation_oeuvre_instrument",
                                      db.Column("oeuvre_id_oeuvre", db.Integer, db.ForeignKey('oeuvre.id_oeuvre'),
                                                primary_key=True),
                                      db.Column("instrument_id_instrument", db.Integer,
                                                db.ForeignKey('instrument.id_instrument'), primary_key=True))


# Table reliant la table des utilisateurs et les tables oeuvre partition et compositeur
class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'))
    authorship_oeuvre_id = db.Column(db.Integer, db.ForeignKey('oeuvre.id_oeuvre'))
    authorship_partition_id = db.Column(db.Integer, db.ForeignKey('partition.id_partition'))
    authorship_compositeur_id = db.Column(db.Integer, db.ForeignKey('compositeur.id_compositeur'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    utilisateur = db.relationship("Utilisateur", back_populates="authorships")
    oeuvre = db.relationship("Oeuvre", back_populates="authorships")
    partition = db.relationship("Partition", back_populates="authorships")
    compositeur = db.relationship("Compositeur", back_populates="authorships")


# AUTRES TABLES

# Modèle de la classe Oeuvre
class Oeuvre(db.Model):
    __tablename__ = "oeuvre"
    id_oeuvre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre_oeuvre = db.Column(db.Text, nullable=False)
    date_oeuvre = db.Column(db.Text)
    audio_oeuvre = db.Column(db.Text)
    compositeur_id_compositeur = db.Column(db.Integer, db.ForeignKey('compositeur.id_compositeur'))
    type_id_type = db.Column(db.Integer, db.ForeignKey('type.id_type'))
    forme_id_forme = db.Column(db.Integer, db.ForeignKey('forme.id_forme'))
    compositeurs = db.relationship("Compositeur", back_populates="oeuvres")
    types = db.relationship("Type", back_populates="oeuvres")
    formes = db.relationship("Forme", back_populates="oeuvres")
    partitions = db.relationship("Partition", back_populates="oeuvres")
    instruments = db.relationship("Instrument", secondary="relation_oeuvre_instrument", back_populates="oeuvres")
    authorships = db.relationship("Authorship", back_populates="oeuvre")

    @staticmethod
    def ajouter_oeuvre(ajout_titre_oeuvre, ajout_date_oeuvre, ajout_audio_oeuvre, ajout_compositeur_oeuvre,
                       ajout_type_oeuvre, ajout_forme_oeuvre):
        """
        Fonction qui permet d'ajouter une oeuvre dans la BDD
        :param ajout_titre_oeuvre: titre de l'oeuvre
        :param ajout_date_oeuvre: date de l'oeuvre
        :param ajout_audio_oeuvre: audio de l'oeuvre
        :param ajout_compositeur_oeuvre: compositeur de l'oeuvre
        :param ajout_type_oeuvre: type de l'oeuvre
        :param ajout_forme_oeuvre: forme de l'oeuvre
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not ajout_titre_oeuvre:
            erreurs.append("le champ 'titre' est obligatoire")
        if not ajout_date_oeuvre:
            erreurs.append("le champ 'date' est obligatoire")
        if not ajout_compositeur_oeuvre:
            erreurs.append("le champ 'compositeur' est obligatoire")
        if not ajout_type_oeuvre:
            erreurs.append("le champ 'type' est obligatoire")
        if not ajout_forme_oeuvre:
            erreurs.append("le champ 'forme' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        test = Oeuvre.query.filter(Oeuvre.titre_oeuvre == ajout_titre_oeuvre) \
            .filter(Oeuvre.date_oeuvre == ajout_date_oeuvre) \
            .filter(Oeuvre.audio_oeuvre == ajout_audio_oeuvre) \
            .filter(Oeuvre.compositeur_id_compositeur == ajout_compositeur_oeuvre) \
            .filter(Oeuvre.type_id_type == ajout_type_oeuvre) \
            .filter(Oeuvre.forme_id_forme == ajout_forme_oeuvre).scalar()

        if test is None:
            noms = Oeuvre(titre_oeuvre=ajout_titre_oeuvre,
                          date_oeuvre=ajout_date_oeuvre,
                          audio_oeuvre=ajout_audio_oeuvre,
                          compositeur_id_compositeur=ajout_compositeur_oeuvre,
                          type_id_type=ajout_type_oeuvre,
                          forme_id_forme=ajout_forme_oeuvre)
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(oeuvre=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            recup = Oeuvre.query.filter(Oeuvre.titre_oeuvre == ajout_titre_oeuvre) \
                .filter(Oeuvre.date_oeuvre == ajout_date_oeuvre) \
                .filter(Oeuvre.audio_oeuvre == ajout_audio_oeuvre) \
                .filter(Oeuvre.compositeur_id_compositeur == ajout_compositeur_oeuvre) \
                .filter(Oeuvre.type_id_type == ajout_type_oeuvre) \
                .filter(Oeuvre.forme_id_forme == ajout_forme_oeuvre).first()
            return recup.id_oeuvre
        else:
            recup = Oeuvre.query.filter(Oeuvre.titre_oeuvre == ajout_titre_oeuvre) \
                .filter(Oeuvre.date_oeuvre == ajout_date_oeuvre) \
                .filter(Oeuvre.audio_oeuvre == ajout_audio_oeuvre) \
                .filter(Oeuvre.compositeur_id_compositeur == ajout_compositeur_oeuvre) \
                .filter(Oeuvre.type_id_type == ajout_type_oeuvre) \
                .filter(Oeuvre.forme_id_forme == ajout_forme_oeuvre).first()
            return recup.id_oeuvre

    @staticmethod
    def modifier_oeuvre(Id_oeuvre, maj_titre, maj_date_oeuvre, maj_compositeur, maj_forme, maj_type, maj_instrument,
                        maj_audio):
        """
        Fonction qui permet de modifier les données d'une oeuvre dans la BDD
        :param Id_oeuvre: id de l'oeuvre (int)
        :param maj_titre: titre de l'oeuvre (str)
        :param maj_date_oeuvre: date de création de l'oeuvre (str)
        :param maj_compositeur: nom du compositeur (str)
        :param maj_forme: forme de l'oeuvre (str)
        :param maj_type: type de l'oeuvre (str)
        :param maj_instrument: instrument de l'oeuvre (str)
        :param maj_audio: audio de l'oeuvre (str)
        :return: modifications de données s'il n'y a pas d'erreurs
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not maj_titre:
            erreurs.append("le champ 'titre' est obligatoire")
        if not maj_compositeur:
            erreurs.append("le champ 'compositeur' est obligatoire")
        if not maj_date_oeuvre:
            erreurs.append("le champ 'date' est obligatoire")
        if not maj_forme:
            erreurs.append("le champ 'forme' est obligatoire")
        if not maj_type:
            erreurs.append("le champ 'type' est obligatoire")
        if not maj_instrument:
            erreurs.append("le champ 'instrument' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Récupération de l'oeuvre
        update_oeuvre = Oeuvre.query.get(Id_oeuvre)
        # Modifications des données
        update_oeuvre.titre_oeuvre = maj_titre
        update_oeuvre.compositeur_id_compositeur = maj_compositeur
        update_oeuvre.date_oeuvre = maj_date_oeuvre
        update_oeuvre.forme_id_forme = maj_forme
        update_oeuvre.type_id_type = maj_type
        update_oeuvre.audio_oeuvre = maj_audio
        # Cette ligne ne fonctionne pas : update_oeuvre.instruments = maj_instrument

        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(update_oeuvre)
            # La modification est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(oeuvre=update_oeuvre, utilisateur=current_user))
            # Confirmation de l'ajout de la modification dans la BDD
            db.session.commit()
            return True, update_oeuvre

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_oeuvre(id_oeuvre):
        """
        Fonction qui permet de supprimer une oeuvre et ses données de la BDD
        :param id_oeuvre: id de l'oeuvre
        :type id_oeuvre: int
        :return: suppression des données s'il n'y a pas d'erreurs
        """
        # Récupération de l'oeuvre
        suppr_oeuvre = Oeuvre.query.get(id_oeuvre)

        try:
            # Les données sont supprimées de la BDD
            db.session.delete(suppr_oeuvre)
            # La suppression est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(oeuvre=suppr_oeuvre, utilisateur=current_user))
            # Confirmation de la suppression dans la BDD
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


# Modèle de la classe Partition
class Partition(db.Model):
    __tablename__ = "partition"
    id_partition = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre_partition = db.Column(db.Text, nullable=False)
    nom_sous_partie_partition = db.Column(db.Text)
    format_partition = db.Column(db.Text)
    page_partition = db.Column(db.Text)
    statut_partition = db.Column(db.Text)
    url_visionneuse_IIIF = db.Column(db.Text)
    oeuvre_id_oeuvre = db.Column(db.Integer, db.ForeignKey('oeuvre.id_oeuvre'))
    institution_conservation_id_institution_conservation = db.Column(db.Integer, db.ForeignKey(
        'institution_conservation.id_institution_conservation'))
    oeuvres = db.relationship("Oeuvre", back_populates="partitions")
    institutions_conservation = db.relationship("Institution_conservation", back_populates="partitions")
    authorships = db.relationship("Authorship", back_populates="partition")

    @staticmethod
    def ajouter_partition(ajout_titre_partition, ajout_sous_titre_partition, ajout_format_partition,
                          ajout_page_partition, ajout_statut_partition, ajout_visionneuse_partition,
                          ajout_oeuvre_partition, ajout_institution_partition):
        """
        Fonction qui permet d'ajouter une partition dans la BDD
        :param ajout_titre_partition: titre de la partition
        :param ajout_sous_titre_partition: sous-titre de la partition
        :param ajout_format_partition: format de la partition
        :param ajout_page_partition: nombre de pages de la partition
        :param ajout_statut_partition: statut de la partition
        :param ajout_visionneuse_partition: visionneuse de la partition
        :param ajout_oeuvre_partition: oeuvre de la partition
        :param ajout_institution_partition: institution de conservation de la partition
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not ajout_titre_partition:
            erreurs.append("le champ 'titre' est obligatoire")
        if not ajout_oeuvre_partition:
            erreurs.append("le champ 'oeuvre' est obligatoire")
        if not ajout_institution_partition:
            erreurs.append("le champ 'institution de conservation' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        test = Partition.query.filter(Partition.titre_partition == ajout_titre_partition) \
            .filter(Partition.nom_sous_partie_partition == ajout_sous_titre_partition) \
            .filter(Partition.format_partition == ajout_format_partition) \
            .filter(Partition.page_partition == ajout_page_partition) \
            .filter(Partition.statut_partition == ajout_statut_partition) \
            .filter(Partition.url_visionneuse_IIIF == ajout_visionneuse_partition) \
            .filter(Partition.oeuvre_id_oeuvre == ajout_oeuvre_partition) \
            .filter(
            Partition.institution_conservation_id_institution_conservation == ajout_institution_partition).scalar()

        if test is None:
            noms = Partition(titre_partition=ajout_titre_partition,
                             nom_sous_partie_partition=ajout_sous_titre_partition,
                             format_partition=ajout_format_partition, page_partition=ajout_page_partition,
                             statut_partition=ajout_statut_partition, url_visionneuse_IIIF=ajout_visionneuse_partition,
                             oeuvre_id_oeuvre=ajout_oeuvre_partition,
                             institution_conservation_id_institution_conservation=ajout_institution_partition)
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(partition=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            recup = Partition.query.filter(Partition.titre_partition == ajout_titre_partition) \
                .filter(Partition.nom_sous_partie_partition == ajout_sous_titre_partition) \
                .filter(Partition.format_partition == ajout_format_partition) \
                .filter(Partition.page_partition == ajout_page_partition) \
                .filter(Partition.statut_partition == ajout_statut_partition) \
                .filter(Partition.url_visionneuse_IIIF == ajout_visionneuse_partition) \
                .filter(Partition.oeuvre_id_oeuvre == ajout_oeuvre_partition) \
                .filter(
                Partition.institution_conservation_id_institution_conservation == ajout_institution_partition).first()
            return recup.id_partition
        else:
            recup = Partition.query.filter(Partition.titre_partition == ajout_titre_partition) \
                .filter(Partition.nom_sous_partie_partition == ajout_sous_titre_partition) \
                .filter(Partition.format_partition == ajout_format_partition) \
                .filter(Partition.page_partition == ajout_page_partition) \
                .filter(Partition.statut_partition == ajout_statut_partition) \
                .filter(Partition.url_visionneuse_IIIF == ajout_visionneuse_partition) \
                .filter(Partition.oeuvre_id_oeuvre == ajout_oeuvre_partition) \
                .filter(
                Partition.institution_conservation_id_institution_conservation == ajout_institution_partition).first()
            return recup.id_partition

    @staticmethod
    def modifier_partition(Id_partition, maj_titre, maj_sous_titre, maj_format, maj_page, maj_statut,
                           maj_institution_conservation, maj_notice_oeuvre, maj_visionneuse):
        """
        Fonction qui permet de modifier les métadonnées d'une partition dans la BDD
        :param Id_partition: id de la partition (int)
        :param maj_titre: titre de la partition (str)
        :param maj_sous_titre: sous-titre de la partition (str)
        :param maj_format: format de la partition (str)
        :param maj_page: nombre de pages de la partition (str)
        :param maj_statut: statut de la partition (str)
        :param maj_institution_conservation: institution de conservation de la partition (str)
        :param maj_notice_oeuvre: oeuvre à laquelle se rattache la partition (str)
        :param maj_visionneuse: visionneuse de la partition (str)
        :return: modifications de données s'il n'y a pas d'erreurs
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not maj_titre:
            erreurs.append("le champ 'titre' est obligatoire")
        if not maj_institution_conservation:
            erreurs.append("le champ 'institution de conservation' est obligatoire")
        if not maj_notice_oeuvre:
            erreurs.append("le champ 'notice de l'oeuvre' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Récupération de la partition
        update_partition = Partition.query.get(Id_partition)
        # Modifications des données
        update_partition.titre_partition = maj_titre
        update_partition.nom_sous_partie_partition = maj_sous_titre
        update_partition.format_partition = maj_format
        update_partition.page_partition = maj_page
        update_partition.statut_partition = maj_statut
        update_partition.institution_conservation_id_institution_conservation = maj_institution_conservation
        update_partition.oeuvre_id_oeuvre = maj_notice_oeuvre
        update_partition.url_visionneuse_IIIF = maj_visionneuse

        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(update_partition)
            # La modification est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(partition=update_partition, utilisateur=current_user))
            # Confirmation de l'ajout de la modification dans la BDD
            db.session.commit()
            return True, update_partition

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_partition(id_partition):
        """
        Fonction qui permet de supprimer une partition et ses données de la BDD
        :param id_partition: id de la partition
        :type id_partition: int
        :return: suppression des données s'il n'y a pas d'erreurs
        """
        # Récupération de la partition
        suppr_partition = Partition.query.get(id_partition)

        try:
            # Les données sont supprimées de la BDD
            db.session.delete(suppr_partition)
            # La suppression est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(partition=suppr_partition, utilisateur=current_user))
            # Confirmation de la suppression dans la BDD
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


# Modèle de la classe Compositeur
class Compositeur(db.Model):
    __tablename__ = "compositeur"
    id_compositeur = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom_compositeur = db.Column(db.Text, nullable=False)
    prenom_compositeur = db.Column(db.Text)
    annee_naissance_compositeur = db.Column(db.Text)
    annee_mort_compositeur = db.Column(db.Text)
    biographie_compositeur = db.Column(db.Text)
    url_portrait_compositeur = db.Column(db.Text)
    oeuvres = db.relationship("Oeuvre", back_populates="compositeurs")
    authorships = db.relationship("Authorship", back_populates="compositeur")

    @staticmethod
    def ajouter_compositeur(ajout_nom_compo, ajout_prenom_compo, ajout_naissance_compo, ajout_mort_compo,
                            ajout_bio_compo, ajout_portrait_compo):
        """
        Fonction qui permet d'ajouter un compositeur dans la BDD
        :param ajout_nom_compo: nom du compositeur
        :param ajout_prenom_compo: prénom du compositeur
        :param ajout_naissance_compo: année de naissance du compositeur
        :param ajout_mort_compo: année de mort du compositeur
        :param ajout_bio_compo: biographie du compositeur
        :param ajout_portrait_compo: portrait du compositeur
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []
        if not ajout_nom_compo:
            erreurs.append("le champ 'nom' est obligatoire")
        if not ajout_prenom_compo:
            erreurs.append("le champ 'prenom' est obligatoire")
        if not ajout_bio_compo:
            erreurs.append("le champ 'courte biographie' est obligatoire")
        if len(ajout_naissance_compo) != 4:
            erreurs.append(
                "les dates doivent être écrites au format suivant : AAAA")
        if len(ajout_mort_compo) != 4:
            erreurs.append(
                "les dates doivent être écrites au format suivant : AAAA")

        # Cette condition permet d'éviter d'enregistrer deux fois une même donnée dans la BDD, mais cela ne fonctionne
        # pas très bien car lorsque je crée une nouvelle donnée cela enregistre le chiffre 0 au lieu du mot
        # ajout_nom_compo = Compositeur.query.filter(db.and_(Compositeur.nom_compositeur == ajout_nom_compo,
        # Compositeur.prenom_compositeur == ajout_prenom_compo)).count()
        # if ajout_nom_compo > 0:
        # erreurs.append("le compositeur existe déjà dans la base de données")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        noms = Compositeur(nom_compositeur=ajout_nom_compo,
                           prenom_compositeur=ajout_prenom_compo,
                           annee_naissance_compositeur=ajout_naissance_compo,
                           annee_mort_compositeur=ajout_mort_compo,
                           biographie_compositeur=ajout_bio_compo,
                           url_portrait_compositeur=ajout_portrait_compo)
        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(compositeur=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            return True, noms

        except Exception as erreur:
            # Annulation des ajouts si erreur
            return False, [str(erreur)]

    @staticmethod
    def modifier_compositeur(Id_compositeur, maj_prenom, maj_nom, maj_naissance, maj_mort, maj_bio, maj_url):
        """
        Fonction qui permet de modifier les métadonnées d'un compositeur dans la BDD
        :param Id_compositeur: id du compositeur (int)
        :param maj_prenom: prenom du compositeur (str)
        :param maj_nom: nom du compositeur (str)
        :param maj_naissance: année naissance du compositeur (str)
        :param maj_mort: année mort du compositeur (str)
        :param maj_bio: biographie du compositeur (str)
        :param maj_url: image du compositeur (str)
        :return: modifications de données s'il n'y a pas d'erreurs
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not maj_prenom:
            erreurs.append("le champ 'prénom' est obligatoire")
        if not maj_nom:
            erreurs.append("le champ 'nom' est obligatoire")
        if not maj_naissance:
            erreurs.append("le champ 'année naissance' est obligatoire")
        if not maj_mort:
            erreurs.append("le champ 'année mort' est obligatoire")
        if not maj_bio:
            erreurs.append("le champ 'courte biographie' est obligatoire")
        if len(maj_naissance) != 4:
            erreurs.append(
                "les dates doivent être écrites au format suivant : AAAA")
        if len(maj_mort) != 4:
            erreurs.append(
                "les dates doivent être écrites au format suivant : AAAA")

        if len(erreurs) > 0:
            return False, erreurs

        # Récupération du compositeur
        update_compositeur = Compositeur.query.get(Id_compositeur)
        # Modifications des données
        update_compositeur.prenom_compositeur = maj_prenom
        update_compositeur.nom_compositeur = maj_nom
        update_compositeur.annee_naissance_compositeur = maj_naissance
        update_compositeur.annee_mort_compositeur = maj_mort
        update_compositeur.biographie_compositeur = maj_bio
        update_compositeur.url_portrait_compositeur = maj_url

        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(update_compositeur)
            # La modification est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(compositeur=update_compositeur, utilisateur=current_user))
            # Confirmation de l'ajout de la modification dans la BDD
            db.session.commit()
            return True, update_compositeur

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_compositeur(id_compositeur):
        """
        Fonction qui permet de supprimer un compositeur et ses données de la BDD
        :param id_compositeur: id du compositeur
        :type id_compositeur: int
        :return: suppression des données s'il n'y a pas d'erreurs
        """
        # Récupération du compositeur
        suppr_compositeur = Compositeur.query.get(id_compositeur)

        try:
            # Les données sont supprimées de la BDD
            db.session.delete(suppr_compositeur)
            # La suppression est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(compositeur=suppr_compositeur, utilisateur=current_user))
            # Confirmation de la suppression dans la BDD
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


# Modèle de la classe Type
class Type(db.Model):
    __tablename__ = "type"
    id_type = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_type = db.Column(db.Text, nullable=False)
    oeuvres = db.relationship("Oeuvre", back_populates="types")


# Modèle de la classe Instrument
class Instrument(db.Model):
    __tablename__ = "instrument"
    id_instrument = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_instrument = db.Column(db.Text, nullable=False)
    oeuvres = db.relationship("Oeuvre", secondary="relation_oeuvre_instrument", back_populates="instruments")

    @staticmethod
    def ajouter_instrument(ajout_label_instrument):
        """
        Fonction qui permet d'ajouter un instrument dans la BDD
        :param ajout_label_instrument: label de l'instrument
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []

        if not ajout_label_instrument:
            erreurs.append("le champ 'instrument' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        test = Instrument.query.filter(Instrument.label_instrument == ajout_label_instrument).scalar()

        if test is None:
            noms = Instrument(label_instrument=ajout_label_instrument)
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(instrument=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            recup = Instrument.query.filter(Instrument.label_instrument == ajout_label_instrument).first()
            return recup.id_instrument
        else:
            recup = Instrument.query.filter(Instrument.label_instrument == ajout_label_instrument).first()
            return recup.id_instrument

    @staticmethod
    def association_Oeuvre_Instrument(oeuvreid, instrumentid):
        """
        Fonction qui permet de faire la jointure entre les deux tables
        :param oeuvreid: id de l'oeuvre
        :param instrumentid: id de l'instrument
        """
        instrumentassoc = Instrument.query.filter(Instrument.id_instrument == instrumentid).first()
        oeuvreassoc = Oeuvre.query.filter(Oeuvre.id_oeuvre == oeuvreid).first()

        instrumentassoc.oeuvres.append(oeuvreassoc)
        db.session.add(instrumentassoc)
        db.session.commit()


# Modèle de la classe Forme
class Forme(db.Model):
    __tablename__ = "forme"
    id_forme = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_forme = db.Column(db.Text, nullable=False)
    oeuvres = db.relationship("Oeuvre", back_populates="formes")

    @staticmethod
    def ajouter_forme(ajout_label_forme):
        """
        Fonction qui permet d'ajouter une forme dans la BDD
        :param ajout_label_forme: label de la forme
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []
        if not ajout_label_forme:
            erreurs.append("le champ 'label forme' est obligatoire")

        # Cette condition permet d'éviter d'enregistrer deux fois une même donnée dans la BDD, mais cela ne fonctionne
        # pas très bien car lorsque je crée une nouvelle donnée cela enregistre le chiffre 0 au lieu du mot
        # ajout_label_forme = Forme.query.filter(Forme.label_forme == ajout_label_forme).count()

        # if ajout_label_forme > 0:
        # erreurs.append("la forme existe déjà dans la base de données")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        noms = Forme(label_forme=ajout_label_forme)
        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(forme=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            return True, noms

        except Exception as erreur:
            # Annulation des ajouts si erreur
            return False, [str(erreur)]


# Modèle de la classe Institution_conservation
class Institution_conservation(db.Model):
    __tablename__ = "institution_conservation"
    id_institution_conservation = db.Column(db.Integer, unique=True, nullable=False, primary_key=True,
                                            autoincrement=True)
    nom_institution_conservation = db.Column(db.Text, nullable=False)
    ville_institution_conservation = db.Column(db.Text)
    partitions = db.relationship("Partition", back_populates="institutions_conservation")

    @staticmethod
    def ajouter_institution(ajout_nom_institution, ajout_ville_institution):
        """
        Fonction qui permet d'ajouter une institution de conservation dans la BDD
        :param ajout_nom_institution: nom de l'institution de conservation
        :param ajout_ville_institution: ville de l'institution de conservation
        :return: ajout de nouvelles données s'il n'y a pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []
        if not ajout_nom_institution:
            erreurs.append("le champ 'nom institution' est obligatoire")
        if not ajout_ville_institution:
            erreurs.append("le champ 'localisation' est obligatoire")

        if len(erreurs) > 0:
            return False, erreurs

        # Ajout d'une nouvelle donnée dans la BDD si pas d'erreur
        noms = Institution_conservation(nom_institution_conservation=ajout_nom_institution,
                                        ville_institution_conservation=ajout_ville_institution)
        try:
            # Les données sont ajoutées dans la BDD
            db.session.add(noms)
            # L'ajout est associée à l'utilisateur et cette association est ajoutée dans la BDD
            db.session.add(Authorship(institution=noms, utilisateur=current_user))
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            return True, noms

        except Exception as erreur:
            # Annulation des ajouts si erreur
            return False, [str(erreur)]
