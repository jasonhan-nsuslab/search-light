def get_positive_rtps(cur, conn):
    cur.execute("select aggregated_at, gp_id, game_code, round(rtp_win_amount/rtp_bet_amount,4)::float as rtp, bet_count from stats_game_rtp_per_user sgrpu where bet_count>10 and rtp_win_amount/rtp_bet_amount > 1 order by aggregated_at, game_code, bet_count")
    data = cur.fetchall()
    conn.close()
    return data


