import pandas as pd

def create_lol_df():
    lol_csv_path = "extras/2025_LoL_esports_match_data_from_OraclesElixir.csv"
    lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

    return lol_df

def create_league_df(lol_df, league):
    league_df = lol_df[lol_df["league"] == league].copy()
    return league_df

def define_columns_df(league_df):
    columns_needed = [
        "gameid",
        "datacompleteness",
        "league",
        "year",
        "split",
        "playoffs",
        "date",
        "game",
        "patch",
        "side",
        "position",
        "teamname",
        "champion",
        "ban1",
        "ban2",
        "ban3",
        "ban4",
        "ban5",
        "pick1",
        "pick2",
        "pick3",
        "pick4",
        "pick5",
        "gamelength",
        "result",
        "dragons",
        "elementaldrakes",
        "infernals",
        "mountains",
        "clouds",
        "oceans",
        "chemtechs",
        "hextechs",
        "dragons (type unknown)",
        "elders",
        "heralds",
        "void_grubs",
        "barons"
    ]

    league_filtered_df = league_df[columns_needed].copy()

    return league_filtered_df

def create_team_league_df(league_columns_filtered_df):
    team_league_df = league_columns_filtered_df[league_columns_filtered_df["position"] == "team"].copy()
    return team_league_df

def create_player_league_df(league_columns_filtered_df):
    player_league_df = league_columns_filtered_df[league_columns_filtered_df["position"] != "team"].copy()
    return player_league_df