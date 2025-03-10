import sys
import main as main_module
import target
import config

def main():
    try:
        database_conn, database_cursor, blacklist_conn, blacklist_cursor = main_module.setup_database(
            'data/database.db', 'data/blacklist.db'
        )

        for site in target.sites:
            events = main_module.get_events(site, config.headers)
            for school, title, title_simplified, link in events:
                try:
                    database_cursor.execute(
                        """
                        INSERT INTO events (School, Title, Title_Simplified, Link)
                        VALUES (?, ?, ?, ?)
                        """,
                        (school, title, title_simplified, link)
                    )
                except Exception:
                    print(f"資料已存在: {school, title}")

        database_conn.commit()
        database_conn.close()

    except Exception as e:
        print(f"未成功連接到 Database: {e}")

if __name__ == "__main__":
    if "--nogui" in sys.argv:
        main()
    else:
        main_module.launch_gui()
