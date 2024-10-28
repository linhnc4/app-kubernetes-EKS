import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

database_path = os.getenv('DATABASE_URI')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Paint
a persistent paint entity, extends the base SQLAlchemy Model
'''
class Paint(db.Model):
    __tablename__ = 'paint'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    # the required datatype is [{'binder': string, 'pigment':string, 'extender':string, 'solvent':string, 'additives':string}]
    recipe = Column(String(500), unique=True)

    '''
    short()
        short form representation of the Paint model
    '''
    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [{'binder': r['binder'], 'pigment': r['pigment'], 'extender': r['extender'], 'solvent': r['solvent']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }
        
    '''
    long()
        long form representation of the Paint model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            paint = Paint(title=req_title, recipe=req_recipe)
            paint.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            paint = Paint(title=req_title, recipe=req_recipe)
            paint.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            paint = Paint.query.filter(Paint.id == id).one_or_none()
            paint.title = 'Sơn bóng'
            paint.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
