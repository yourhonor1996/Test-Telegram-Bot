
import logging
import mysql.connector as sql
from mysql.connector import Error
from config import settings
from utility.util import logger


commands = []
database_query_filename = 'queries.sql'
dirname = settings.QUERIES_DIRNAME / database_query_filename

with open(str(dirname), 'r') as file:
    commands.append(file.read())

def run_sql_command(commands: "str | list[str]"):
    if type(commands) is str:
        commands = [commands]
    
    try:
        connection = sql.connect(**settings.MYSQL_CONNECTION)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info, '\n')
            logger('Connected to MySQL Server version')
            cursor = connection.cursor()
            records = []
            for command in commands:
                for result in cursor.execute(command, multi=True):
                    if result.with_rows:
                        # print(f"Statement executed: {result.statement}")
                        logger(f"Statement executed: {result.statement}")
                        # print(result.fetchall())
                        records += result.fetchall()
                    # else:
                        # print("Number of rows affected by statement '{}': {}".format(
                        # result.statement, result.rowcount), '\
            # return cursor.fetchall()
            print(records)
    except Error as e:
        logger(f"Error while connecting to MySQLL {e}\n")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger("MySQL connection is closed.")
        

def main():
    run_sql_command(commands)
    
    
if __name__ == '__main__':
    main()