class Database:
    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn