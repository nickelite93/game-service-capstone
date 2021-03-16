import os
import unittest
import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Character, Game

admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikx2WDU2Ni0tS0I3cl9PWlRJSkdJRCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlja3MuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NTYzNjUzNzcwNTIzNTQ4NTQ1IiwiYXVkIjpbImdhbWVzLWxpYnJhcnkiLCJodHRwczovL2ZzbmQtbmlja3MuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxNTkxNTk5NiwiZXhwIjoxNjE2MDAyMzk2LCJhenAiOiJ6VHlwTXR1VVV1aEdNVlpmaEZ1ZUJPazNjUnBxR1I0eiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2hhcmFjdGVycyIsImRlbGV0ZTpnYW1lcyIsImdldDpjaGFyYWN0ZXJzIiwiZ2V0OmdhbWVzIiwicGF0Y2g6Z2FtZXMiLCJwb3N0OmNoYXJhY3RlcnMiLCJwb3N0OmdhbWVzIl19.AmJMbEa87YD8UJJ--xUgnPAtLkZ5Y50R3oN33_IYne2oLjTk0rw1nfUUfCXU3gnRBG5q2137fGGMpSG8KPHBgC4Olmsz2XV3Iti9VX4c8VPDbQImFUFqp2wl9eRz7NE_AE3UQG58xXPMS-H5myrq-OKSgdqiLfYWrCNf8WcXOVTj5aely2vYTbsX-rH8sNUZWwajEHxtDR-dSZzNm0hrLIUIqzLxSy6Wmdt-rO-wUnL8OcmbHn-bSmWwY5ja1Hf74aptJWxYOfQHhNgIeCpxM0OpY4rLlQSXSWyWD0aat_MeoqnUT5TImVwmKeCkJ7mRvKmIX92XKPGJ4o_-Uml1Cw'
user_token =  'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikx2WDU2Ni0tS0I3cl9PWlRJSkdJRCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlja3MuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMGVkOTBhNzRlMDY4MDA2OTUzODIzMyIsImF1ZCI6ImdhbWVzLWxpYnJhcnkiLCJpYXQiOjE2MTU5MTgxODAsImV4cCI6MTYxNjAwNDU4MCwiYXpwIjoielR5cE10dVVVdWhHTVZaZmhGdWVCT2szY1JwcUdSNHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjaGFyYWN0ZXJzIiwiZ2V0OmdhbWVzIl19.NO5AqxElqkr2BYMkLmHXxg7pP4c9XuOCn_MxamwmBpmYxedw2rfFy8OwYiW5Ppd27kjbPTXFyGvwKdPz7o7gk-pjcGHcqOSn-6673s9K-NSxM5eDhDeZWMeSEVLhZA456bHi4FDY2Cf3hRzFlARmFQwXVQ5ghS0m0wE6BmJgs74KruD9sbhc1AcRMrM0jd1YH2DYyidzoly3YCwCZU7S0tzmeRVLG2oOcRXCUN420cp6X-BWXdV6shmpdVEpUh2yqcTgpoY_P1TyKHtZfDzocL5KjtCO7ZFpL12okuN2GtpCsonsWBy_9Cn6oJWDPs137IRflqbYBkWYvaIt3RkC2w'

class GameCharacterCatalogueTestCase(unittest.TestCase):

        def setUp(self):
            self.app = create_app()
            self.client = self.app.test_client
            self.database_name = "game_test"
            self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
            setup_db(self.app, self.database_path)

            self.new_game = {
                'title': 'This is a test game',
                'rating': 8,
                'completed': False
            }

            self.new_character = {
                'name': 'This is a test character',
                'fighting': 7,
                'intelligence': 5,
                'good': False,
                'game_id': 6
            }

            self.game_patch = {
                "new_rating": 9,
                "completed": True
            }

        # binds the app to the current context
            with self.app.app_context():
                self.db = SQLAlchemy()
                self.db.init_app(self.app)
                # create all tables
                self.db.create_all()


        # def tearDown(self):
        #     pass


        def test_get_games(self):
            res = self.client().get('/games', headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['games'])


        def test_get_characters(self):
            res = self.client().get('/characters', headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['characters'])

        def test_post_game(self):
            res = self.client().post('/games/create', json=self.new_game, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['game_id'])

        def test_patch_game(self):
            game = Game.query.filter(Game.title=='This is a test game').first()
            id = game.id

            res = self.client().patch('/games/' + str(id), json=self.game_patch, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['title'], game.title)

        def test_post_character(self):
            res = self.client().post("/characters/create", json=self.new_character, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['character_id'])


        def test_delete_game(self):
            game = Game.query.filter(Game.title=='This is a test game').first()
            id = game.id
            res = self.client().delete('/games/' + str(id), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['game_id'])

        def test_delete_character(self):
            character = Character.query.filter(Character.name=='This is a test character').first()
            id = character.id
            res = self.client().delete('/characters/' + str(id), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['character_id'])

        def test_fail_to_create_game(self):
            bad_game = {"title":"bad title", "rating": "NaN", "completed": False}
            res = self.client().post('/games/create', json=bad_game, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'bad request')

        def test_no_auth_create_game(self):
            bad_game = {"title":"bad title", "rating": "NaN", "completed": False}
            res = self.client().post('/games/create', json=bad_game, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)

        def test_delete_non_existent_game(self):
            res = self.client().delete('/games/10000000000', headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['message'], 'resource not found')

        def test_fail_to_create_character(self):
            bad_character = {"name":"bad name", "fighting": "NaN", "intelligence": 7, "good": False, "game_id": 2}
            res = self.client().post('/characters/create', json=bad_character, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'bad request')
        
        def test_no_auth_create_character(self):
            bad_character = {"name":"bad name", "fighting": 7, "intelligence": 7, "good": False, "game_id": 2}
            res = self.client().post('/characters/create', json=bad_character, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)

        def test_delete_non_existent_character(self):
            res = self.client().delete('/characters/10000000000', headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['message'], 'resource not found')

        def test_patch_nonexistent_game(self):
            res = self.client().patch('/games/10000000', json=self.game_patch, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + admin_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['message'], 'resource not found')

        def test_create_game_as_user(self):
            bad_character = {"name":"bad name", "fighting": 7, "intelligence": 7, "good": False, "game_id": 2}
            res = self.client().post('/characters/create', json=bad_character, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + user_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)



if __name__ == "__main__":
    unittest.main()


        

        


