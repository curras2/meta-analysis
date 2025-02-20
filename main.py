import df_generators as df_gen
import analysis as an
import db_conn as conn

lol_df = df_gen.create_lol_df()

unique_patches = lol_df['patch'].unique()
unique_splits = lol_df['split'].unique()
unique_leagues = lol_df['league'].unique()

for league in unique_leagues:
    if league == "LPL":
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
                        pickrate = an.pickrate_analysis(team_df)
                        banrate = an.banrate_analysis(team_df)
                        wr_champs_dict = an.champ_winrate_analysis(player_df)
                        wr_side_dict = an.side_winrate_analysis(team_df)
                        wr_objectives_dict = an.objectives_analysis(team_df)
                        wr_dragon_soul_dict = an.dragon_soul_winrate_analysis(team_df)
                        game_length_dict = an.game_length_analysis(team_df)
                        

                        conn.upsert_pickrate_record(pickrate)
                        conn.upsert_banrate_record(banrate)
                        conn.upsert_champion_winrate_record(wr_champs_dict)
                        conn.upsert_side_winrate_record(wr_side_dict)
                        conn.upsert_objectives_winrate_record(wr_objectives_dict)
                        conn.upsert_dragon_soul_winrate_record(wr_dragon_soul_dict)
                        conn.upsert_game_length_mean_record(game_length_dict)
                    except Exception as e:
                        columns_filtered_df.to_csv(f'{league} error.csv')
                        print(f"{league} ---- {e}")

pickrate_results_dict_list = conn.get_pickrate()
banrate_results_dict_list = conn.get_banrate()
champion_winrate_results_dict_list = conn.get_champion_winrate()
side_winrate_results_dict_list = conn.get_side_winrate()
objectives_winrate_results_dict_list = conn.get_objectives_winrate()
dragon_soul_winrate_results_dict_list = conn.get_dragon_soul_winrate()
game_length_mean_results_dict_list = conn.get_game_length_mean()

