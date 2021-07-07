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

# Logs are being read form the logs.json file
log_reader = ProfilLoggerReader(handler=json_handler)
matches_text = log_reader.find_by_text("info message")
# returns list of LogEntry that contains message: "Some info message"
# orginal regex will not match anything!
matches_regex = log_reader.find_by_regex(".*[a-g]{1} message")

groups_level = log_reader.groupby_level()

print("\n|======== FILTER BY TEXT ==========|")
print(f"{matches_text=}")
print("\n|======== FILTER BY REGEX =========|")
print(f"{matches_regex=}")
print("\n|======== GROUPING BY LEVEL =======|")
for g in groups_level:
    print(f"{g} : {groups_level[g]}")
