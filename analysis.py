import pandas as pd

class Analysis:
    def __init__(self, team_df, player_df):
        self.team_df = team_df
        self.player_df = player_df
        self.league = self.team_df.iloc[0]["league"]
        self.patch = self.team_df.iloc[0]["patch"]
        self.split = self.team_df.iloc[0]["split"]
        self.league_pl = self.player_df.iloc[0]["league"]
        self.patch_pl = self.player_df.iloc[0]["patch"]
        self.split_pl = self.player_df.iloc[0]["split"]

    def pickrate_analysis(self):
        picks_df = self.team_df[["pick1", "pick2", "pick3", "pick4", "pick5"]]
        
        total_games = len(self.team_df) / 2
        
        pick_counts = picks_df.stack().value_counts()
        
        pickrate = (pick_counts / total_games)

        

        results_list = []
        
        for champion, rate in pickrate.items():
            record = {
                "league": self.league,
                "patch": self.patch,
                "split": self.split,
                "picked games": round(rate*total_games),
                "total games": total_games,
                "champion": champion,
                "pickrate": rate
            }
            results_list.append(record)
        
        return results_list

    def banrate_analysis(self):
        bans_df = self.team_df[["ban1", "ban2", "ban3", "ban4", "ban5"]]
        
        total_games = len(self.team_df) / 2
        
        ban_counts = bans_df.stack().value_counts()
        
        banrate = (ban_counts / total_games)

        results_list = []
        
        for champion, rate in banrate.items():
            record = {
                "league": self.league,
                "patch": self.patch,
                "split": self.split,
                "banned games": round(rate*total_games),
                "total games": total_games,
                "champion": champion,
                "banrate": rate
            }
            results_list.append(record)
        
        return results_list

    def champ_winrate_analysis(self):
        champs_df = self.player_df[["champion", "result"]]
        wr_champs_df = champs_df.groupby("champion").agg(
        winrate=("result", "mean")).reset_index()
        
        wr_champs_df["league"] = self.league_pl
        wr_champs_df["patch"] = self.patch_pl
        wr_champs_df["split"] = self.split_pl

        results_list = wr_champs_df.to_dict('records')

        return results_list

    def side_winrate_analysis(self):
        side_df = self.team_df[["side", "result"]]
        wr_side_df = side_df.groupby("side").agg(
        winrate=("result", "mean")).reset_index()

        wr_side_df["league"] = self.league
        wr_side_df["patch"] = self.patch
        wr_side_df["split"] = self.split

        results_list = wr_side_df.to_dict('records')

        return results_list

    def __elder_winrate_analysis(self):
        elder_df = self.team_df[["elders", "result"]]
        elder_df = elder_df[elder_df["elders"] > 0]

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

    def __baron_winrate_analysis(self):
        baron_df = self.team_df[["barons", "result"]]
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

    def __herald_winrate_analysis(self):
        herald_df = self.team_df[["heralds", "result"]]
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

    def __void_grub_winrate_analysis(self):
        void_grub_df = self.team_df[["void_grubs", "result"]]
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

    def __soul_winrate_analysis(self):
        if self.team_df.iloc[0]["league"] != "LPL":
            soul = self.team_df[["elementaldrakes", "result"]]
            soul = soul[soul["elementaldrakes"] == 4]
        else:
            soul = self.team_df[["dragons (type unknown)", "result"]]
            soul = soul[soul["dragons (type unknown)"] == 4]
        
        wr_soul_dict = soul.agg(
        winrate=("result", "mean"),
        count=("result", "count")).to_dict()

        wr_soul_dict = {
            "winrate": wr_soul_dict["result"]["winrate"],
            "games": wr_soul_dict["result"]["count"],
            "objective": "soul"
        }

        return wr_soul_dict

    def dragon_soul_winrate_analysis(self):
        dragon_soul_df = self.team_df[["elementaldrakes", "infernals", "mountains", "clouds", "oceans", "chemtechs", "hextechs", "result"]]
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

        wr_dragon_soul_df["league"] = self.league
        wr_dragon_soul_df["patch"] = self.patch
        wr_dragon_soul_df["split"] = self.split

        results_list = wr_dragon_soul_df.to_dict('records')

        return results_list

    def __atakhan_winrate_analysis(self):
        atakhan_df = self.team_df[["atakhans", "result"]]
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

    def game_length_analysis(self):
        game_length_df = self.team_df[["gameid", "gamelength"]]
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
            "league" : self.league,
            "patch" : self.patch,
            "split" : self.split
        }

        results_list = []
        results_list.append(game_length_dict)

        return results_list

    def objectives_analysis(self):
        baron_dict = self.__baron_winrate_analysis()
        herald_dict = self.__herald_winrate_analysis()
        void_grub_dict = self.__void_grub_winrate_analysis()
        soul_dict = self.__soul_winrate_analysis()

        objectives_list = [
            baron_dict,
            herald_dict,
            void_grub_dict,
            soul_dict
        ]

        if self.league != "LPL":
            atakhan_dict = self.__atakhan_winrate_analysis()
            elder_dict = self.__elder_winrate_analysis()
            
            objectives_list.append(atakhan_dict)
            objectives_list.append(elder_dict)

        objectives_df = pd.DataFrame(objectives_list)

        objectives_df["league"] = self.league
        objectives_df["patch"] = self.patch
        objectives_df["split"] = self.split

        results_list = objectives_df.to_dict('records')

        return results_list
