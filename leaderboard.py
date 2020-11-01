import requests
import click


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
    params = {
        'mode': mode,
        'offset': 0
    }
    # make a request to API
    try:
        res = requests.get(api_url, params=params)
    except requests.exceptions.ConnectionError:
        result.append("Cannot connect to API")
        print_info(result)
        return

    # if count is less than 0, print an error
    if count is not None and count < 0:
        result.append("--count parameter cannot be less than 0")
        print_info(result)
        return

    # get data in json format
    data = res.json()
    # extract list from dictionary
    data = data['leaderboard']

    # There we need to select certain players
    if user_id:
        for each_player in data:
            if each_player['user_id'] == user_id:
                result.append(each_player)
        if not result:  # if there were not any player with specified id
            result.append("It seems that there is no player with this id")
            print_info(result)
        else:
            if count is None:  # if count is specified -> need to display info about N players
                print_info(result)
            else:
                print_info(result[:count])

    elif country:
        counter = 0
        for each_player in data:  # count number of players in certain country
            if each_player['country'] == country:
                counter += 1
        if counter == 0:
            result.append("There is no such country")
            print_info(result)
            return

        if count is None:  # if count wasn't specified, need to display number of players in certain country
            result.append(counter)
            print_info(result)
        else:   # if count is specified, need to display minimum from 'count' and number of counted players
            result.append(min([counter, count]))
            print_info(result)

    else:
        # delete field 'user_id'
        for player in data:
            del player['user_id']
        if count is None:
            print_info(data)
        else:
            print_info(data[:count])


def print_info(info):
    for player in info:
        print(player)


if __name__ == '__main__':
    get_stats()
