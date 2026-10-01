from immaculate_api.database.db_players import PlayerData
from immaculate_api.models.models import Player, PlayerRequest

# following typical structure
# we don't really have any "business logic" though...
class PlayerService:
    def __init__(self):
        self.player_data = PlayerData()

    def get_all_players(self) -> list[dict]:
        try:
            return self.player_data.get_all_players()
        except Exception:
            raise

    def get_players(self, player_request: PlayerRequest) -> list[dict]:
        try:
            return self.player_data.get_players(player_request)
        except Exception:
            raise

    def create_player(self, player: Player) -> int:
        try:
            return self.player_data.create_player(player)
        except Exception:
            raise

    def delete_player(self, player: Player) -> int:
        try:
            return self.player_data.delete_player(player)
        except Exception:
            raise

    def update_player(self, player: Player) -> int:
        try:
            return self.player_data.update_player(player)   
        except Exception:
            raise