import time
import sqlite3
import datetime

"""DB interface for comunicating with sqlite3"""


class DBError(Exception):
    pass


class DB(object):
    """
    Public methods:
        add_request(): add a request to the database (requests table).
        get_user(): get user info from the database (users table).
        add_user(): add a user to the database (users table).
        update_user(): update a user on the database (users table).
    Exceptions:
         DBError: Something went wrong when trying to connect/interact
         with the database.
    """

    def __init__(self, dbname):
    	"""Create a new db object.
        :param: dbname (string) the path of the database.
        """
        self.dbname = dbname


    def connect(self):
        """ """
        try:
            self.con = sqlite3.connect(self.dbname)
            self.con.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise DBError("%s" % str(e))

    def add_request(self):
        """Add a request to the database.
        For now we just count the number of requests we have received so far.
        """
        try:
            with self.con:
                cur = self.con.cursor()
                cur.execute("SELECT counter FROM requests WHERE id = 1")
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE requests SET counter=? WHERE id=?",
                                (row['counter']+1, 1))
                else:
                    cur.execute("INSERT INTO requests VALUES(?, ?)", (1, 1))
        except sqlite3.Error as e:
            raise DBError("%s" % str(e))

    def get_user(self, user, service):
        """Get user info from the database.
        :param: user (string) unique (hashed) string that represents the user.
        :param: service (string) the service related to the user (e.g. SMTP).
        :return: (dict) the user information, with fields as indexes
                 (e.g. row['user']).
        """
        try:
            with self.con:
                cur = self.con.cursor()
                cur.execute("SELECT * FROM users WHERE id =? AND service =?",
                            (user, service))

                row = cur.fetchone()
                return row
        except sqlite3.Error as e:
            raise DBError("%s" % str(e))

    def add_user(self, user, service, blocked):
        """Add a user to the database.
        We add a user with one 'times' and the current time as 'last_request'
        by default.
        :param: user (string) unique (hashed) string that represents the user.
        :param: service (string) the service related to the user (e.g. SMTP).
        :param: blocked (int) one if user is blocked, zero otherwise.
        """
        try:
            with self.con:
                cur = self.con.cursor()
                cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                            (user, service, 1, blocked, str(time.time())))
        except sqlite3.Error as e:
            raise DBError("%s" % str(e))

    def update_user(self, user, service, times, blocked):
        """Update a user on the database.
        We update the user info with the current time as 'last_request'.
        :param: user (string) unique (hashed) string that represents the user.
        :param: service (string) the service related to the user (e.g. SMTP).
        :param: times (int) the number of requests the user has made.
        :param: blocked (int) one if user is blocked, zero otherwise.
        """
        try:
            with self.con:
                cur = self.con.cursor()
                cur.execute("UPDATE users SET times =?, blocked =?,"
                            " last_request =? WHERE id =? AND service =?",
                            (times, blocked, str(time.time()), user, service))
        except sqlite3.Error as e:
            raise DBError("%s" % str(e))
