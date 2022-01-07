from app                import app, db
from itsdangerous       import TimedJSONWebSignatureSerializer as Serial

from flask_login        import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id          = db.Column(db.Integer,     primary_key = True)
    email       = db.Column(db.String(100), nullable = False, unique = True)
    password    = db.Column(db.String(255), nullable = False)
    nom         = db.Column(db.String(100), nullable = False)
    prenom      = db.Column(db.String(100), nullable = False)
    fonction    = db.Column(db.String(100), nullable = False)
    ressource   = db.relationship("Ressource")

    def __init__(self, email, password, nom, prenom, fonction):
        self.email      = email 
        self.password   = password
        self.nom        = nom
        self.prenom     = prenom
        self.fonction   = fonction

    def get_reini_token(self, expiration=86400):
        s = Serial(app.config['SECRET_KEY'], expiration)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verifier_reini_token(token):
        s = Serial(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_fonct(self):
        return self.fonction

class Localisation(db.Model):
    __tablename__ = 'localisation'

    id          = db.Column(db.Integer,     primary_key = True)
    nom         = db.Column(db.String(100), nullable = False)
    ressource   = db.relationship("Ressource")
    def __init__(self, nom):
        self.nom = nom

class Ressource(db.Model):
    __tablename__ = 'ressource'

    id              = db.Column(db.Integer,     primary_key = True)
    nom             = db.Column(db.String(100), nullable = False)
    description     = db.Column(db.String(100), nullable = False)
    
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.id'))
    localisation    = db.relationship("Localisation", back_populates="ressource")
    
    responsable_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    responsable     = db.relationship("User", back_populates="ressource")

    anomalie        = db.relationship("Anomalie")
    
    def __init__(self, nom, description, responsable_id, localisation_id):
        self.nom                = nom
        self.description        = description
        self.responsable_id     = responsable_id
        self.localisation_id    = localisation_id

class Anomalie(db.Model):
    __tablename__ = 'anomalie'

    id              = db.Column(db.Integer,     primary_key = True)
    ressource       = db.Column(db.String(100), nullable = False)
    description     = db.Column(db.String(100), nullable = False)

    ressource_id  = db.Column(db.Integer, db.ForeignKey('ressource.id'))
    ressource     = db.relationship("Ressource", back_populates="anomalie")
    
    def __init__(self, ressource_id, description):
        self.ressource_id   = ressource_id
        self.description    = description