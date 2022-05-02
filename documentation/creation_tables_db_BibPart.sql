# Script pour la création des tables de la BDD
BEGIN TRANSACTION;
DROP TABLE IF EXISTS "type";
CREATE TABLE IF NOT EXISTS "type" (
	"id_type"	INTEGER NOT NULL,
	"label_type"	TEXT NOT NULL,
	PRIMARY KEY("id_type" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "forme";
CREATE TABLE IF NOT EXISTS "forme" (
	"id_forme"	INTEGER NOT NULL,
	"label_forme"	TEXT NOT NULL,
	PRIMARY KEY("id_forme" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "instrument";
CREATE TABLE IF NOT EXISTS "instrument" (
	"id_instrument"	INTEGER NOT NULL,
	"label_instrument"	TEXT NOT NULL,
	PRIMARY KEY("id_instrument" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "relation_oeuvre_instrument";
CREATE TABLE IF NOT EXISTS "relation_oeuvre_instrument" (
	"oeuvre_id_oeuvre"	INTEGER NOT NULL,
	"instrument_id_instrument"	INTEGER NOT NULL,
	FOREIGN KEY("instrument_id_instrument") REFERENCES "instrument"("id_instrument"),
	FOREIGN KEY("oeuvre_id_oeuvre") REFERENCES "oeuvre"("id_oeuvre"),
	PRIMARY KEY("instrument_id_instrument","oeuvre_id_oeuvre")
);
DROP TABLE IF EXISTS "institution_conservation";
CREATE TABLE IF NOT EXISTS "institution_conservation" (
	"id_institution_conservation"	INTEGER NOT NULL,
	"nom_institution_conservation"	TEXT NOT NULL,
	"ville_institution_conservation"	TEXT,
	PRIMARY KEY("id_institution_conservation" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "compositeur";
CREATE TABLE IF NOT EXISTS "compositeur" (
	"id_compositeur"	INTEGER NOT NULL,
	"nom_compositeur"	TEXT NOT NULL,
	"prenom_compositeur"	TEXT,
	"annee_naissance_compositeur"	TEXT,
	"annee_mort_compositeur"	TEXT,
	"biographie_compositeur"	TEXT,
	"url_portrait_compositeur"	TEXT,
	PRIMARY KEY("id_compositeur" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "oeuvre";
CREATE TABLE IF NOT EXISTS "oeuvre" (
	"id_oeuvre"	INTEGER NOT NULL,
	"titre_oeuvre"	TEXT NOT NULL,
	"date_oeuvre"	TEXT,
	"audio_oeuvre"	TEXT,
	"compositeur_id_compositeur"	INTEGER NOT NULL,
	"type_id_type"	INTEGER NOT NULL,
	"forme_id_forme"	INTEGER NOT NULL,
	FOREIGN KEY("compositeur_id_compositeur") REFERENCES "compositeur"("id_compositeur"),
	FOREIGN KEY("type_id_type") REFERENCES "type"("id_type"),
	PRIMARY KEY("id_oeuvre" AUTOINCREMENT),
	FOREIGN KEY("forme_id_forme") REFERENCES "forme"("id_forme")
);
DROP TABLE IF EXISTS "utilisateur";
CREATE TABLE IF NOT EXISTS "utilisateur" (
	"id_utilisateur"	INTEGER NOT NULL,
	"nom_utilisateur"	TEXT NOT NULL,
	"login_utilisateur"	TEXT NOT NULL UNIQUE,
	"email_utilisateur"	TEXT NOT NULL,
	"password_utilisateur"	TEXT NOT NULL,
	PRIMARY KEY("id_utilisateur" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "partition";
CREATE TABLE IF NOT EXISTS "partition" (
	"id_partition"	INTEGER NOT NULL,
	"titre_partition"	TEXT NOT NULL,
	"nom_sous_partie_partition"	TEXT,
	"format_partition"	TEXT,
	"page_partition"	TEXT,
	"statut_partition"	TEXT,
	"url_visionneuse_IIIF"	TEXT,
	"oeuvre_id_oeuvre"	INTEGER NOT NULL,
	"institution_conservation_id_institution_conservation"	INTEGER NOT NULL,
	FOREIGN KEY("oeuvre_id_oeuvre") REFERENCES "oeuvre"("id_oeuvre"),
	PRIMARY KEY("id_partition" AUTOINCREMENT),
	FOREIGN KEY("institution_conservation_id_institution_conservation") REFERENCES "institution_conservation"("id_institution_conservation")
);
DROP TABLE IF EXISTS "authorship";
CREATE TABLE IF NOT EXISTS "authorship" (
	"authorship_id"	INTEGER,
	"authorship_utilisateur_id"	INTEGER,
	"authorship_oeuvre_id"	INTEGER,
	"authorship_partition_id"	INTEGER,
	"authorship_compositeur_id"	INTEGER,
	"authorship_date"	INTEGER,
	FOREIGN KEY("authorship_partition_id") REFERENCES "partition"("id_partition"),
	FOREIGN KEY("authorship_compositeur_id") REFERENCES "compositeur"("id_compositeur"),
	PRIMARY KEY("authorship_id" AUTOINCREMENT),
	FOREIGN KEY("authorship_oeuvre_id") REFERENCES "oeuvre"("id_oeuvre"),
	FOREIGN KEY("authorship_utilisateur_id") REFERENCES "utilisateur"("id_utilisateur")
);
COMMIT;
