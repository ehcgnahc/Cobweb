import main as main_module
import threading
import schedule
import time
import requests
import target
import config

database_path = 'data/database.db'
blacklist_path = 'data/blacklist.db'

def update_data():
    try:
        database_conn, database_cursor, blacklist_conn, blacklist_cursor = main_module.setup_database(
            database_path, blacklist_path
        )

        for site in target.sites:
            try:
                events = main_module.get_events(site, config.headers)
            except requests.exceptions.Timeout:
                print(f"爬取 {site['school']} 時間逾時，跳過。")
                continue
            except requests.exceptions.RequestException as e:
                print(f"爬取 {site['school']} 發生連線錯誤：{e}，跳過。")
                continue
            
            for school, title, title_simplified, link in events:
                try:
                    database_cursor.execute(
                        """
                        INSERT INTO events (School, Title, Title_Simplified, Link)
                        VALUES (?, ?, ?, ?)
                        """,
                        (school, title, title_simplified, link)
                    )
                    print(f"已新增 {school} - {title} ({title_simplified})")
                except Exception:
                    continue
            
        database_conn.commit()
        database_conn.close()

    except Exception as e:
        print(f"未成功連接到 Database: {e}")

def check_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    update_data()
    schedule.every(1).hours.do(update_data)
    threading.Thread(target=check_schedule, daemon=True).start()
    
    main_module.launch_gui(
        database_path, blacklist_path
    )