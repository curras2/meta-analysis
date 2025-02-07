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
    # print(banrate.sort_values(ascending=False))

    player_league_df = league_filtered_df[league_filtered_df["position"] != "team"].copy()

    champs_df = player_league_df[["champion", "result"]]
    wr_champs_df = champs_df.groupby("champion").agg(
    winrate=("result", "mean"),
    count=("result", "count")).reset_index()
    
    wr_champs_df = wr_champs_df.rename(columns={"result": "winrate"})
    wr_champs_df["winrate"] = wr_champs_df["winrate"] * 100

    # print(wr_champs_df.sort_values(by="winrate", ascending=False))

    side_df = team_league_df[["side", "result"]]
    wr_side_df = side_df.groupby("side").agg(
    winrate=("result", "mean"),
    count=("result", "count")).reset_index()
    
    wr_side_df = wr_side_df.rename(columns={"result": "winrate"})
    wr_champs_df["winrate"] = wr_champs_df["winrate"] * 100

    # print(wr_side_df.sort_values(by="winrate", ascending=False))

    elder_df = team_league_df[["elders", "result"]]
    elder_df = elder_df[elder_df["elders"] != 0]
    wr_elder_df = elder_df.agg(
    winrate=("result", "mean"),
    count=("result", "count"))

    # print(wr_elder_df)

    baron_df = team_league_df[["barons", "result"]]
    baron_df = baron_df[baron_df["barons"] != 0]
    wr_baron_df = baron_df.agg(
    winrate=("result", "mean"),
    count=("result", "count"))

    # print(wr_baron_df)

    herald_df = team_league_df[["heralds", "result"]]
    herald_df = herald_df[herald_df["heralds"] != 0]
    wr_herald_df = herald_df.agg(
    winrate=("result", "mean"),
    count=("result", "count"))

    # print(wr_herald_df)

    void_grub_df = team_league_df[["void_grubs", "result"]]
    void_grub_df = void_grub_df[void_grub_df["void_grubs"] > 3]
    wr_void_grub_df = void_grub_df.agg(
    winrate=("result", "mean"),
    count=("result", "count"))

    # print(wr_void_grub_df)

    elementaldrake_df = team_league_df[["elementaldrakes", "result"]]
    elementaldrake_df = elementaldrake_df[elementaldrake_df["elementaldrakes"] == 4]
    wr_elementaldrake_df = elementaldrake_df.agg(
    winrate=("result", "mean"),
    count=("result", "count"))

    # print(wr_elementaldrake_df)

    drakes_df = team_league_df[["elementaldrakes", "infernals", "mountains", "clouds", "oceans", "chemtechs", "hextechs", "result"]]
    drakes_df = drakes_df[drakes_df["elementaldrakes"] == 4]

    def get_soul(row):
        if row["infernals"] >= 2:
            return "Infernal"
        elif row["mountains"] >= 2:
            return "Mountain"
        elif row["clouds"] >= 2:
            return "Cloud"
        elif row["oceans"] >= 2:
            return "Ocean"
        elif row["chemtechs"] >= 2:
            return "Chemtech"
        elif row["hextechs"] >= 2:
            return "Hextech"
        else:
            return "Unknown"

    drakes_df["soul"] = drakes_df.apply(get_soul, axis=1)
    wr_drakes_df = drakes_df.groupby("soul").agg(
    winrate=("result", "mean"),
    count=("result", "count")).reset_index()
    wr_drakes_df = wr_drakes_df.rename(columns={"result":"winrate"})
    wr_drakes_df["winrate"] = wr_drakes_df["winrate"] * 100

    # print(wr_drakes_df.sort_values(by="winrate", ascending=False))

    game_length_df = team_league_df[["gameid", "gamelength"]]
    game_length_df = game_length_df.groupby("gameid")["gamelength"].mean().reset_index()

    game_length_df = game_length_df["gamelength"].mean()

    def calculate_time_seconds(sec_time):
        sec_time = int(sec_time)
        minutes = sec_time // 60
        seconds = sec_time % 60

        time_return = f"{minutes:02}:{seconds:02}"

        return time_return
    
    print(calculate_time_seconds(game_length_df))
    