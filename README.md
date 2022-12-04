# Searchlight
Retrieves data from Casino databases that can be used to detect game abuse.
Requires Python 3.10.8, MySQL Server 5.7
### Usage

Install requirements using `pip -r requirements.txt`

Start MySQL Server 5.7 on port 3307 and run tables.sql.

Run script using `python main.py`
### Notes
 - Monetary amounts and RTP are rounded to 2 decimals, which is a possible source of error
	 - E.g. RTP Values less than 100 may be seen as >= 100, such as 99.51

	