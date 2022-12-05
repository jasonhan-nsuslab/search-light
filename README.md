# Searchlight
Retrieves data from Casino databases that can be used to detect game abuse.
Requires Python 3.10.8, MySQL Server 5.7
### Usage

1. Insert ssh keys into ./credentials and create vars.cfg
2. Install requirements using `pip -r requirements.txt`
3. Start MySQL Server 5.7 on port 3307
4. Run tables.sql
5. Run script using `python main.py`

### Table Structures

```
CREATE TABLE IF NOT EXISTS win_history (
    aggregated_at DATE NOT NULL,
    gp_id VARCHAR(24) NOT NULL,
    game_code VARCHAR(64) NOT NULL,
    total_bet FLOAT DEFAULT NULL,
    total_win FLOAT DEFAULT NULL,
    profit FLOAT DEFAULT NULL,
    rtp FLOAT DEFAULT NULL,
    bet_count INT(11) DEFAULT NULL,
    PRIMARY KEY (aggregated_at , gp_id , game_code),
    UNIQUE KEY aggregation_key (aggregated_at , gp_id , game_code)
);

CREATE TABLE IF NOT EXISTS account_details (
    gp_id VARCHAR(24) NOT NULL PRIMARY KEY,
    nickname VARCHAR(64));

CREATE TABLE IF NOT EXISTS abusers (
    gp_id VARCHAR(24) NOT NULL PRIMARY KEY);

CREATE VIEW coalesced_history AS 
	(SELECT 
	    aggregated_at,
	    gp_id,
	    ROUND(SUM(total_bet), 2) AS total_bet,
	    ROUND(SUM(total_win), 2) AS total_win,
	    ROUND(SUM(profit), 2) AS profit,
	    ROUND(SUM(total_win)/SUM(total_bet), 2) AS rtp,
	    SUM(bet_count) AS bet_count
	FROM
	    win_history
	GROUP BY gp_id, aggregated_at
	ORDER BY gp_id, aggregated_at DESC);
	
CREATE VIEW coalesced_stats AS 
	(SELECT 
	    gp_id,
	    SUM(IF(rtp >= 1, 1, 0)) AS num_days_won,
	    COUNT(*) AS total_days,
	    SUM(IF(rtp >= 1, 1, 0)) / COUNT(*) AS win_percentage,
	    ROUND(SUM(profit), 2) AS profit,
	    SUM(bet_count) AS bet_count
	FROM
	    coalesced_history
	GROUP BY gp_id);
 ```
	
