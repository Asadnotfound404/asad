# asad
A personal ML library by Asad

1. First package is of Logging through the my personal Machine learning projects
    we have toh import this git repo using this command "git+https://github.com/Asadnotfound404/asad.git"
    
from logging_core import Logger Factory
# logger.py
logger = LoggerFactory.get_logger(__name__, level="DEBUG")

logger.info("INFO test")
logger.debug("DEBUG test")
logger.warning("WARNING test")
logger.error("ERROR test")
