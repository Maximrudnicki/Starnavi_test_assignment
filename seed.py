import psycopg2

from config.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


def execute_sql_file():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )

    try:
        with conn.cursor() as cursor:
            with open("./seed.sql", "r") as sql_file:
                sql_commands = sql_file.read()

            cursor.execute(sql_commands)

        conn.commit()
        print("SQL script executed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()


execute_sql_file()
