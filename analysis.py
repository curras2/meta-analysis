def pickrate_analysis(team_league_df):
    picks_df = team_league_df[["pick1", "pick2", "pick3", "pick4", "pick5"]]
    
    total_games = len(team_league_df) / 2
    
    pick_counts = picks_df.stack().value_counts()
    
    pickrate = (pick_counts / total_games) *100
    
    return pickrate

def banrate_analysis(team_league_df):
    bans_df = team_league_df[["ban1", "ban2", "ban3", "ban4", "ban5"]]
    
    total_games = len(team_league_df) / 2
    
    ban_counts = bans_df.stack().value_counts()
    
    banrate = (ban_counts / total_games) *100
    
    return banrate