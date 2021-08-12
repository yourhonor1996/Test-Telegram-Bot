import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)

def logger(message:str, *args, **kwargs):
    return logging.log(logging.INFO, message, *args, **kwargs)

class classproperty(object):
    '''Converts a class method into a class property. However this property cannot be set it can only be called.'''
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
    
    