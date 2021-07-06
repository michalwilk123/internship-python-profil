import csv
import os
from .base_handler import Handler
from ..log_entry import LogEntry
from dataclasses import asdict
from datetime import datetime
from typing import List


class CSVHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def add_log(self, log: LogEntry) -> None:
        # Unfortunatly we have to open and close file per each log action
        with open(self.__filename, 'a+') as csv_file:
            log_writer = csv.DictWriter(csv_file, fieldnames=LogEntry.get_field_names())

            # looking for header
            # if not csv.Sniffer().has_header(csv_file.read()):
            #     log_writer.writeheader()
            if not os.stat(self.__filename).st_size:
                log_writer.writeheader()
            
            log_writer.writerow(asdict(log))
            
                
                
    def get_base_form(self) -> List[LogEntry]:
        with open(self.__filename, 'r') as csv_file:
            # looking for header
            log_writer = csv.DictReader(csv_file, fieldnames=LogEntry.get_field_names())
            # generating datetime obj from datetime.now strign
            log_entries = []

            for row in log_writer:
                # this looks bad but and i do not know how to 
                # make this part better
                log_entries.append(
                    LogEntry(
                        date = datetime.fromisoformat(row["date"]),
                        level=row["date"],
                        msg=row["msg"],
                    )
                )

        return log_entries