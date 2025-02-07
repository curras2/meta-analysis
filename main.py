import pandas as pd
import numpy as np

lol_csv_path = "extras/2025_LoL_esports_match_data_from_OraclesElixir.csv"
lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

leagues_list = [
    "LTA S",
    # "LTA N"
    ]

for i in leagues_list:
    league_df = lol_df[lol_df["league"] == i].copy()

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

    team_league_df = league_filtered_df[league_filtered_df["position"] == "team"].copy()

    picks_df = team_league_df[["pick1", "pick2", "pick3", "pick4", "pick5"]]

    bans_df = team_league_df[["ban1", "ban2", "ban3", "ban4", "ban5"]]

    total_games = len(team_league_df) / 2

    pick_counts = picks_df.stack().value_counts()
    ban_counts = bans_df.stack().value_counts()

    pickrate = (pick_counts / total_games) *100
    banrate = (ban_counts / total_games) *100

    # print(pickrate.sort_values(ascending=False))
    print(banrate.sort_values(ascending=False))