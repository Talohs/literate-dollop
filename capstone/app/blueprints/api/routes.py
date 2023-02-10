from flask import request
from . import api
from .auth import basic_auth, token_auth
from app.models import User, Mod, Build

@api.route('/token')
@basic_auth.login_required
def index():
    user = basic_auth.current_user()
    token = user.get_token()
    return {'token': token, 'token_expiration': user.token_expiration}

@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return {'error': f"{field} must be in request body"}, 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter((User.username == username)|(User.email == email)).all()
    if existing_user:
        return {'error': 'User with this username and/or email already exists'}, 400

    new_user = User(username=username, email=email, password=password)
    return new_user.to_dict(), 201

@api.route('/mod', methods=['GET'])
def export_mods():
    mods = Mod.query.all()
    return [m.to_dict() for m in mods]

@api.route('/build', methods=['Post'])
def create_build():
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    data = request.json
    for field in ['aura', 'exilus', 'mod1', 'mod2', 'mod3', 'mod4', 'mod5', 'mod6', 'mod7', 'mod8']:
        if field not in data:
            return {'error': f"{field} must be in request body"}, 400

        aura = data.get('aura')
        exilus = data.get('exilus')
        mod1 = data.get('mod1')
        mod2 = data.get('mod2')
        mod3 = data.get('mod3')
        mod4 = data.get('mod4')
        mod5 = data.get('mod5')
        mod6 = data.get('mod6')
        mod7 = data.get('mod7')
        mod8 = data.get('mod8')

        user = token_auth.current_user()

        new_build = Build(aura=aura, exilus=exilus, mod1=mod1, mod2=mod2, mod3=mod3,mod4=mod4, mod5=mod5, mod6=mod6,mod7=mod7, mod8=mod8, user_id=user.id )
        return new_build.to_dict(), 201