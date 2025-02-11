import df_generators as df_gen
import analysis as an
import db_conn as conn

lol_df = df_gen.create_lol_df()

leagues_list = [
    "LTA S",
    # "LTA N"
    ]

for i in leagues_list:
    # Dataframes principais
    league_df = df_gen.create_league_df(lol_df, i)

    league_columns_filtered_df = df_gen.define_columns_df(league_df)

    team_league_df = df_gen.create_team_league_df(league_columns_filtered_df)

    player_league_df = df_gen.create_player_league_df(league_columns_filtered_df)

    # Análise
    pickrate = an.pickrate_analysis(team_league_df)
    banrate = an.banrate_analysis(team_league_df)
    wr_champs_df = an.champ_winrate_analysis(player_league_df)
    wr_side_df = an.side_winrate_analysis(team_league_df)
    wr_elder_df = an.elder_winrate_analysis(team_league_df)
    wr_baron_df = an.baron_winrate_analysis(team_league_df)
    wr_herald_df = an.herald_winrate_analysis(team_league_df)
    wr_void_grub_df = an.void_grub_winrate_analysis(team_league_df)
    wr_soul_df = an.soul_winrate_analysis(team_league_df)
    wr_dragon_soul_df = an.dragon_soul_winrate_analysis(team_league_df)
    game_length_mean = an.game_length_analysis(team_league_df)

    conn.upsert_pickrate_record(pickrate)
    conn.upsert_banrate_record(banrate)