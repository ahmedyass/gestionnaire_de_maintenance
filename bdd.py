import random
import re
from app import bcrypt
from app.models     import db, User, Ressource, Localisation, Ressource, Anomalie

if __name__ == '__main__':
    
    db.create_all()
    
    Admin = User('admin@email.fr', bcrypt.generate_password_hash('admin', 5), 'admin', 'admin', 'admin')
    db.session.add(Admin)
    db.session.commit()
    
    donnees = [
        {
            'nom': 'Clothilde',
            'prenom': 'Nadine',
            'fonction': 'informatique',
            'ressource': 'PC ',
            'localisation': ['Salle Informatique'],
            'range': [2, 3],
            'occu': 18
        },
        {
            'nom': 'Alix',
            'prenom': 'Natacha',
            'fonction': 'informatique',
            'ressource': 'Serveur ',
            'localisation': ['Salle Informatique'],
            'range': [2, 3],
            'occu': 1
        },
        {
            'nom': 'Pascal',
            'prenom': 'Alberte',
            'fonction': 'informatique',
            'ressource': 'Logiciel ',
            'localisation': ['Salle Informatique'],
            'range': [2, 3],
            'occu': 6
        },
        {
            'nom': 'Thibaut',
            'prenom': 'Rachel',
            'fonction': 'réseau',
            'ressource': 'Modem ',
            'localisation': [''],
            'range': [0, 1, 2, 3],
            'occu': 1
        },
        {
            'nom': 'Gwenaëlle',
            'prenom': 'Yohan',
            'fonction': 'réseau',
            'ressource': 'Point d\'accès ',
            'localisation': ['Couloire'],
            'range': [0, 1, 2, 3],
            'occu': 4
        },
        {
            'nom': 'Lorette',
            'prenom': 'Joceline',
            'fonction': 'réseau',
            'ressource': 'Téléphone ',
            'localisation': [''],
            'range': [0, 1, 2, 3],
            'occu': 4
        },
        {
            'nom': 'Cerise',
            'prenom': 'Killian',
            'fonction': 'electricité',
            'ressource': 'Lampe ',
            'localisation': ['Salle Informatique',  'Salle', 'Couloire'],
            'range': [0, 1, 2, 3],
            'occu': 10
        },
        {
            'nom': 'Madeline',
            'prenom': 'Jacinthe',
            'fonction': 'electricité',
            'ressource': 'Imprimante ',
            'localisation': [''],
            'range': [0, 1, 2, 3],
            'occu': 2
        },
        {
            'nom': 'Alcide',
            'prenom': 'Romane',
            'fonction': 'plomberie',
            'ressource': 'Chaufage ',
            'localisation': ['Salle Informatique',  'Salle', 'Couloire'],
            'range': [0, 1, 2, 3],
            'occu': 4
        },
        {
            'nom': 'Jean-François',
            'prenom': 'Romane',
            'fonction': 'plomberie',
            'ressource': 'Robinet ',
            'localisation': ['Toilette'],
            'range': [0, 1, 2, 3],
            'occu': 2
        }
    ]

    """
    Ajouter des localisations à la base de données
    """
    id_l = 1
    loc_dict = {}

    for i in range(4):
        loc_dict['Etage {}'.format(i)] = id_l
        id_l += 1
        localisation = Localisation('Etage {}'.format(i))
        db.session.add(localisation)
        db.session.commit()

    for i in range(4):
        for j in range(1, 11) :
            loc_dict['Etage {} Salle {}'.format(i,j)] = id_l
            id_l += 1
            localisation = Localisation('Etage {} Salle {}'.format(i,j))
            db.session.add(localisation)
            db.session.commit()

    for i in [2, 3]:
        for j in range(1, 5):
            loc_dict['Etage {} Salle Informatique {}'.format(i,j)] = id_l
            id_l += 1
            localisation = Localisation('Etage {} Salle Informatique {}'.format(i,j))
            db.session.add(localisation)
            db.session.commit()

    for i in range(4):
        for j in range(1, 5) :
            loc_dict['Etage {} Couloire {}'.format(i,j)] = id_l
            id_l += 1
            localisation = Localisation('Etage {} Couloire {}'.format(i,j))
            db.session.add(localisation)
            db.session.commit()

    for i in range(4):
        for j in range(1, 5) :
            loc_dict['Etage {} Toilette {}'.format(i,j)] = id_l
            id_l += 1
            localisation = Localisation('Etage {} Toilette {}'.format(i,j))
            db.session.add(localisation)
            db.session.commit()

    max_ = {'Salle Informatique': 5,  'Salle': 11, 'Couloire': 5, 'Toilette': 5}

    id_r = 2
    for donnee in donnees:
        """
        Ajouter des responsables
        """
        prenom_pass = re.sub('[^a-zA-Z0-9 \n\.]', '', donnee['prenom'])
        nom_pass = re.sub('[^a-zA-Z0-9 \n\.]', '', donnee['nom'])
        
        password = 'pass' + nom_pass + prenom_pass[:3]
        email = 'email.' + nom_pass + prenom_pass[:3] + '@email.fr'

        user = User(email, bcrypt.generate_password_hash(password, 5), donnee['nom'], donnee['prenom'], donnee['fonction'])
        db.session.add(user)
        db.session.commit()
        
        id_res = 0
        for loca in donnee['localisation']:
            if loca == '':
                for i in donnee['range']:
                    for k in range(donnee['occu']):
                        """
                        Ajouter des ressources
                        """
                        localisation = 'Etage ' + str(i)
                        localisation_id = loc_dict[localisation]
                        description = donnee['ressource'] + str(k) + ' ' + localisation
                        ressource = Ressource(donnee['ressource'] + str(k), description, id_r, localisation_id)
                        db.session.add(ressource)
                        db.session.commit()
            else :
                if loca == 'Salle Informatique':
                    range_ = [2, 3]
                else:
                    range_ = donnee['range']
                for i in range_:
                    for j in range(1, max_[loca]):
                        for k in range(donnee['occu']):
                            """
                            Ajouter des ressources
                            """
                            localisation = 'Etage '+ str(i) + ' ' + loca + ' ' + str(j)
                            localisation_id = loc_dict[localisation]
                            description = donnee['ressource'] + str(k) + ' ' + localisation
                            ressource = Ressource(donnee['ressource'] + str(k), description, id_r, localisation_id)
                            db.session.add(ressource)
                            db.session.commit()
        id_r +=1
ressources = Ressource.query.all()
for res in ressources:
    for l in range(random.randint(0, 11)):
        """
        Ajouter des anomalies
        """
        anomalie = Anomalie(res.id, 'Problème ' + str(l) + ' ' + res.description)
        db.session.add(anomalie)
        db.session.commit()