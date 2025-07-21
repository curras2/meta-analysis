import pandas as pd

def create_lol_df():
    lol_csv_path = "extras/2025_LoL_esports_match_data_from_OraclesElixir.csv"
    lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})
    lol_df.loc[lol_df['league'].str.upper() == 'MSI','split'] = 'MSI'
    return lol_df

def create_league_df(lol_df, league):
    league_df = lol_df[lol_df["league"] == league].copy()
    return league_df

def create_split_df(league_df, split):
    split_df = league_df[league_df["split"] == split].copy()
    return split_df

def create_patch_df(split_df, patch):
    patch_df = split_df[split_df["patch"] == patch].copy()
    return patch_df

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
        "barons",
        "atakhans"
    ]

    league_filtered_df = league_df[columns_needed].copy()

    return league_filtered_df

def create_team_df(columns_filtered_df):
    team_df = columns_filtered_df[columns_filtered_df["position"] == "team"].copy()
    return team_df

def create_player_df(columns_filtered_df):
    player_df = columns_filtered_df[columns_filtered_df["position"] != "team"].copy()
    return player_df

def create_dataframe_from_list(dict_list):
    df = pd.DataFrame(dict_list)

    return df