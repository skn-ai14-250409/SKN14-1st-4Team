import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()
CONFIG_HOST = os.getenv('CONFIG_HOST')
CONFIG_USER = os.getenv('CONFIG_USER')
CONFIG_PASSWORD = os.getenv('CONFIG_PASSWORD')
CONFIG_PORT = os.getenv('CONFIG_PORT')
USER_TO_GRANT = os.getenv('USER_TO_GRANT')

config = {
    'host': CONFIG_HOST,
    'user': CONFIG_USER,  
    'password': CONFIG_PASSWORD, 
    'port': CONFIG_PORT
}


db_name = 'ev_charger_db'
user_to_grant = USER_TO_GRANT  

def create_database_and_grant():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE DATABASE IF NOT EXISTS {db_name}
            DEFAULT CHARACTER SET utf8mb4
            DEFAULT COLLATE utf8mb4_general_ci;
        ''')
        print(f"Database '{db_name}' created or already exists.")

        cursor.execute(f'''
            GRANT ALL PRIVILEGES ON {db_name}.* TO '{user_to_grant}'@'%';
        ''')
        print(f"Granted all privileges on '{db_name}' to user '{user_to_grant}'.")


        cursor.execute('FLUSH PRIVILEGES;')
        print("Flushed privileges.")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    create_database_and_grant()
