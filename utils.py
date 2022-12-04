from datetime import date, timedelta

def get_positive_rtps(cur_stats, cur_local, conn_local, cur_gp):
    cur_date = date(2022, 9, 1)
    end_date = date(2022, 9, 30)
    delta = timedelta(days=1)
    print("Starting data collection.\n")
    while cur_date <= end_date:
        print("Inserting data from "+str(cur_date))
        
        cur_stats.execute("""
            SELECT 
                aggregated_at,
                gp_id,
                game_code,
                sum(rtp_bet_amount) as total_bet,
                sum(rtp_win_amount) as total_win,
                sum(rtp_win_amount)-sum(rtp_bet_amount) as profit,
                sum(rtp_win_amount)/sum(rtp_bet_amount) as rtp,
                sum(bet_count)
            FROM stats_game_rtp_per_user
            WHERE aggregated_at=%s
            GROUP BY aggregated_at, gp_id, game_code
            HAVING sum(bet_count)>1
        """, (cur_date,))
        data = cur_stats.fetchall()
        
        query = """
            INSERT INTO win_history(
                aggregated_at,
                gp_id,
                game_code,
                total_bet,
                total_win,
                profit,
                rtp,
                bet_count
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur_local.executemany(query, data)
        
        print("Getting nicknames\n")
        
        cur_local.execute("""
            SELECT
                DISTINCT gp_id
            FROM win_history
            WHERE gp_id NOT IN(
                SELECT gp_id
                FROM account_details
                )
        """)
        data = cur_local.fetchall()
        
        ids = "("
        for item in data:
            ids += "\""+item[0]+"\","
        ids = ids[:-1] + ")"
        
        cur_gp.execute("""
            SELECT 
                gp_id,
                nickname
            FROM account
            WHERE gp_id IN
        """ + ids)
        res = cur_gp.fetchall()
        
        query = """
            INSERT INTO account_details(
                gp_id,
                nickname
            )
            VALUES(%s,%s)
        """
        cur_local.executemany(query, res)
        
        cur_date += delta
    conn_local.commit()

def get_today_rtps(cur_stats, cur_local, conn_local, cur_gp):
    cur_date = date.today()
    cur_stats.execute("""
        SELECT 
            aggregated_at,
            gp_id,
            game_code,
            sum(rtp_bet_amount) as total_bet,
            sum(rtp_win_amount) as total_win,
            sum(rtp_win_amount)-sum(rtp_bet_amount) as profit,
            sum(rtp_win_amount)/sum(rtp_bet_amount) as rtp,
            sum(bet_count)
        FROM stats_game_rtp_per_user
        WHERE aggregated_at=%s
        GROUP BY aggregated_at, gp_id, game_code
        HAVING sum(bet_count)>1
    """, (cur_date,))
    data = cur_stats.fetchall()
    query = """
        INSERT INTO win_history(
            aggregated_at,
            gp_id,
            game_code,
            total_bet,
            total_win,
            profit,
            rtp,
            bet_count
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur_local.executemany(query, data)
    cur_local.execute("""
        SELECT
            DISTINCT gp_id
        FROM win_history
        WHERE gp_id NOT IN(
            SELECT gp_id
            FROM account_details
            )
    """)
    data = cur_local.fetchall()
    ids = "("
    for item in data:
        ids += "\""+item[0]+"\","
    ids = ids[:-1] + ")"
    cur_gp.execute("""
        SELECT
            gp_id,
            nickname
        FROM account
        WHERE gp_id IN
    """ + ids)
    res = cur_gp.fetchall()
    query = """
        INSERT INTO account_details(
            gp_id,
            nickname
        )
        VALUES(%s,%s)
    """
    cur_local.executemany(query, res)
    conn_local.commit()

# def get_nicknames(cur_local, conn_local, cur_gp):
#     print("Getting nicknames")
#     cur_local.execute("""
#         SELECT
#             DISTINCT gp_id
#         FROM win_history
#         WHERE gp_id NOT IN(
#             SELECT gp_id
#             FROM account_details
#             )
#     """)
#     data = cur_local.fetchall()
#     ids = "("
#     for item in data:
#         ids += "\""+item[0]+"\","
#     ids = ids[:-1] + ")"
#     cur_gp.execute("""
#         SELECT 
#             gp_id,
#             nickname
#         FROM account
#         WHERE gp_id IN
#     """ + ids)
#     res = cur_gp.fetchall()
#     query = """
#         INSERT INTO account_details(
#             gp_id,
#             nickname
#         )
#         VALUES(%s,%s)
#     """
#     cur_local.executemany(query, res)
#     conn_local.commit()