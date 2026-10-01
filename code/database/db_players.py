from code import mongo
from flask import current_app
from code.models.models import Player, PlayerRequest

class PlayerData():
    def __init__(self):
        pass

    def get_players(self, player_request: PlayerRequest) -> list[dict]:
        """
        Gets a random sample of players based off of passed in player_count value. Returns a list of records.
        """
        try:
            # it seems to be standard to do the queries like this
            # aggregate involves something like a "pipeline" which is something like a multi-stage data transformation
            match: dict = dict()

            # never null
            match["rating"] = {"$lt": player_request.rating}

            # could be simpler if used a dictionary instead of a class, but I like having the model for PlayerRequest for clarity
            if player_request.pos:
                match["pos"] = player_request.pos

            if player_request.name:
                match["name"] = player_request.name

            if player_request.team:
                match["team"] = player_request.team

            # sample if random
            query = ( 
                [{"$match": match}, {"$sample": {"size": int(player_request.count)}}] if player_request.count 
                else [{"$match": match}]
            )
            
            players: list = list()
            players = list(mongo.db.players.aggregate(query))

            return players
        except Exception:
            raise

# helper for create_player to lookup if a certain player already exists
    def get_player_by_name(self, player: Player) -> list[dict]:
        try:
            query = {
                "name": player.name,
                "pos": player.pos
            }
        
            # initialize first in case nothing returned
            player: list = list()
            player = list(mongo.db.players.find(query))
            
            return player
        except Exception as ex:
            current_app.logger.error(f"get_player_by_name() - Issue retrieving player by name {player.name} - {ex}")
            raise

    # specific query to get all players, used by get_players()
    def get_all_players(self) -> list[dict]:
        try:
            result: list[dict] = mongo.db.players.find({})

            return result
        except Exception as ex:
            current_app.logger.error(f"get_all_players() - error getting all players - {ex}")
            raise
        

    # creates a player, requires all fields
    def create_player(self, player: Player) -> int:
        try:
            query = {
                    "name": player.name,
                    "pos": player.pos,
                    "rating": int(player.rating),
                    "img": player.img,
                    "team": player.team
                    }
    
            if self.get_player_by_name(player):
                current_app.logger.info(f"create_player() - Player {player.name} already exists. Updating...")
                id = self.update_player(player)
            else:
                id = mongo.db.players.insert_one(query)
                
            return id
        except Exception:
            raise


    # deletes a player, only requres name, pos, team
    def delete_player(self, player: Player) -> int:
        try:
            dq = {
                    "name": player.name,
                    "pos": player.pos,
                    "team": player.team
                } 

            result = mongo.db.players.delete_many(dq)

            current_app.logger.info(f"Deleted {result.deleted_count} with name {player.name}.")
            return result.deleted_count
        except Exception:
            raise

    # uses position as a tiebreaker (word from PO)
    def update_player(self, player: Player) -> int:
        # might need to put more effort into this update? im thinking wherever uses this can autopopulate the fields with the players current info
        # so that when the request is sent we don't blanks sent or unwanted data changed
        try:
            dq = {
                "name": player.name,
                "pos": player.pos,
                "rating": player.rating,
                "img": player.img,
                "team": player.team
            }

            filter = {
                "name": player.name,
                "pos": player.pos
            }
            # updatemany might be preferable ??

            result = mongo.db.players.update_one(filter, {"$set": dq})

            # will most likely only ever find one... no idea if there will be a situation where two players with the same name yknow
            # maybe need some sort of differentiator for players with the same name? team? idk not sure if there are many
            # current_app.logger.info(f"Found {result.matchedCount} player(s) and updated {result.modifiedCount} of them.")
            return result
        except Exception:
            raise