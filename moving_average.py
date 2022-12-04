from connection import local_db
import numpy as np

WSIZE = 5

def main():
    db = local_db()

    # Find all gp_ids for users that have data for all 10 days (for testing purposes)
    db.cur.execute("""
    SELECT
        gp_id
    FROM
        last_10_history
    GROUP BY gp_id
    HAVING COUNT(*) = 10
    """)
    data = db.cur.fetchall()

    # Retrieve all data for each user
    ids = "("
    for item in data:
        ids += "\""+item[0]+"\","
    ids = ids[:-1] + ")"
    
    db.cur.execute("""
        SELECT 
            *
        FROM last_10_history
        WHERE gp_id IN
    """+ ids)
    res = db.cur.fetchall()
    
    # Insert retrieved data into a dictionary
    rtps = {}
    for idx in range(len(res)):
        gp_id = res[idx][1]
        if gp_id not in rtps:
            rtps[gp_id] = []
        rtps[gp_id].append(res[idx][5])

    # Calculate moving average for each user
    for key in rtps:
        i=0
        moving_averages = []
        while i < len(rtps[key]) - WSIZE + 1:
            window_average = round(np.sum(rtps[key][i:i+WSIZE]) / WSIZE, 2)
            moving_averages.append(window_average)
            i += 1
        print(key, moving_averages)

    db.conn.close()

if __name__ == "__main__":
    main()
        