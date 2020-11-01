from click.testing import CliRunner
from leaderboard import get_stats


def test_inverse_parameters():
    runner = CliRunner()
    result1 = runner.invoke(get_stats, ["--mode", "r_wo", "--count", "2"])
    result2 = runner.invoke(get_stats, ["--count", "2", "--mode", "r_wo"])
    assert result2.output == result1.output
    assert result1.exit_code == 0
    assert result2.exit_code == 0


def test_country_count():
    runner = CliRunner()
    result = runner.invoke(get_stats, ["--mode", "r_wo", "--country", "ru"])
    assert result.output == "3\n"
    assert result.exit_code == 0


def test_wrong_mode():
    runner = CliRunner()
    result = runner.invoke(get_stats, ["--mode", "qwer"])
    assert result.output == "This mode doesn't exist. Available mods: r_macguffin, r_wo, " \
                            "r_rocket_arena_2, r_shaft_arena_1, r_ca_2, r_ca_1\n"
    assert result.exit_code == 0


def test_wrong_count():
    runner = CliRunner()
    result = runner.invoke(get_stats, ["--mode", "r_rocket_arena_2", "--user_id", "25bdfaf800b143ecbf361e1db12da390"])
    assert result.output == "{'user_id': '25bdfaf800b143ecbf361e1db12da390', 'name': 'erebucks', 'country': 'us', " \
                            "'match_type': 2, 'rating': '2025', 'rank_tier': 36, 'rank_position': None, " \
                            "'match_count': 53, 'match_wins': 41}\n"
    assert result.exit_code == 0
