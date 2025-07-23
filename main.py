import df_generators as df_gen
import analysis as an
import db_conn as conn
import traceback

lol_df = df_gen.create_lol_df()

unique_patches = lol_df['patch'].unique()
unique_splits = lol_df['split'].unique()
unique_leagues = lol_df['league'].unique()
leagues_filter = [
    "LCK",
    "LTA S",
    "LTA N",
    "LPL",
    "LEC",
    "MSI",
    "LCP",
    "LJL",
    "PCS",
    "MSI",
    "VCS"
]

for league in unique_leagues:
    if league not in leagues_filter:
        continue

    league_df = df_gen.create_league_df(lol_df, league)

    for split in unique_splits:
        split_df = df_gen.create_split_df(league_df, split)

        if not split_df.empty:
            for patch in unique_patches:
                patch_df = df_gen.create_patch_df(split_df, patch)

                if not patch_df.empty:
                    try:
                        columns_filtered_df = df_gen.define_columns_df(patch_df)

                        team_df = df_gen.create_team_df(columns_filtered_df)

                        player_df = df_gen.create_player_df(columns_filtered_df)

                        # Análise
                        pickrate_dict_list = an.pickrate_analysis(team_df)
                        banrate_dict_list = an.banrate_analysis(team_df)
                        wr_champs_dict_list = an.champ_winrate_analysis(player_df)
                        wr_side_dict_list = an.side_winrate_analysis(team_df)
                        wr_objectives_dict_list = an.objectives_analysis(team_df)
                        if league != "LPL":
                            wr_dragon_soul_dict_list = an.dragon_soul_winrate_analysis(team_df)
                        game_length_dict_list = an.game_length_analysis(team_df)
                        

                        conn.upsert_pickrate_record(pickrate_dict_list)
                        conn.upsert_banrate_record(banrate_dict_list)
                        conn.upsert_champion_winrate_record(wr_champs_dict_list)
                        conn.upsert_side_winrate_record(wr_side_dict_list)
                        conn.upsert_objectives_winrate_record(wr_objectives_dict_list)
                        if league != "LPL":
                            conn.upsert_dragon_soul_winrate_record(wr_dragon_soul_dict_list)
                        conn.upsert_game_length_mean_record(game_length_dict_list)
                    except Exception as e:
                        columns_filtered_df.to_csv(f'{league} error.csv')
                        print(f"{league} ---- {traceback.print_exception(e)}")

pickrate_results_dict_list = conn.get_pickrate()
banrate_results_dict_list = conn.get_banrate()
champion_winrate_results_dict_list = conn.get_champion_winrate()
side_winrate_results_dict_list = conn.get_side_winrate()
objectives_winrate_results_dict_list = conn.get_objectives_winrate()
dragon_soul_winrate_results_dict_list = conn.get_dragon_soul_winrate()
game_length_mean_results_dict_list = conn.get_game_length_mean()

pickrate_results_df = df_gen.create_dataframe_from_list(pickrate_results_dict_list)
banrate_results_df = df_gen.create_dataframe_from_list(banrate_results_dict_list)
champion_winrate_results_df = df_gen.create_dataframe_from_list(champion_winrate_results_dict_list)
side_winrate_results_df = df_gen.create_dataframe_from_list(side_winrate_results_dict_list)
objectives_winrate_results_df = df_gen.create_dataframe_from_list(objectives_winrate_results_dict_list)
dragon_soul_winrate_results_df = df_gen.create_dataframe_from_list(dragon_soul_winrate_results_dict_list)
game_length_mean_results_df = df_gen.create_dataframe_from_list(game_length_mean_results_dict_list)

pickrate_results_df.to_csv("extras/csv/pickrate.csv", index=False)
banrate_results_df.to_csv("extras/csv/banrate.csv", index=False)
champion_winrate_results_df.to_csv("extras/csv/champion_winrate.csv", index=False)
side_winrate_results_df.to_csv("extras/csv/side_winrate.csv", index=False)
objectives_winrate_results_df.to_csv("extras/csv/objectives_winrate.csv", index=False)
dragon_soul_winrate_results_df.to_csv("extras/csv/dragon_soul_winrate.csv", index=False)
game_length_mean_results_df.to_csv("extras/csv/game_length.csv", index=False)