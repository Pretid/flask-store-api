import os #access environment of os (variable)
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from datetime import timedelta
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') #first in prod second in dev
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.confgi['PROPAGATE_EXCEPTION'] =True 
app.secret_key = "123456"
api = Api(app)

jwt = JWT(app, authenticate,identity) #/auth
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    #app.run(port=8080)
    from db import db
    db.init_app(app)
    app.run(port=8080, debug=True)