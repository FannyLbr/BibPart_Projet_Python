# Import pour sécuriser la création de mots de passe
from werkzeug.security import generate_password_hash, check_password_hash
# Import pour avoir un ensemble de propriétés concernant la connexion d'un utilisateur
from flask_login import UserMixin

from .. app import db, login


# Modèle de la classe Utilisateur
class Utilisateur(UserMixin, db.Model):
    __tablename__ = "utilisateur"
    id_utilisateur = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom_utilisateur = db.Column(db.Text, nullable=False)
    login_utilisateur = db.Column(db.Text, nullable=False, unique=True)
    email_utilisateur = db.Column(db.Text, nullable=False)
    password_utilisateur = db.Column(db.Text, nullable=False)
    authorships = db.relationship("Authorship", back_populates="utilisateur")

    @staticmethod
    def identification(login, motdepasse):
        """
        Fonction permettant d'identifier un utilisateur
        :param login: login de l'utilisateur
        :param motdepasse: mot de passe envoyé par l'utilisateur
        :returns: Connexion de l'utilisateur si pas d'erreur, sinon None
        """
        user = Utilisateur.query.filter(Utilisateur.login_utilisateur == login).first()
        if user and check_password_hash(user.password_utilisateur, motdepasse):
            return user
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """
        Fonction permettant de créer un compte utilisateur
        :param login: login de l'utilisateur
        :param email: email de l'utilisateur
        :param nom: nom de l'utilisateur
        :param motdepasse: mot de passe de l'utilisateur (minimum 6 caractères)
        :returns: Création du compte de l'utilisateur si pas d'erreur
        """
        # Gestion des erreurs lorsque les champs obligatoires ne sont pas remplis
        erreurs = []
        if not login:
            erreurs.append("le login fourni est vide")
        if not email:
            erreurs.append("l'email fourni est vide")
        if not nom:
            erreurs.append("le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("le mot de passe fourni est vide ou trop court")

        # Vérification que l'email ou le login est unique
        uniques = Utilisateur.query.filter(
            db.or_(Utilisateur.email_utilisateur == email, Utilisateur.login_utilisateur == login)
        ).count()
        if uniques > 0:
            erreurs.append("l'email ou le login sont déjà inscrits dans notre base de données")

        if len(erreurs) > 0:
            return False, erreurs

        # Création des données de l'utilisateur
        user = Utilisateur(
            nom_utilisateur=nom,
            login_utilisateur=login,
            email_utilisateur=email,
            # "sha256" permet d'encrypter le mot de passe de l'utilisateur dans la BDD
            password_utilisateur=generate_password_hash(motdepasse, method="sha256"))

        try:
            # Les données de l'utilisateur sont ajoutées dans la BDD
            db.session.add(user)
            # Confirmation de l'ajout dans la BDD
            db.session.commit()
            return True, user

        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.id_utilisateur


@login.user_loader
def trouver_utilisateur_via_id(id_utilisateur):
    """
    Fonction permettant de récupérer un utilisateur grâce à son identifiant
    :return: id de l'utilisateur
    :rtype: int
    """
    return Utilisateur.query.get(int(id_utilisateur))
