import pandas as pd
import numpy as np
import df_generators as df_gen
import analysis as an

lol_df = df_gen.create_lol_df()

leagues_list = [
    "LTA S",
    # "LTA N"
    ]

for i in leagues_list:
    league_df = df_gen.create_league_df(lol_df, i)

    league_columns_filtered_df = df_gen.define_columns_df(league_df)

    team_league_df = df_gen.create_team_league_df(league_columns_filtered_df)

    pickrate = an.pickrate_analysis(team_league_df)
    banrate = an.banrate_analysis(team_league_df)

    player_league_df = df_gen.create_player_league_df(league_columns_filtered_df)

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
    