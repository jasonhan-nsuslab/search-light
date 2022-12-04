from connection import local_db

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

    for id in data:
        db.cur.execute("""
        SELECT
            *
        FROM
            last_10_history
        WHERE gp_id = %s
        """, (id[0],))
        user = db.cur.fetchall()
        print(user)

    db.conn.close()

if __name__ == "__main__":
    main()


    # ids = "("
    # for item in data:
    #     ids += "\""+item[0]+"\","
    # ids = ids[:-1] + ")"
    
    # db.cur.execute("""
    #     SELECT 
    #         *
    #     FROM last_10_history
    #     WHERE gp_id IN
    # """+ ids)
    # res = db.cur.fetchall()