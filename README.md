**Motivation for project**

This API provides a catalogue system for game collections. It allows a user to manage records of games and the characters that are in them. 

**Project Dependencies**

The list of project dependencies is included in the requirements.txt file. 

**PostgresSQL**

This application is configured to run with PostgresSQL as the database. The following section of the application located in models.py file will need to be updated:

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://{username}:{password}@{domainOrLocation}:{port}/{dbName}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

**Auth0**

This applicaiton is configured to use Auth0 for managing permissions. The following section of the auth.py file will need to be conifugred to work with your Auth0 account:

AUTH0_DOMAIN = '{yourdomain}.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = '{yourAPITitle}'

Information on how to configure this for your application can be found here: https://auth0.com

**Roles & Permissions**

There are two Roles configured for this app with the following permissions. 

1. User:
    - get:games
    - get:characters

2. Admin:
    - get:games
    - get:characters
    - post:games
    - post:characters
    - delete:games
    - delete:characters
    - patch:games


**Endpoints API **

GET '/games'
GET '/characters'
POST '/games/create'
POST '/characters/create'
DELETE '/games'
DELETE '/characters'
PATCH '/games'


GET '/games'
- Retrieves a list of all the Games in the database. Each game has all of its attributes included. 
- Request Arguments: None
- Returns: An array of objects, each object has several key value pairs. 
{"games": [
        {
            "completed": true,
            "genres": [
                "Horror"
            ],
            "id": 2,
            "rating": 9,
            "title": "Resident Evil"
        },
        {
            "completed": true,
            "genres": [
                "Horror"
            ],
            "id": 3,
            "rating": 9,
            "title": "Luigis Mansion"
        }
    ],
    "success": true}


GET '/characters'
- Retrieves a list of all the Characters in the database. Each character has all of its attributes included as well as the id of the game the character is from. 
- Request Arguments: None
- Returns: An array of objects, each object has several key value pairs. 
{
    "characters": [
        {
            "fighting": 9,
            "game_id": 2,
            "good": true,
            "id": 1,
            "intelligence": 7,
            "name": "Leon"
        },
        {
            "fighting": 7,
            "game_id": 3,
            "good": false,
            "id": 6,
            "intelligence": 4,
            "name": "Wario"
        }
    ],
    "success": true
}

POST '/games/create'
- Adds a new game to the database. 
- Request Arguments: Json object with keys for all required fields. Completed is default set to false if not inculded, a game can have multiple genres by adding to the 'genres' array. 
{
"title": "Luigis Mansion", 
"genres": ["Horror", "Adventure"], 
"rating": 8, 
"completed": false
}
- Returns: Status, title and the ID of the new game. 
{
    "game_id": 5,
    "game_title": "Luigis Mansion",
    "success": true
}


POST 'characters/create'
- Adds a new character to the database.
- Request Arguments: Json object with keys for all required fields. 'game_id' refers to the id of the game entry that the character belongs to. 
{
    "name": "Wario",
    "fighting": 7,
    "intelligence": 4,
    "good": false,
    "game_id": 3
}
- Returns: Status and ID of the new character.
{
    "character_id": 8,
    "character_name": "Wario",
    "success": true
}


DELETE '/games/{game_id}'
- Deletes a game from the database.
- Request Arguements: Game id
- Returns: Status, title and id of deleted game
{
    "game_id": 5,
    "title": "Snake",
    "success": true
}

DELETE '/characters/{character_id}'
- Deletes a character from the database.
- Request Arguements: Character id
- Returns: Status, name and id of deleted character
{
    "character_id": 5,
    "name": "Snake",
    "success": true
}

PATCH '/games/{game_id}'
- Updates the rating and completed status of a game in the database. 
- Request Arguments: Game id specified in the endpoint path, rating and completed status in the body. 
{
"new_rating": 9,
"completed": true
}
- Response Arguments: Status and game id. 
