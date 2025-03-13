import sqlite3

def setup_database(database_path, blacklist_path):
    database_conn = sqlite3.connect(database_path)
    blacklist_conn = sqlite3.connect(blacklist_path)
    database_cursor = database_conn.cursor()
    blacklist_cursor = blacklist_conn.cursor()

    database_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            School TEXT NOT NULL,
            Title TEXT UNIQUE NOT NULL,
            Title_Simplified TEXT UNIQUE NOT NULL,
            Link TEXT NOT NULL,
            Post_Date TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (School, Link)
        )
        """
    )

    blacklist_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS blacklist (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            School TEXT NOT NULL,
            Title TEXT UNIQUE NOT NULL,
            Title_Simplified TEXT UNIQUE NOT NULL,
            Link TEXT NOT NULL,
            Post_Date TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (School, Link)
        )
        """
    )

    database_conn.commit()
    blacklist_conn.commit()
    
    return database_conn, database_cursor, blacklist_conn, blacklist_cursor
