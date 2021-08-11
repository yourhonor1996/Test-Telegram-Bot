
import mysql.connector as sql
from mysql.connector import Error
from config import settings


commands = []
database_query_filename = 'queries.sql'
dirname = settings.BASE_DIR / database_query_filename

with open(dirname, 'r') as file:
    commands.append(file.read())

connection_config_dict = {
    'user': 'root',
    'password': 'adelante5225',
    'host': '127.0.0.1',
}

def run_sql_command(commands):
    try:
        connection = sql.connect(**connection_config_dict)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info, '\n')
            cursor = connection.cursor()
            records = []
            for command in commands:
                for result in cursor.execute(command, multi=True):
                    if result.with_rows:
                        print(f"Statement executed: {result.statement}")
                        # print(result.fetchall())
                        records += result.fetchall()
                    # else:
                        # print("Number of rows affected by statement '{}': {}".format(
                        # result.statement, result.rowcount), '\
            # return cursor.fetchall()
            print(records)
    except Error as e:
        print("Error while connecting to MySQL", e, '\n')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed", '\n')
        

def main():
    run_sql_command(commands)
    
    
if __name__ == '__main__':
    main()