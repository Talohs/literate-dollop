import base64
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'date_created': self.date_created,
        }

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        now = datetime.utcnow()
        self.token_expiration = now - timedelta(seconds=1)
        db.session.commit()


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aura = db.Column(db.String(50), nullable=True)
    exilus = db.Column(db.String(50), nullable=True)
    mod1 = db.Column(db.String(50), nullable=True)
    mod2 = db.Column(db.String(50), nullable=True)
    mod3 = db.Column(db.String(50), nullable=True)
    mod4 = db.Column(db.String(50), nullable=True)
    mod5 = db.Column(db.String(50), nullable=True)
    mod6 = db.Column(db.String(50), nullable=True)
    mod7 = db.Column(db.String(50), nullable=True)
    mod8 = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'aura', 'exilus', 'mod1', 'mod2', 'mod3', 'mod4', 'mod5', 'mod6', 'mod7', 'mod8'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'aura': self.aura,
            'exilus': self.exilus,
            'mod1': self.mod1,
            'mod2': self.mod2,
            'mod3': self.mod3,
            'mod4': self.mod4,
            'mod5': self.mod5,
            'mod6': self.mod6,
            'mod7': self.mod7,
            'mod8': self.mod8,
        }    
    

class Mod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    polarity = db.Column(db.String(20), nullable=False)
    drain = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    rarity = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    effect = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<Name {self.name}| id {self.id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'polarity': self.polarity,
            'drain': self.drain,
            'rank': self.rank,
            'rarity': self.rarity,
            'type': self.rarity
        }

class Warframe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    health = db.Column(db.Integer, nullable=False)
    shield = db.Column(db.Integer, nullable=True)
    armor = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.Integer, nullable=True)
    starting_energy = db.Column(db.Integer, nullable=True)
    sprint_speed = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<Name {self.name}| id {self.id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'health': self.health,
            'shield': self.shield,
            'armor': self.armor,
            'energy': self.energy,
            'starting energy': self.starting_energy,
            'sprint speed': self.sprint_speed,
        }

class WeaponPrimary():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    fire_rate = db.Column(db.Integer, nullable=False)
    impact = db.Column(db.Integer, nullable=True)
    puncture = db.Column(db.Integer, nullable=True)
    slash = db.Column(db.Integer, nullable=True)
    cold = db.Column(db.Integer, nullable=True)
    electricity = db.Column(db.Integer, nullable=True)
    heat = db.Column(db.Integer, nullable=True)
    toxin = db.Column(db.Integer, nullable=True)
    blast = db.Column(db.Integer, nullable=True)
    corrosive = db.Column(db.Integer, nullable=True)
    gas = db.Column(db.Integer, nullable=True)
    magnetic = db.Column(db.Integer, nullable=True)
    radiation = db.Column(db.Integer, nullable=True)
    viral = db.Column(db.Integer, nullable=True)
    critical_chance = db.Column(db.Float, nullable=False)
    critical_multi = db.Column(db.Float, nullable=False)
    multishot = db.Column(db.Float, nullable=False)
    punch_through = db.Column(db.Float, nullable=False)
    range = db.Column(db.Float, nullable=False)
    status_chance = db.Column(db.Float, nullable=False)
    impact_aoe = db.Column(db.Integer, nullable=True)
    puncture_aoe = db.Column(db.Integer, nullable=True)
    slash_aoe = db.Column(db.Integer, nullable=True)
    cold_aoe = db.Column(db.Integer, nullable=True)
    electricity_aoe = db.Column(db.Integer, nullable=True)
    heat_aoe = db.Column(db.Integer, nullable=True)
    toxin_aoe = db.Column(db.Integer, nullable=True)
    blast_aoe = db.Column(db.Integer, nullable=True)
    corrosive_aoe = db.Column(db.Integer, nullable=True)
    gas_aoe = db.Column(db.Integer, nullable=True)
    magnetic_aoe = db.Column(db.Integer, nullable=True)
    radiation_aoe = db.Column(db.Integer, nullable=True)
    viral_aoe = db.Column(db.Integer, nullable=True)
    dmg_falloff = db.Column(db.Float, nullable=True)
    range_aoe = db.Column(db.Float, nullable=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<Name {self.name}| id {self.id}>"

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'fire rate': self.fire_rate,
            'impact': self.impact,
            'puncture': self.puncture,
            'slash': self.slash,
            'cold': self.cold,
            'electricity': self.electricity,
            'heat': self.heat,
            'toxin': self.toxin,
            'blast': self.blast,
            'corrosive': self.corrosive,
            'gas': self.gas,
            'magnetic': self.magnetic,
            'radiation': self.radiation,
            'viral': self.viral,
            'critical chance': self.critical_chance,
            'critical multi': self.critical_multi,
            'multishot': self.multishot,
            'punchthrough': self.punch_through,
            'range': self.range,
            'status chance': self.status_chance,
            'impact aoe': self.impact_aoe,
            'puncture aoe': self.puncture_aoe,
            'slash aoe': self.slash_aoe,
            'cold aoe': self.cold_aoe,
            'electricity aoe': self.electricity_aoe,
            'heat aoe': self.heat_aoe,
            'toxin aoe': self.toxin_aoe,
            'blast aoe': self.blast_aoe,
            'corrosive aoe': self.corrosive_aoe,
            'gas aoe': self.gas_aoe,
            'magnetic aoe': self.magnetic_aoe,
            'radiation aoe': self.radiation_aoe,
            'viral aoe': self.viral_aoe,
            'damage falloff': self.dmg_falloff,
            'range aoe': self.range_aoe,
        }