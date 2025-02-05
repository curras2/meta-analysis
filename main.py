import pandas as pd
import numpy as np

lol_csv_path = "extras/2025_LoL_esports_match_data_from_OraclesElixir.csv"
lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

leagues_list = [
    "LTA S",
    "LTA N"
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
        "playername",
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