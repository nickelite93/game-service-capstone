import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from flask_migrate import Migrate

from models import setup_db, Character, Game, db
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Acces-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/games', methods=['GET'])
  @requires_auth('get:games')
  def get_games(jwt):
    games = Game.query.all()

    list = [game.full() for game in games]

    return jsonify({
      "success": True,
      "games": list
    })

  @app.route('/characters', methods=['GET'])
  @requires_auth('get:characters')
  def get_characters(jwt):
    characters = Character.query.all()

    list = [character.full() for character in characters]

    return jsonify({
      "success": True,
      "characters": list
    })

  @app.route("/games/create", methods=["POST"])
  @requires_auth('post:games')
  def post_game(jwt):
    body = request.get_json()
    try:
      title = body.get('title')
      rating = body.get('rating')
      completed = body.get('completed')

      game = Game(title=title, rating=rating, completed=completed)
      game.insert()
      return jsonify({
        'success': True,
        'game_id': game.id,
        'game_title': game.title
      })
    except:
      abort(400)

  @app.route("/games/<int:game_id>", methods=['DELETE'])
  @requires_auth("delete:games")
  def delete_game(jwt, game_id):
    print("2")
    game = Game.query.filter_by(id=game_id).first()
    print("1")

    if game is None:
      abort(404)

    game.delete()
    print("3")

    return jsonify({
      'success': True,
      'game_id': game.id,
      'title': game.title
    })

  @app.route("/characters/create", methods=["POST"])
  @requires_auth("post:characters")
  def post_character(jwt):
    body = request.get_json()
    try:
      name = body.get('name')
      fighting = body.get('fighting')
      intelligence = body.get('intelligence')
      good = body.get('good')
      new_game_id = body.get('game_id')
      print("1")

      character = Character(name=name, fighting=fighting, intelligence=intelligence, good=good, game_id=new_game_id)
      print("2")
      character.insert()
      print("3")
      return jsonify({
        'success': True,
        'character_id': character.id,
        'character_name': character.name
      })
    except:
      abort(400)

  @app.route("/characters/<int:character_id>", methods=['DELETE'])
  @requires_auth('delete:characters')
  def delete_character(jwt, character_id):
    character =  Character.query.filter_by(id=character_id).first()

    if character is None:
      abort(404)
    character.delete()

    return jsonify({
      'success': True,
      'character_id': character.id
    })

  @app.route("/games/<int:game_id>", methods=['PATCH'])
  @requires_auth('patch:games')
  def patch_game(jwt, game_id):
    body = request.get_json()

    new_rating= body.get("new_rating")
    completed = body.get("completed")

    game = Game.query.filter(Game.id==game_id).one_or_none()

    if game is None:
      abort(404)

    game.rating = new_rating
    game.completed = completed
    game.update()

    return jsonify({
      "success": True,
      "title": game.title
    })
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found"
    }), 404

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      'success': False,
      'error': 401,
      'message': 'unauthorized'
    }), 401

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": 'bad request'
    }), 400

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        'error': error.error,
        'status_code': error.status_code
    }), 401

  return app

app = create_app()
# db.create_all()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
    

# Test comment line
# 


