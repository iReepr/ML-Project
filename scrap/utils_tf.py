import requests
from urllib.parse import urljoin
import pycountry
from datetime import datetime

def iso_alpha3_to_country_name(alpha3_code):
    try:
        country = next(
            country for country in pycountry.countries if country.alpha_3 == alpha3_code
        )
        return country.name
    except StopIteration:
        return None

# alpha3_code = "ARG"
# country_name = iso_alpha3_to_country_name(alpha3_code)
# print(country_name)


url = "http://localhost:8000/"
t_url = "https://www.transfermarkt.com/"

def search_club(club_name: str) -> tuple[int, dict]:
    """
    Search for a club by name.
    """
    response = requests.get(urljoin(url, f"clubs/search/{club_name}"))
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if len(results) > 0:
            return results[0]  # Return the first matching club
    return None

def get_player_market_value(player_id: int) -> tuple[int, dict]:
    """
    Get a player by ID.
    """
    response = requests.get(urljoin(url, f"players/{player_id}/market_value"))
    if response.status_code == 200:
        return (200, response.json())
    else:
        return (response.status_code, {"error": f"Failed to get player: {response.status_code}"})
    
def get_player_transfers(player_id: int) -> tuple[int, dict]:
    """
    Get a player's transfers by ID.
    """
    response = requests.get(urljoin(url, f"players/{player_id}/transfers"))
    if response.status_code == 200:
        return (200, response.json())
    else:
        return (response.status_code, {"error": f"Failed to get player transfers: {response.status_code}"})
    
def build_player_url(player_id: int, player_name: str) -> str:
    """
    Build a URL for a player by ID.
    """
    player_name = player_name.lower().replace(" ", "-")
    return urljoin(t_url, f"{player_name}/profil/spieler/{player_id}/")
    

def search_player(player_name: str, nationality = "", club = "") -> tuple[int, dict, dict]:
    """
    Search for a player by name.
    """
    response = requests.get(urljoin(url, f"players/search/{player_name}"))
    if response.status_code == 200:
        data = response.json()
        for player in data["results"]:
            data = player
            
            # Check if nationality match
            if nationality and len(nationality) > 0 and "nationalities" in player :
                nationalities = player["nationalities"]
                nationality = iso_alpha3_to_country_name(nationality)
                if nationality != None and len(nationality) > 0 and nationality not in [n for n in nationalities]:
                    continue
            
            values = get_player_market_value(player["id"])
            history = values[1].get("marketValueHistory", [])                
            # Check if club match
            if club and len(club) > 0 and "club" in player :
                if player["club"] != club:
                    if len(history) > 0:
                        if not any(entry.get("clubId") == club for entry in history):
                            continue
            # player found
            return 200, player, history
            """
            start_date = datetime.strptime("17-08-2024", "%d-%m-%Y")
            end_date = datetime.strptime("25-05-2025", "%d-%m-%Y")

            filtered_values = [
                entry for entry in history
                if start_date <= datetime.strptime(entry["date"], "%Y-%m-%d") <= end_date
            ]

            if filtered_values:
                last_value = filtered_values[-1]["marketValue"]
                print(f"Last market value in the specified range: {last_value}")
            else:
                print("No market value found in the specified range.")
            return (200, player)
            """
            # return (200, response.json())
        
    return (response.status_code, {"error": f"Failed to search for player: {response.status_code}"}, [])

if __name__ == "__main__":
    # Example usage
    print(search_player("Ro Abajas"))
    # print(search_club("Real Madrid"))
    # for i in range(1, 1000):
    #     # print(get_player_transfers(i))
    #     result = search_player("Neymar")
    #     if "error" in result[1]:
    #         print("error")
    # print(get_player_market_value(471690))
