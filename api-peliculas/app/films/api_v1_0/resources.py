from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import FilmSchema, ActorSchema, CinemaSchema
from ..models import Film, Actor, Cinema

films_v1_0_bp = Blueprint('films_v1_0_bp', __name__)

film_schema = FilmSchema()
actor_schema = ActorSchema()
cinema_schema = CinemaSchema()

api = Api(films_v1_0_bp)
class FilmListResource(Resource):
    def get(self):
        films = Film.get_all()
        result = film_schema.dump(films, many=True)
        return result

    def post(self):
        data = request.get_json()
        film_dict = film_schema.load(data)
        film = Film(title=film_dict['title'],
                    length=film_dict['length'],
                    year=film_dict['year'],
                    director=film_dict['director']
        )
        for actor_data in film_dict['actors']:
            actor_name = actor_data['name']
            existing_actor = Actor.query.filter_by(name=actor_name).first()
            if existing_actor:
            # El actor ya existe, usa el actor existente
                film.actors.append(existing_actor)
            else:
            # El actor no existe, créalo y agrégalo a la película
                new_actor = Actor(name=actor_name)
                film.actors.append(new_actor)
        for cinema_data in film_dict['cinemas']:
            cinema_name = cinema_data['name']
            existing_cinema = Cinema.query.filter_by(name=cinema_name).first()
            if existing_cinema:
            # El cine ya existe, usa el cine existente
                film.cinemas.append(existing_cinema)
            else:
            # El cine no existe, créalo y agrégalo a la película
                new_cinema = Cinema(name=cinema_name)
                film.cinemas.append(new_cinema)
        film.save()
        resp = film_schema.dump(film)
        return resp, 201
    
    '''
    def post(self):
        data = request.get_json()
        film_dict = film_schema.load(data)
        film = Film(title=film_dict['title'],
                    length=film_dict['length'],
                    year=film_dict['year'],
                    director=film_dict['director']
        )
        for actor in film_dict['actors']:
            film.actors.append(Actor(actor['name']))
        for cinema in film_dict['cinemas']:
            film.cinemas.append(Cinema(cinema['name']))
        film.save()
        resp = film_schema.dump(film)
        return resp, 201
'''

class FilmResource(Resource):
    def get(self, film_id):
        film = Film.get_by_id(film_id)
        if not film:
            return {"message": f"No se encontró la película con ID {film_id}."}, 404
        resp = film_schema.dump(film)
        return resp

class ActorResource(Resource):
    def get(self, actor_name):
        actor = Actor.get_by_name(actor_name)
        if not actor:
            return {"message": f"No se encontro el actor {actor_name}."}, 404
        films = Film.query.filter(Film.actors.contains(actor)).all()
        #films = Film.query.filter(Film.actors.any(Actor.name == actor_name)).all()
        result = film_schema.dump(films, many=True)
        return result
    
class CinemaResource(Resource):
    def get(self, cinema_name):
        cinema = Cinema.get_by_name(cinema_name)
        if not cinema:
            return {"message": f"No existe el cine {cinema_name}."}, 404
        films = Film.query.filter(Film.cinemas.contains(cinema)).all()
        #films = Film.simple_filter(cinemas=[cinema])
        #films = Film.query.filter(Film.cinemas.any(Cinema.name == cinema_name)).all()
        result = film_schema.dump(films, many=True)
        return result

api.add_resource(FilmListResource, '/api/v1.0/films/', endpoint='film_list_resource')
api.add_resource(FilmResource, '/api/v1.0/films/<int:film_id>', endpoint='film_resource')
api.add_resource(ActorResource, '/api/v1.0/actors/<actor_name>', endpoint='actor_resource')
api.add_resource(CinemaResource, '/api/v1.0/cinemas/<cinema_name>', endpoint='cinema_resource')