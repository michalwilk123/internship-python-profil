from my_logger import (
    JsonHandler,
    CSVHandler,
    SQLLiteHandler,
    FileHandler,
    ProfilLogger,
    ProfilLoggerReader,
)

json_handler = JsonHandler("logs.json")
csv_handler = CSVHandler("logs.csv")
sql_handler = SQLLiteHandler("logs.sqlite")
file_handler = FileHandler("logs.txt")

logger = ProfilLogger(
    handlers=[json_handler, csv_handler, sql_handler, file_handler]
)
logger.set_log_level("INFO")
logger.info("Some info message")
logger.warning("Some warning message")
logger.debug("Some debug message")
logger.critical("Some critical message")
logger.error("Some error message")
# The logs are stores in logs.json, logs.csv, logs.sqlite and logs.txt

# -----
# Logs are being read form the logs.json file
log_reader = ProfilLoggerReader(handler=json_handler)
log_reader.find_by_text(
    "info message"
)  # returns list of LogEntry that contains message: "Some info message"
log_reader.find_by_regex(f"[a-g]{1} message")
