import numpy as np
from datetime import date, timedelta

def get_history(cur_stats, cur_local, conn_local, cur_gp):
    
    # Get data from cur_date to end_date
    cur_date = date(2022, 9, 1)
    end_date = date(2022, 9, 30)
    delta = timedelta(days=1)
    print("Starting data collection.\n")
    while cur_date <= end_date:
        # Data retrieval is split into individual days due to max packet size restrictions
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
        
        # For each retrieved day, if the nickname is not already stored, get it from db_gp.
        # Also split into days due to max packet size restrictions

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

def get_abusers(db, wsize, tsize):

    # Retrieve data from history per user per day
    print("Retrieving user history")
    db.cur.execute("""
    SELECT
        gp_id,
        rtp,
        aggregated_at
    FROM
        coalesced_history
    """)
    res = db.cur.fetchall()
    
    # Insert retrieved data into a dictionary in the format {"gpid":[rtp1, rtp2, ... rtpm]}
    rtps = {}
    for idx in range(len(res)):
        gp_id = res[idx][0]
        if gp_id not in rtps:
            rtps[gp_id] = []
        rtps[gp_id].append(res[idx][1])

    # Calculate moving average for each user using the last 10 days
    abusers = []
    for key in rtps:
        # If the user has less than the required total days played, skip
        if len(rtps[key])<tsize:
            continue
        i=0
        moving_averages = []
        while i < tsize - wsize + 1:
            window_average = round(np.sum(rtps[key][i:i+wsize]) / wsize, 2)
            moving_averages.append(window_average)
            i += 1
        if min(moving_averages) >= 1:
            abusers.append((key,))

    # Get abuser IDs and insert them into table
    print("Inserting abuser IDs")
    query = """
    INSERT INTO abusers
    VALUES(
        %s
    )
    """
    db.cur.executemany(query, abusers)
    print("Done.")
    db.conn.commit()
    db.conn.close()