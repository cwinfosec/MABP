import logging
#from sys import argv

#log_filename = argv[1]

def log(log_filename):
    logging.basicConfig(filename='./logs/' + log_filename, format='%(asctime)s:[%(levelname)s]:%(message)s')
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    log(log_filename)