import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)

def logger(message:str, *args, **kwargs):
    return logging.log(logging.INFO, message, *args, **kwargs)