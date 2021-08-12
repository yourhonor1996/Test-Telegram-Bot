
# from src.utility.mysql_util import run_sql
from src.utility.mysql_util import SQLRunner
from src.config import settings
from src.utility.util import classproperty

class QueryAgent():

    def __init__(self, tablename) -> None:
        self.tablename = tablename
        self.database_name = settings.DATABASE_NAME
        self.use_database = f"USE {self.database_name};"
        self.sqlrunner = SQLRunner()
        # self.sqlrunner.run_sql(self.use_database, False)
    
    def all(self):
        command = \
        f'''
        SELECT * FROM {self.tablename};
        '''
        return self.sqlrunner.run_sql(command)
    
    def filter(self, filter_type, **kwargs):
        pass
    def create(self):
        pass
        
    def save(self):
        pass
    
    
    
class BaseModel():
    
    def __init__(self):
        pass

    @classproperty
    def objects(cls):
        return QueryAgent(cls.table_name)

    @classproperty
    def table_name(cls, name= None):
        if not name:
            class_name = cls.__name__
            if class_name.endswith('Model'):
                return class_name[:-5].lower()
            else:
                return class_name.lower()
        else:
            return name
    
        
        
        
class ActorModel(BaseModel):
    pass        
            
            
# run this file from manage.py for test of the self written orm system
# print(ActorModel.objects.all())