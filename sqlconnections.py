
import mysql.connector as sql
from mysql.connector import Error


        
commands = [
    '''
    USE sakila;
    SELECT * FROM actor;
    ''',
    '''
    USE sakila;
    SELECT * FROM actor WHERE actor_id < 10;
    '''
]  


connection_config_dict = {
    'user': 'root',
    'password': 'adelante5225',
    'host': '127.0.0.1',
}


try:
    connection = sql.connect(**connection_config_dict)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info, '\n')
        cursor = connection.cursor()
        
        for command in commands:
            for result in cursor.execute(command, multi=True):
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(
                    result.statement))
                    print(result.fetchall())
                else:
                    print("Number of rows affected by statement '{}': {}".format(
                    result.statement, result.rowcount), '\n')
        record = cursor.fetchall()
        
except Error as e:
    print("Error while connecting to MySQL", e, '\n')

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed", '\n')
        
        