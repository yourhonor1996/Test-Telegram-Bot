import mysql.connector as sql
from mysql.connector import Error
from src.config import settings
from src.utility.util import logger




def load_commands(query_name:str):
    '''loads the commands from a certain query filename in the queries folder'''
    dirname = settings.QUERIES_DIR / f'{query_name}.sql'

    with open(str(dirname), 'r') as file:
        commands = file.read()
    return commands

def run_sql(commands: "str | list[str]"):
    if type(commands) is str:
        commands = [commands]
    
    try:
        connection = sql.connect(**settings.MYSQL_CONNECTION)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            logger('Connected to MySQL Server version')
            cursor = connection.cursor()
            records = []
            for command in commands:
                for result in cursor.execute(command, multi=True):
                    if result.with_rows:
                        logger(f"Statement executed: {result.statement}")
                        records += result.fetchall()
            # return records
            if records:
                print(records)
    except Error as e:
        logger(f"Error while connecting to MySQLL {e}\n")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger("MySQL connection is closed.")


        

def main():
    run_sql(load_commands('queries'))
    
    
if __name__ == '__main__':
    main()
    
    
