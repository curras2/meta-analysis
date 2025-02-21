def pickrate_analysis(team_df):
    picks_df = team_df[["pick1", "pick2", "pick3", "pick4", "pick5"]]
    
    total_games = len(team_df) / 2
    
    pick_counts = picks_df.stack().value_counts()
    
    pickrate = (pick_counts / total_games) *100

    pickrate = pickrate.to_dict()

    pickrate["league"] = team_df.iloc[0]["league"]
    pickrate["patch"] = team_df.iloc[0]["patch"]
    pickrate["split"] = team_df.iloc[0]["split"]
    pickrate["total games"] = total_games
    
    return pickrate

def banrate_analysis(team_df):
    bans_df = team_df[["ban1", "ban2", "ban3", "ban4", "ban5"]]
    
    total_games = len(team_df) / 2
    
    ban_counts = bans_df.stack().value_counts()
    
    banrate = (ban_counts / total_games) *100

    banrate = banrate.to_dict()

    banrate["league"] = team_df.iloc[0]["league"]
    banrate["patch"] = team_df.iloc[0]["patch"]
    banrate["split"] = team_df.iloc[0]["split"]
    banrate["total games"] = total_games
    
    return banrate

def champ_winrate_analysis(player_df):
    champs_df = player_df[["champion", "result"]]
    wr_champs_df = champs_df.groupby("champion").agg(
    winrate=("result", "mean")).reset_index()
    
    wr_champs_df["winrate"] = wr_champs_df["winrate"] * 100

    wr_champs_dict = dict(zip(wr_champs_df["champion"], wr_champs_df["winrate"]))

    wr_champs_dict["league"] = player_df.iloc[0]["league"]
    wr_champs_dict["patch"] = player_df.iloc[0]["patch"]
    wr_champs_dict["split"] = player_df.iloc[0]["split"]

    return wr_champs_dict

def side_winrate_analysis(team_df):
    side_df = team_df[["side", "result"]]
    wr_side_df = side_df.groupby("side").agg(
    winrate=("result", "mean")).reset_index()
    
    wr_side_dict = dict(zip(wr_side_df["champion"], wr_side_df["winrate"]))

    wr_side_dict["league"] = team_df.iloc[0]["league"]
    wr_side_dict["patch"] = team_df.iloc[0]["patch"]
    wr_side_dict["split"] = team_df.iloc[0]["split"]

    return wr_side_dict

def elder_winrate_analysis(team_df):
    elder_df = team_df[["elders", "result"]]
    elder_df = elder_df[elder_df["elders"] != 0]

    if not elder_df.empty:
        wr_elder_dict = elder_df.agg(
            winrate=("result", "mean"),
            count=("result", "count")
        ).to_dict()

        wr_elder_dict = {
            "winrate": wr_elder_dict["result"]["winrate"] * 100,
            "count": wr_elder_dict["result"]["count"],
        }
    else:
        wr_elder_dict = {
            "winrate": 0,
            "count": 0,
        }

    return wr_elder_dict

def baron_winrate_analysis(team_df):
    baron_df = team_df[["barons", "result"]]
    baron_df = baron_df[baron_df["barons"] != 0]
    wr_baron_dict = baron_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_baron_dict = {
        "winrate": wr_baron_dict["result"]["winrate"]* 100,
        "count": wr_baron_dict["result"]["count"],
    }

    return wr_baron_dict

def herald_winrate_analysis(team_df):
    herald_df = team_df[["heralds", "result"]]
    herald_df = herald_df[herald_df["heralds"] != 0]
    wr_herald_dict = herald_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_herald_dict = {
        "winrate": wr_herald_dict["result"]["winrate"]* 100,
        "count": wr_herald_dict["result"]["count"],
    }

    return wr_herald_dict

def void_grub_winrate_analysis(team_df):
    void_grub_df = team_df[["void_grubs", "result"]]
    void_grub_df = void_grub_df[void_grub_df["void_grubs"] > 3]
    wr_void_grub_dict = void_grub_df.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_void_grub_dict = {
        "winrate": wr_void_grub_dict["result"]["winrate"]* 100,
        "count": wr_void_grub_dict["result"]["count"],
    }

    return wr_void_grub_dict

def soul_winrate_analysis(team_df):
    soul = team_df[["elementaldrakes", "result"]]
    soul = soul[soul["elementaldrakes"] == 4]
    wr_soul_dict = soul.agg(
    winrate=("result", "mean"),
    count=("result", "count")).to_dict()

    wr_soul_dict = {
        "winrate": wr_soul_dict["result"]["winrate"]* 100,
        "count": wr_soul_dict["result"]["count"],
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
    
    wr_dragon_soul_df = wr_dragon_soul_df.rename(columns={"result":"winrate"})
    
    wr_dragon_soul_df["winrate"] = wr_dragon_soul_df["winrate"] * 100

    wr_dragon_soul_dict = wr_dragon_soul_df.set_index("soul")[["winrate", "count"]].to_dict(orient="index")

    wr_dragon_soul_dict["league"] = team_df.iloc[0]["league"]
    wr_dragon_soul_dict["patch"] = team_df.iloc[0]["patch"]
    wr_dragon_soul_dict["split"] = team_df.iloc[0]["split"]

    return wr_dragon_soul_dict

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

    objectives_dict = {
        "elder": elder_winrate_analysis(team_df),
        "baron": baron_winrate_analysis(team_df),
        "herald": herald_winrate_analysis(team_df),
        "void_grub": void_grub_winrate_analysis(team_df),
        "soul": soul_winrate_analysis(team_df),
        "league" : team_df.iloc[0]["league"],
        "patch" : team_df.iloc[0]["patch"],
        "split" : team_df.iloc[0]["split"]

    }

    return objectives_dict