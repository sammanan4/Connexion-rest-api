#!/home/sammanan4/Desktop/Assignment/env/bin/python3
from sqlalchemy.orm import scoped_session, sessionmaker
from connexion import NoContent
import connexion
import datetime
import logging

from models import engine, Person
from schema import PersonSchema

def provide_session(func, *args, **kwargs):
    def decorator(*args, **kwargs):
        session = scoped_session(sessionmaker(bind=engine))
        ret_val = func(session, *args, **kwargs)
        session.close()
        return ret_val
    return decorator


@provide_session
def get_persons(session, limit):
    persons = session.query(Person).limit(limit).all()
    return_list = []
    for p in persons:
        person_schema = PersonSchema()
        dump_data = person_schema.dump(p)
        return_list.append(dump_data)

    return return_list

@provide_session
def get_person(session, id):
    person = session.query(Person).filter(Person.id==id).first()
    if person:
        person_schema = PersonSchema()
        dump_data = person_schema.dump(person)
        return dump_data
    return ('Not found', 404)

@provide_session
def put_person(session, id, person):
    person_in_db = session.query(Person).filter(Person.id==id).first()
    
    if person_in_db:
        logging.info('Updating person %s..', id)
        person_schema = PersonSchema()
        person_schema.load(person, session=session, instance=person_in_db, partial=True)
    else:
        logging.info('Creating person %s..', id)
        person['date'] = datetime.datetime.utcnow()
        session.add(Person(id=id, **person))
    session.commit()
    return NoContent, (200 if person_in_db else 201)

@provide_session
def delete_person(session, id):
    person = session.query(Person).filter(Person.id==id).first()
    if person:
        logging.info('Deleting person %s..', id)
        session.delete(person)
        session.commit()
        return NoContent, 204
    return ('Not found', 404)


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, options={'swagger_url': '/docs'})
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':

    # run our standalone gevent server
    app.run(port=8080, server='gevent')