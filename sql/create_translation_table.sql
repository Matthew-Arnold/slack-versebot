CREATE TABLE translation_stats (id SERIAL PRIMARY KEY, name VARCHAR(60), trans VARCHAR(20), lang VARCHAR(20), count INTEGER DEFAULT 0, last_used TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW());

INSERT INTO translation_stats (name,trans) VALUES 
	('Amuzgo de Guerrero','AMU','Amuzgo Guerrero'), 
	('Arabic Bible: Easy-to-Read Version','ERV-AR','Arabic'), 
	('Arabic Life Application Bible','ALAB','Arabic'), 
	('Awadhi Bible: Easy-to-Read Version','ERV-AWA','Awadhi'), 
	('1940 Bulgarian Bible','BG1940','Bulgarian'),
	('Bulgarian Bible','BULG','Bulgarian'), 
	('Bulgarian New Testament: Easy-to-Read Version','ERV-BG','Bulgarian'), 
	('Bulgarian Protestant Bible','BPB','Bulgarian'), 
	('Chinanteco de Comaltepec','CCO','Chinanteco de Comaltepec'), 
	('Ang Pulong Sa Dios','APSD-CEB','Cebuano'), 
	('Cherokee New Testament','CHR','Cherokee'), 
	('Cakchiquel Occidental','CKW','Kaqchikel'), 
	('Bible 21','B21','Czech'), 
	('Slovo na cestu','SNC','Czech'), 
	('Bibelen på hverdagsdansk','BPH','Danish'),
	('Dette er Biblen på dansk','DN1933','Danish'), 
	('Hoffnung für Alle','HOF','German'), 
	('Luther Bibel 1545','LUTH1545','German'), 
	('Neue Genfer Übersetzung','NGU-DE','German'), 
	('Schlachter 1951','SCH1951','German'), 
	('Schlachter 2000','SCH2000','German'), 
	('21st Century King James Version','KJ21','English'), 
	('American Standard Version','ASV','English'), 
	('Amplified Bible','AMP','English'), 
	('Common English Bible','CEB','English'), 
	('Complete Jewish Bible','CJB','English'), 
	('Contemporary English Version','CEV','English'), 
	('Darby Translation','DARBY','English'), 
	('Douay-Rheims 1899 American Edition','DRA','English'), 
	('Easy-to-Read Version','ERV','English'), 
	('English Standard Version','ESV','English'), 
	('English Standard Version Anglicised','ESVUK','English'), 
	('Expanded Bible','EXB','English'), 
	('1599 Geneva Bible','GNV','English'), 
	('GOD’S WORD Translation','GW','English'),
	('Good News Translation','GNT','English'), 
	('Holman Christian Standard Bible','HCSB','English'), 
	('J.B. Phillips New Testament','PHILLIPS','English'), 
	('Jubilee Bible 2000','JUB','English'), 
	('King James Version','KJV','English'), 
	('Authorized (King James) Version','AKJV','English'), 
	('Lexham English Bible','LEB','English'), 
	('Living Bible','TLB','English'), 
	('The Message','MSG','English'), 
	('Mounce Reverse-Interlinear New Testament','MOUNCE','English'), 
	('Names of God Bible','NOG','English'), 
	('New American Standard Bible','NASB','English'), 
	('New Century Version','NCV','English'), 
	('New English Translation','NET','English'), 
	("New International Reader's Version",'NIRV','English'), 
	('New International Version','NIV','English'), 
	('New International Version - UK','NIVUK','English'), 
	('New King James Version','NKJV','English'), 
	('New Life Version','NLV','English'), 
	('New Living Translation','NLT','English'), 
	('New Revised Standard Version','NRSV','English'), 
	('New Revised Standard Version, Anglicised','NRSVA','English'), 
	('New Revised Standard Version, Anglicised Catholic Edition','NRSVACE','English'), 
	('New Revised Standard Version Catholic Edition','NRSVCE','English'), 
	('Orthodox Jewish Bible','OJB','English'), 
	('Revised Standard Version','RSV','English'), 
	('Revised Standard Version Catholic Edition','RSVCE','English'), 
	('The Voice','VOICE','English'), 
	('World English Bible','WEB','English'), 
	('Worldwide English (New Testament)','WE','English'),
	('Wycliffe Bible','WYC','English'), 
	("Young's Literal Translation",'YLT','English'), 
	('La Biblia de las Américas','LBLA','Spanish'), 
	('Dios Habla Hoy','DHH','Spanish'), 
	('Jubilee Bible 2000 (Spanish)','JBS','Spanish'), 
	('Nueva Biblia Latinoamericana de Hoy','NBLH','Spanish'), 
	('Nueva Traducción Viviente','NTV','Spanish'), 
	('Nueva Versión Internacional (Castilian)','CST','Spanish'),
	('Nueva Versión Internacional','NVI','Spanish'), 
	('Palabra de Dios para Todos','PDT','Spanish'), 
	('La Palabra (España)','BLP','Spanish'), 
	('La Palabra (Hispanoamérica)','BLPH','Spanish'), 
	('Reina Valera Contemporánea','RVC','Spanish'), 
	('Reina-Valera 1960','RVR1960','Spanish'), 
	('Reina Valera 1977','RVR1977','Spanish'), 
	('Reina-Valera 1995','RVR1995','Spanish'), 
	('Reina-Valera Antigua','RVA','Spanish'), 
	('Traducción en lenguaje actual','TLA','Spanish'), 
	('Raamattu 1933/38','R1933','Finnish'), 
	('La Bible du Semeur','BDS','French'), 
	('Louis Segond','LSG','French'),
	('Nouvelle Edition de Genève – NEG1979','NEG1979','French'), 
	('Segond 21','SG21','French'), 
	('1550 Stephanus New Testament','TR1550','Greek'), 
	('1881 Westcott-Hort New Testament','WHNU','Greek'), 
	('1894 Scrivener New Testament','TR1894','Greek'), 
	('SBL Greek New Testament','SBLGNT','Greek'), 
	('Habrit Hakhadasha/Haderekh','HHH','Hebrew'), 
	('The Westminster Leningrad Codex','WLC','Hebrew'), 
	('Hindi Bible: Easy-to-Read Version','ERV-HI','Hindi'), 
	('Ang Pulong Sang Dios','HLGN','Hiligaynon'),
	('Knijga O Kristu','CRO','Croatian'), 
	('Haitian Creole Version','HCV','Haitian Creole'), 
	('Hungarian Károli','KAR','Hungarian'), 
	('Hungarian Bible: Easy-to-Read Version','ERV-HU','Hungarian'), 
	('Hungarian New Translation','NT-HU','Hungarian'), 
	('Hawai‘i Pidgin','HWP','Hawai‘i Pidgin'), 
	('Icelandic Bible','ICELAND','Icelandic'), 
	('La Bibbia della Gioia','BDG','Italian'), 
	('Conferenza Episcopale Italiana','CEI','Italian'), 
	('La Nuova Diodati','LND','Italian'), 
	('Nuova Riveduta 1994','NR1994','Italian'),
	('Nuova Riveduta 2006','NR2006','Italian'), 
	('Jacalteco, Oriental','JAC','Jakaltek'), 
	('Kekchi','KEK','Kekchi'), 
	('Biblia Sacra Vulgata','VULGATE','Latin'), 
	('Maori Bible','MAORI','Maori'), 
	('Macedonian New Testament','MNT','Macedonian'), 
	('Marathi Bible: Easy-to-Read Version','ERV-MR','Marathi'), 
	('Mam, Central','MVC','Mam'), 
	('Mam de Todos Santos Chuchumatán','MVJ','Mam'), 
	('Reimer 2001','REIMER','Low German'), 
	('Nepali Bible: Easy-to-Read Version','ERV-NE','Nepali'),
	('Náhuatl de Guerrero','NGU','Nahuatl'), 
	('Het Boek','HTB','Dutch'), 
	('Det Norsk Bibelselskap 1930','DNB1930','Norwegian'), 
	('En Levende Bok','LB','Norwegian'), 
	('Oriya Bible: Easy-to-Read Version','ERV-OR','Oriya'), 
	('Punjabi Bible: Easy-to-Read Version','ERV-PA','Punjabi'), 
	('Nowe Przymierze','NP','Polish'), 
	('Słowo Życia','SZ-PL','Polish'), 
	('Ne Bibliaj Tik Nawat','NBTN','Pipil'), 
	('João Ferreira de Almeida Atualizada','AA','Portuguese'), 
	('Nova Versão Internacional','NVI-PT','Portuguese'),
	('O Livro','OL','Portuguese'), 
	('Portuguese New Testament: Easy-to-Read Version','VFL','Portuguese'), 
	('Mushuj Testamento Diospaj Shimi','MTDS','Quichua'), 
	('Quiché, Centro Occidental','QUT',"K'iche"), 
	('Cornilescu','RMNN','Romanian'), 
	('Nouă Traducere În Limba Română','NTLR','Romanian'), 
	('Russian New Testament: Easy-to-Read Version','ERV-RU','Russian'), 
	('Russian Synodal Version','RUSV','Russian'), 
	('Slovo Zhizny','SZ','Russian'), 
	('Nádej pre kazdého','NPK','Slovak'), 
	('Somali Bible','SOM','Somali'), 
	('Albanian Bible','ALB','Albanian'),
	('Serbian New Testament: Easy-to-Read Version','ERV-SR','Serbian'), 
	('Nya Levande Bibeln','SVL','Swedish'), 
	('Svenska 1917','SV1917','Swedish'), 
	('Svenska Folkbibeln','SFB','Swedish'), 
	('Neno: Bibilia Takatifu','SNT','Swahili'), 
	('Tamil Bible: Easy-to-Read Version','ERV-TA','Tamil'), 
	('Thai New Contemporary Bible','TNCV','Thai'), 
	('Thai New Testament: Easy-to-Read Version','ERV-TH','Thai'), 
	('Ang Salita ng Diyos','SND','Tagalog'), 
	('Nkwa Asem','NA-TWI','Twi'), 
	('Ukrainian Bible','UKR','Ukrainian'),
	('Ukrainian New Testament: Easy-to-Read Version','ERV-UK','Ukrainian'), 
	('Urdu Bible: Easy-to-Read Version','ERV-UR','Urdu'), 
	('Uspanteco','USP','Uspanteko'), 
	('1934 Vietnamese Bible','VIET','Vietnamese'), 
	('Bản Dịch 2011','BD2011','Vietnamese'), 
	('Vietnamese Bible: Easy-to-Read Version','BPT','Vietnamese'), 
	('Chinese Contemporary Bible','CCB','Chinese'), 
	('Chinese New Testament: Easy-to-Read Version','ERV-ZH','Chinese'), 
	('Chinese New Version (Traditional)','CNVT','Chinese'), 
	('Chinese Standard Bible (Simplified)','CSBS','Chinese'), 
	('Chinese Standard Bible (Traditional)','CSBT','Chinese'),
	('Chinese Union Version (Simplified)','CUVS','Chinese'), 
	('Chinese Union Version (Traditional)','CUV','Chinese'), 
	('Chinese Union Version Modern Punctuation (Simplified)','CUVMPS','Chinese'), 
	('Chinese Union Version Modern Punctuation (Traditional)','CUVMPT','Chinese'), 
	('JPS Tanakh','NJPS','English'),
	('New American Bible (Revised Edition)','NABRE','English');
	
CREATE TRIGGER update_translation_stats_timestamp BEFORE UPDATE
    ON translation_stats FOR EACH ROW EXECUTE PROCEDURE 
    update_timestamp_column();
