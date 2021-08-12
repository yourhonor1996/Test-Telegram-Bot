
from src.utility.mysql_util import run_sql
from src.config import settings
from src.utility.util import classproperty

class QueryAgent():

    def __init__(self, tablename) -> None:
        self.tablename = tablename
        self.database_name = settings.DATABASE_NAME
        self.use_database = f"USE {self.database_name};"
    
    def all(self):
        command = self.use_database + \
        f'''
        SELECT * FROM {self.tablename}
        WHERE actor_id < 10;
        '''
        return run_sql(command)
    
    def filter(self, **kwargs):
        ...
        
    def create(self):
        ...
        
    def save(self):
        ...
    
    
    
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
            
            
print(ActorModel.objects.all())