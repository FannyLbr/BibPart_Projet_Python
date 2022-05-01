<!--Script insertion des données dans la BDD-->
BEGIN TRANSACTION;
INSERT INTO "type" ("id_type","label_type") VALUES (1,'musique vocale'),
 (2,'musique instrumentale'),
 (3,'musique vocale et instrumentale');
INSERT INTO "forme" ("id_forme","label_forme") VALUES (1,'pièce de caractère'),
 (2,'concerto'),
 (3,'sonate'),
 (4,'messe'),
 (5,'valse'),
 (6,'opéra');
INSERT INTO "instrument" ("id_instrument","label_instrument") VALUES (1,'clavecin'),
 (2,'piano'),
 (3,'violon'),
 (4,'orchestre'),
 (5,'soprano'),
 (6,'basse'),
 (7,'ténor'),
 (8,'choeur');
INSERT INTO "relation_oeuvre_instrument" ("oeuvre_id_oeuvre","instrument_id_instrument") VALUES (1,1),
 (2,2),
 (2,4),
 (3,4),
 (3,5),
 (3,6),
 (3,7),
 (3,8),
 (4,2),
 (5,3),
 (5,2),
 (6,8),
 (6,4),
 (7,3),
 (7,4),
 (8,3),
 (8,4),
 (9,2),
 (10,2);
INSERT INTO "institution_conservation" ("id_institution_conservation","nom_institution_conservation","ville_institution_conservation") VALUES (1,'Bibliothèque nationale de France, Département Musique','Paris');
INSERT INTO "compositeur" ("id_compositeur","nom_compositeur","prenom_compositeur","annee_naissance_compositeur","annee_mort_compositeur","biographie_compositeur","url_portrait_compositeur") VALUES (1,'Rameau','Jean-Philippe','1683','1764','Organiste, compositeur français et théoricien de la musique de la fin de l’époque baroque et du début du classicisme. Il est principalement connu pour ses œuvres lyriques, en particulier le genre de l’opéra-ballet, et pour sa musique pour clavecin. Il s’inscrit aussi comme une référence théorique sur l’harmonie classique. ','https://upload.wikimedia.org/wikipedia/commons/4/4a/A._de_Saint-Aubin_d%27apr%C3%A8s_J.-J._Caffi%C3%A9ri%2C_portrait_de_J.-Ph._Rameau%2C_d%C3%A9tail_%281762%29.jpg'),
 (2,'Mozart','Wolfgang Amadeus','1756','1791','Compositeur autrichien et virtuose du clavecin et du violon. Il est la figure majeure de la période du classicisme. Il est un génie de la composition ayant créé de très nombreuses œuvres embrassant tous les genres musicaux de son époque. ','https://upload.wikimedia.org/wikipedia/commons/4/47/Croce-Mozart-Detail.jpg'),
 (3,'Fauré','Gabriel','1845','1924','Pianiste, organiste et compositeur français de la fin du XIXe siècle. Étant influencé par Camille Saint-Saëns et Frédéric Chopin, il a largement contribué à l’essor de la musique française. ','https://upload.wikimedia.org/wikipedia/commons/d/de/Gabriel_Faure.jpg'),
 (4,'Chopin','Frédéric','1810','1849','Pianiste et compositeur franco-polonais. Il est considéré comme l’un des plus grands compositeurs de la période romantique. Il est aussi l’un des pianistes les plus célèbres de son époque, ayant fait évoluer la technique de son instrument. ','https://upload.wikimedia.org/wikipedia/commons/f/fc/Frederic_Chopin_gross_A.jpg'),
 (5,'Saint-Saëns','Camille','1835','1921','Pianiste, organiste et compositeur français de l’époque romantique. Auteur de nombreuses œuvres diverses, il est l’un des musiciens les plus prolifiques de son époque. Ces œuvres ont marqué l’évolution de la musique à l’aube du XXe siècle.','https://upload.wikimedia.org/wikipedia/commons/9/9b/Camille_Saint-Saens_b_Meurisse_1921.jpg'),
 (6,'Debussy','Claude','1862','1918','Compositeur français. Il marqua son époque par son anticonformisme et ouvra les portes de l’avant-garde musicale. ','https://upload.wikimedia.org/wikipedia/commons/f/f9/Claude_Debussy_ca_1908%2C_foto_av_F%C3%A9lix_Nadar.jpg');
