
# Searchlight

Retrieves data from Casino databases that can be used to detect game abuse.
Requires Python 3.10.8, MySQL Server 5.7

### Usage

1. Insert ssh keys into ./credentials and create vars.cfg
2. Install requirements using `pip -r requirements.txt`
3. Start MySQL Server 5.7 on port 3307
4. Run tables.sql
5. Run script using `python main.py`

### Abuser Detection Method

Abusers are found using the user's moving average of RTP. If a user has all MAs > 1, the gp_id is flagged.
For examples with N = 5 and M = 6 for a total of 10 days examined:

```
Flagged User (min(moving_averages) == 1.07)
GP ID - YUiWs219nwSqchbdLHdpwWt1 
Data Set - [1.31, 0.52, 1.21, 1.2, 1.69, 0.86, 1.95, 1.05, 0.8, 0.7] 
Moving Averages - [1.19, 1.1, 1.38, 1.35, 1.27, 1.07]
```

```
Not Flagged User (min(moving_averages) == 0.8)
GP ID - ZZ9Qua4FTMl76UL7xLo5efrF 
Data Set - [0.65, 1.33, 1.16, 2.0, 0.67, 0.51, 0.73, 0.49, 1.61, 1.07] 
Moving Averages - [1.16, 1.13, 1.01, 0.88, 0.8, 0.88]
```

### Database Table Structures

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
	
