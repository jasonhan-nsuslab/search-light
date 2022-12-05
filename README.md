# Searchlight
Retrieves data from Casino databases that can be used to detect game abuse.
Requires Python 3.10.8, MySQL Server 5.7
### Usage

1. Insert ssh keys into ./credentials and create vars.cfg
2. Install requirements using `pip -r requirements.txt`
3. Start MySQL Server 5.7 on port 3307
4. Run tables.sql
5. Run script using `python main.py`

### Notes
 - Monetary amounts and RTP are rounded to 2 decimals, which is a possible source of error
	 - E.g. RTP Values less than 100 may be seen as >= 100, such as 99.51

	
