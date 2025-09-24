import logging, sys, json
from config import LOG_JSON, LOG_LEVEL

def get_logger(name=__name__):
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    if LOG_JSON:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "time": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            data["exc"] = self.formatException(record.exc_info)
        return json.dumps(data)

if __name__ == "__main__":
    log = get_logger("logger_setup_test")
    log.info("Logger self-test successful")