INSERT INTO "oeuvre" ("id_oeuvre","titre_oeuvre","date_oeuvre","audio_oeuvre","compositeur_id_compositeur","type_id_type","forme_id_forme") VALUES (1,'La Dauphine RCT 12','1747','https://www.youtube.com/embed/nrh2mds5prE ',1,2,1),
 (2,'Concerto pour piano et orchestre en la majeur KV 488 n°23','1786','https://www.youtube.com/embed/Qll0vK3uTHA',2,2,2),
 (3,'Don Giovanni KV 527','1787','https://www.youtube.com/embed/Hnd5ULYG2no',2,3,6),
 (4,'Suite Dolly op. 56','1896','https://www.youtube.com/embed/WKnTHR6Vwac',3,2,1),
 (5,'Sonate pour violon et piano en la majeur op. 13 n°1','1875-1876','https://www.youtube.com/embed/IG6byr172UU',3,2,3),
 (6,'Messe de Requiem op. 48','1888','https://www.youtube.com/embed/08GyEGqBC70',3,3,4),
 (7,'Concerto de violon en ré mineur op. 14 ','1879','https://www.youtube.com/embed/-JK1aSBq2wE',3,2,2),
 (8,'Concerto pour violon en si mineur R 198 n°3','1880','https://www.youtube.com/embed/VIdQjYI0gzg',5,2,2),
 (9,'La plus que lente valse pour piano FL 128','1910','https://www.youtube.com/embed/3gE1CqCQQqA',6,2,5),
 (10,'Valse en do dièse mineur CT 213','1847-1848','https://www.youtube.com/embed/UJXcjiRhtMo',4,2,5);
INSERT INTO "utilisateur" ("id_utilisateur","nom_utilisateur","login_utilisateur","email_utilisateur","password_utilisateur") VALUES (1,'essai','essai','essai@gmail.com','sha256$8m0gqAH0ZBzflk43$a14baf793f6be8a3e31d97be0d68c4fe566cd9064d0e9b88bae8ed7dc37edfda');
INSERT INTO "partition" ("id_partition","titre_partition","nom_sous_partie_partition","format_partition","page_partition","statut_partition","url_visionneuse_IIIF","oeuvre_id_oeuvre","institution_conservation_id_institution_conservation") VALUES (1,'La Dauphine RCT 12','',' 21,5 x 27,5 cm','2 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b7400130b',1,1),
 (2,'Concerto pour piano et orchestre en la majeur KV 488 n°23','Allegro - Adagio - Allegro assai','23,5 x 32 cm','100 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002037r',2,1),
 (3,'Don Giovanni KV 527','Ouvertura','25 x 29 cm','27 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002493z',3,1),
 (4,'Don Giovanni KV 527','Atto Imo - Scena I.-VII.','25 x 29 cm','101 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002497r',3,1),
 (5,'Don Giovanni KV 527','Atto Imo - Scena VIII.-XVI.','25 x 29 cm','96 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002495v',3,1),
 (6,'Don Giovanni KV 527','Atto Imo - Finale','25 x 29 cm','78 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b550024986',3,1),
 (7,'Don Giovanni KV 527','Atto 2do - Scena I.-VII.','25 x 29 cm','92 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002494d',3,1),
 (8,'Don Giovanni KV 527','Atto 2do - Scena VIII.-XVI.','25 x 29 cm','75 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002499n',3,1),
 (9,'Don Giovanni KV 527','Atto 2do - Finale','25 x 29 cm','81 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b550025008',3,1),
 (10,'Don Giovanni KV 527','Aria - D. Ottavio','25 x 29 cm','8 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b550024969',3,1),
 (11,'Suite Dolly op. 56','N°6 Le Pas Espagnol (4 mains)','35 x 27 cm','10 p. de musique','partition complète (partie du second piano)','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b550008428',4,1),
 (12,'Sonate pour violon et piano en la majeur op. 13 n°1','Allegro - Andante - Scherzo - Finalle','35 x 27 cm','64 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55009612c',5,1),
 (13,'Messe de Requiem op. 48','Introït et Kyrie','35,4 x 27,9 cm','25 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/bpt6k859978j',6,1),
 (14,'Messe de Requiem op. 48','Sanctus','35 x 27,4 cm','15 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55009473j',6,1),
 (15,'Messe de Requiem op. 48','Agnus Dei','35 x 27,4 cm','20 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b550094723',6,1),
 (16,'Messe de Requiem op. 48','In paradisum','35,2 x 27,2 cm','15 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55009471n',6,1),
 (17,'Concerto de violon en ré mineur op. 14','Allegro','35 x 27 cm','64 p. de musique','conducteur incomplet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b525057032',7,1),
 (18,'Concerto pour violon en si mineur R 198 n°3','Allegro non troppo - Andantino quadi allegretto - Molto moderato e mastoso','35,5 x 27 cm','191 p. de musique','conducteur complet','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55001033m',8,1),
 (19,'La plus que lente valse pour piano FL 128','Lent','40 x 29 cm','3 p. de musique','partition complète','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b52500675r',9,1),
 (20,'Valse en do dièse mineur CT 213','Valse','22 x 28,5 cm','1 p. de musique','partition complète','https://gallica.bnf.fr/view3if/ga/ark:/12148/btv1b55002555k',10,1);
COMMIT;