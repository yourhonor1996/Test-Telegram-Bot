import mysql.connector as sql
from mysql.connector import Error, connect
from mysql.connector import connection
from src.config import settings
from src.utility.util import logger


class SQLRunner():
    
    def __init__(self):
        self.open_connection()
    
    def __del__(self):
        self.close_connection()

    def open_connection(self, **conn_settings):
        if not conn_settings:
            self.connection = sql.connect(**settings.MYSQL_CONNECTION)
        else:
            self.connection = sql.connect(**conn_settings)

        self.connection_id = self.connection.connection_id
        db_Info = self.connection.get_server_info()
        logger(f'Connected to MySQL Server version. Database info: {db_Info}')

    def get_connection(self):
        return self.connection
    
    def close_connection(self):
        if self.connection.is_connected() and self.connection_id == self.connection.connection_id: 
                self.connection.cursor.close()
                self.connection.close()
                logger("MySQL connection is closed.")
    
            
        
    
    def load_commands(self, query_name:str):
        '''loads the commands from a certain query filename in the queries folder'''
        dirname = settings.QUERIES_DIR / f'{query_name}.sql'

        with open(str(dirname), 'r') as file:
            commands = file.read()
        return commands

    def run_sql(self, commands: "str | list[str]", close_conn= True):
        """Runs sql commands or a list of sql commands and returns result
        if the command returns anything
        
        #TODO make this function so that it can fetch larg ammounts of data from the data base (useing fetchone() and a generator)

        Args:
            commands (str | list[str]): [The sql command or a list of sql commands to run. if a list of 
            commansd are give, then it will return a list[list] of results for each command in the commandlist.]
        """
        
        if type(commands) is str:
            commands = [commands]
        
        records = []
        try:
            # connection = sql.connect(**settings.MYSQL_CONNECTION)
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                for command in commands:
                    for result in cursor.execute(command, multi=True):
                        if result.with_rows:
                            logger(f"Statement contained rows: {result.statement}")
                            if len(commands) > 1:
                                records += [result.fetchall()]
                            else:
                                records += result.fetchall()
                        else:
                            logger(f"Statement DID NOT contain any rows: {result.statement}")
                            
                # print(records)
                return records
        except Error as e:
            logger(f"Error while connecting to MySQLL {e}\n")
        finally:
            if close_conn:
                # self.close_connection()
                if self.connection.is_connected():
                    self.connection.cursor().close()
                    self.connection.close()
                    logger("MySQL connection is closed.")
            else:
                logger("MySQL connection DID NOT CLOSE. Waiting for other commands ...")
