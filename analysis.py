import pandas as pd

def pickrate_analysis(team_df):
    picks_df = team_df[["pick1", "pick2", "pick3", "pick4", "pick5"]]
    
    total_games = len(team_df) / 2
    
    pick_counts = picks_df.stack().value_counts()
    
    pickrate = (pick_counts / total_games)

    league = team_df.iloc[0]["league"]
    patch = team_df.iloc[0]["patch"]
    split = team_df.iloc[0]["split"]

    results_list = []
    
    for champion, rate in pickrate.items():
        record = {
            "league": league,
            "patch": patch,
            "split": split,
            "total games": total_games,
            "champion": champion,
            "pickrate": rate
        }
        results_list.append(record)
    
    return results_list

def banrate_analysis(team_df):
    bans_df = team_df[["ban1", "ban2", "ban3", "ban4", "ban5"]]
    
    total_games = len(team_df) / 2
    
    ban_counts = bans_df.stack().value_counts()
    
    banrate = (ban_counts / total_games)

    league = team_df.iloc[0]["league"]
    patch = team_df.iloc[0]["patch"]
    split = team_df.iloc[0]["split"]

    results_list = []
    
    for champion, rate in banrate.items():
        record = {
            "league": league,
            "patch": patch,
            "split": split,
            "total games": total_games,
            "champion": champion,
            "banrate": rate
        }
        results_list.append(record)
    
    return results_list

def champ_winrate_analysis(player_df):
    champs_df = player_df[["champion", "result"]]
    wr_champs_df = champs_df.groupby("champion").agg(
    winrate=("result", "mean")).reset_index()
    
    wr_champs_df["league"] = player_df.iloc[0]["league"]
    wr_champs_df["patch"] = player_df.iloc[0]["patch"]
    wr_champs_df["split"] = player_df.iloc[0]["split"]

    results_list = wr_champs_df.to_dict('records')

    return results_list

def side_winrate_analysis(team_df):
    side_df = team_df[["side", "result"]]
    wr_side_df = side_df.groupby("side").agg(
    winrate=("result", "mean")).reset_index()

    wr_side_df["league"] = team_df.iloc[0]["league"]
    wr_side_df["patch"] = team_df.iloc[0]["patch"]
    wr_side_df["split"] = team_df.iloc[0]["split"]

    results_list = wr_side_df.to_dict('records')

    return results_list

def elder_winrate_analysis(team_df):
    elder_df = team_df[["elders", "result"]]
    elder_df = elder_df[elder_df["elders"] != 0]

    if not elder_df.empty:
        wr_elder_dict = elder_df.agg(
            winrate=("result", "mean"),
            count=("result", "count")
        ).to_dict()

        wr_elder_dict = {
            "winrate": wr_elder_dict["result"]["winrate"] ,
            "games": wr_elder_dict["result"]["count"],
            "objective": "elder"
        }
    else:
        wr_elder_dict = {
            "winrate": 0,
            "games": 0,
            "objective": "elder"
        }

    return wr_elder_dict

def baron_winrate_analysis(team_df):
    baron_df = team_df[["barons", "result"]]
    baron_df = baron_df[baron_df["barons"] != 0]
    wr_baron_dict = baron_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_baron_dict = {
        "winrate": wr_baron_dict["result"]["winrate"],
        "games": wr_baron_dict["result"]["count"],
        "objective": "baron" 
    }

    return wr_baron_dict

def herald_winrate_analysis(team_df):
    herald_df = team_df[["heralds", "result"]]
    herald_df = herald_df[herald_df["heralds"] != 0]
    wr_herald_dict = herald_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_herald_dict = {
        "winrate": wr_herald_dict["result"]["winrate"],
        "games": wr_herald_dict["result"]["count"],
        "objective": "herald"
    }

    return wr_herald_dict

def void_grub_winrate_analysis(team_df):
    void_grub_df = team_df[["void_grubs", "result"]]
    void_grub_df = void_grub_df[void_grub_df["void_grubs"] > 1]
    wr_void_grub_dict = void_grub_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_void_grub_dict = {
        "winrate": wr_void_grub_dict["result"]["winrate"],
        "games": wr_void_grub_dict["result"]["count"],
        "objective": "void grub"
    }

    return wr_void_grub_dict

def soul_winrate_analysis(team_df):
    soul = team_df[["elementaldrakes", "result"]]
    soul = soul[soul["elementaldrakes"] == 4]
    wr_soul_dict = soul.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_soul_dict = {
        "winrate": wr_soul_dict["result"]["winrate"],
        "games": wr_soul_dict["result"]["count"],
        "objective": "soul"
    }

    return wr_soul_dict

def dragon_soul_winrate_analysis(team_df):
    dragon_soul_df = team_df[["elementaldrakes", "infernals", "mountains", "clouds", "oceans", "chemtechs", "hextechs", "result"]]
    dragon_soul_df = dragon_soul_df[dragon_soul_df["elementaldrakes"] == 4]

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

    dragon_soul_df["soul"] = dragon_soul_df.apply(get_soul, axis=1)
    
    wr_dragon_soul_df = dragon_soul_df.groupby("soul").agg(
    winrate=("result", "mean"),
    count=("result", "count")).reset_index()

    wr_dragon_soul_df["league"] = team_df.iloc[0]["league"]
    wr_dragon_soul_df["patch"] = team_df.iloc[0]["patch"]
    wr_dragon_soul_df["split"] = team_df.iloc[0]["split"]

    results_list = wr_dragon_soul_df.to_dict('records')

    return results_list

def atakhan_winrate_analysis(team_df):
    atakhan_df = team_df[["atakhans", "result"]]
    atakhan_df = atakhan_df[atakhan_df["atakhans"] > 0]
    wr_atakhan_dict = atakhan_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_atakhan_dict = {
        "winrate": wr_atakhan_dict["result"]["winrate"],
        "games": wr_atakhan_dict["result"]["count"],
        "objective": "atakhan"
    }

    return wr_atakhan_dict

def game_length_analysis(team_df):
    game_length_df = team_df[["gameid", "gamelength"]]
    game_length_df = game_length_df.groupby("gameid")["gamelength"].mean().reset_index()

    game_length_df = game_length_df["gamelength"].mean()

    def calculate_time_seconds(sec_time):
        sec_time = int(sec_time)
        minutes = sec_time // 60
        seconds = sec_time % 60

        time_return = f"{minutes:02}:{seconds:02}"

        return time_return
    
    game_length_mean = calculate_time_seconds(game_length_df)

    game_length_dict = {
        "game_length_mean" : game_length_mean,
        "league" : team_df.iloc[0]["league"],
        "patch" : team_df.iloc[0]["patch"],
        "split" : team_df.iloc[0]["split"]
    }

    return game_length_dict

def objectives_analysis(team_df):

    elder_dict = elder_winrate_analysis(team_df)
    baron_dict = baron_winrate_analysis(team_df)
    herald_dict = herald_winrate_analysis(team_df)
    void_grub_dict = void_grub_winrate_analysis(team_df)
    soul_dict = soul_winrate_analysis(team_df)
    atakhan_dict = atakhan_winrate_analysis(team_df)

    objectives_list = [
        elder_dict,
        baron_dict,
        herald_dict,
        void_grub_dict,
        soul_dict,
        atakhan_dict
    ]

    objectives_df = pd.DataFrame(objectives_list)

    objectives_df["league"] = team_df.iloc[0]["league"]
    objectives_df["patch"] = team_df.iloc[0]["patch"]
    objectives_df["split"] = team_df.iloc[0]["split"] 

    results_list = objectives_df.to_dict('records')

    return results_list