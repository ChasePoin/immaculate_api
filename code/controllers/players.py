from . import api
from flask import request, jsonify, current_app
from code.models.models import Player, PlayerRequest


# parameters:
# rating
# player_count
# team
# pos
# name
@api.route("/api/players", methods=["GET"])
def get_players() -> list[Player]:
    """
    Takes various parameters and returns players fitting those parameters. No parameters are required, returns all players by default.
    ---
    tags:
      - players
    parameters:
      - name: rating
        in: query
        type: integer
        required: false
      - name: count
        in: query
        type: integer
        required: false
      - name: team
        in: query
        type: string
        required: false
      - name: pos
        in: query
        type: string
        required: false
      - name: name
        in: query
        type: string
        required: false
    responses:
      200:
        description: A list of players
        examples:
          application/json: [
            {
              "_id": {"$oid": "69b49328e125138bb1208fe8"},
              "name": "Leo Carlsson",
              "pos": "C",
              "rating": 70,
              "img": "https://assets.nhle.com/mugs/nhl/20252026/ANA/8484153.png",
              "team": "ANA"
            }
          ]
      404:
        description: No players found
      500:
        description: Error retrieving players
    """
    data = request.args.to_dict()

    try:
        # no params -> all players
        if not data:
            response = current_app.player_service.get_all_players()
            if not response: return jsonify({"info": "no players found"}), 404
            return jsonify(response), 200

        # should implicitly convert between json and class
        player_request = PlayerRequest(**data)

        response = current_app.player_service.get_players(player_request)
        return jsonify(response), 200
    
    except Exception as ex:
        current_app.logger.error(f"get_players() - Issue retrieving players - {ex}")
        return jsonify({"error": f"error getting players"}), 500
    
# creates a player
# requires name, pos, img, team, rating
@api.route("/api/players/create", methods=["POST"])
def create_player():
    """
    Creates a player with the given parameters.
    ---
    tags:
      - players
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [name, pos, img, rating, team]
          properties:
            name:
              type: string
            pos:
              type: string
            img:
              type: string
            rating:
              type: integer
            team:
              type: string
    responses:
      200:
        description: Player successfully created
      400:
        description: Missing a required field
      500:
        description: Issue during player creation
    """
    # name: str, pos: str, rating: int, img: str
    try:
        data = request.get_json()
        
        player = Player(**data)

        if not player.name or not player.pos or not player.img or not int(player.rating) or not player.team:
            return jsonify({"error": f"missing a required field in request"}), 400

        id = current_app.player_service.create_player(
            player=player
        )

        return jsonify({"info": f"{player.name} successfully created with id {id}"}), 200
    
    except Exception as ex:
        current_app.logger.error(f"create_player() - Issue Inserting {player.name} into players database - {ex}")
        return jsonify({"error": f"issue during player creation"}), 500

# deletes player
# requires name, pos, team 
@api.route("/api/players/delete", methods=["DELETE"])
def delete_player():
    """
    Deletes a player given a name, pos, and team.
    ---
    tags:
      - players
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [name, pos, team]
          properties:
            name:
              type: string
            pos:
              type: string
            team:
              type: string
    responses:
      200:
        description: Player successfully deleted (or not found)
      400:
        description: Missing a required field
      500:
        description: Issue during player deletion
    """
    try:
        data = request.get_json()
        player = Player(**data)

        if not player.name or not player.pos or not player.team:
            return jsonify({"error": f"missing a required field in request"}), 400

        res = current_app.player_service.delete_player(
            player=player
        )

        if res == 0:
            return jsonify({"info": f"{player.name} was not found - deleted {res} players"}), 200

        return jsonify({"info": f"{player.name} successfully deleted {res} player(s)"}), 200
    
    except Exception as ex:
        current_app.logger.error(f"delete_player_entry() - Issue during player {player.name} deletion process - {ex}")
        return jsonify({"error": f"issue during player deletion"}), 500

# updates player
# requires name, pos, team, rating, img
# will probably update later, I don't really like this but I don't see us using it much currently, should probably make optional params
@api.route("/api/players/update", methods=["POST"])
def update_player():
    """
    Updates a player given a name, pos, team, rating, or img.
    (WIP)
    ---
    tags:
      - players
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [name, pos, team, rating, img]
          properties:
            name:
              type: string
            pos:
              type: string
            team:
              type: string
            rating:
              type: integer
            img:
              type: string
    responses:
      200:
        description: Player successfully updated
      400:
        description: Missing a required field
      500:
        description: Issue during player update
    """
    try:
        data = request.get_json()
        player = Player(**data)

        if not player.name or not player.pos or not player.team or not int(player.rating) or not player.img:
            return jsonify({"error": f"missing a required field in request"}), 400

        id = current_app.player_service.update_player(
            player=player
        )

        return jsonify({"info": f"{player.name} successfully updated with id {id}"}), 200
    
    except Exception as ex:
        current_app.logger.error(f"update_player_entry() - Issue during player update process - {ex}")
        return jsonify({"error": f"issue during player update"}), 500