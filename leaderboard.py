import requests
import click

offset_size = 20


@click.command()
@click.option("--mode", "mode", required=True, help="game mode")
@click.option("--user_id", "user_id", help="identifier of user")
@click.option("--count", "count", help="number of entries to display", type=int)
@click.option("--country", "country", help="country of player")
def get_stats(mode, user_id, count, country):
    # list to store results about information of players
    result = []
    # display available game modes to the user
    available_mods = ['r_macguffin', 'r_wo', 'r_rocket_arena_2', 'r_shaft_arena_1', 'r_ca_2', 'r_ca_1']
    if mode not in available_mods:
        result.append("This mode doesn't exist. Available mods: " + ", ".join(available_mods) + ".")
        print_info(result)
        return

    api_url = "https://www.diabotical.com/api/v0/stats/leaderboard"
    offset = 0
    while True:
        params = {
            'mode': mode,
            'offset': offset
        }
        offset += offset_size
        # make a request to API
        try:
            res = requests.get(api_url, params=params)
        except requests.exceptions.ConnectionError:
            result.append("Cannot connect to API")
            print_info(result)
            return
        # get data in json format and extract list from dictionary
        data = res.json()['leaderboard']
        # if we get empty response, it means that data ran out
        if not data:
            break
        for player in data:
            result.append(player)

        if count is not None and offset >= count:
            result = result[:count]
            break

        # in this case we only need to display only 20 players
        if user_id is None and country is None and count is None:
            break

    # if count is less than 0, print an error
    if count is not None and count < 0:
        print_info("--count parameter cannot be less than 0")
        return

    # There we need to select certain players
    if user_id:
        certain_players = []
        for player in result:
            if player['user_id'] == user_id:
                certain_players.append(player)
        if not certain_players:  # if there were not any player with specified id
            print_info("It seems that there is no player with this id")
            return
        else:
            print_info(certain_players)

    elif country:
        counter = 0
        for player in result:  # count number of players in certain country
            if player['country'] == country:
                counter += 1
        if counter == 0:
            print_info("There is no any player from such country")
            return

        print_info(counter)

    else:
        for player in result:
            # delete field 'user_id'
            del player['user_id']
        print_info(result)


def print_info(info):
    if isinstance(info, list):
        for player in list(info):
            print(player)
    else:
        print(info)


if __name__ == '__main__':
    get_stats()
