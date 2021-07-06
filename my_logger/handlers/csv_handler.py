import csv
import os
from .base_handler import Handler
from ..log_entry import LogEntry
from dataclasses import asdict
from datetime import datetime
from typing import List


class InvalidCSVFileException(Exception):
    ...


class InvalidCSVHeaderException(Exception):
    ...


class CSVHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def add_log(self, log: LogEntry) -> None:
        # Unfortunatly we have to open and close file per each log action
        with open(self.__filename, "a+") as csv_file:
            log_writer = csv.DictWriter(
                csv_file, fieldnames=LogEntry.get_field_names()
            )

            # looking for header
            if not os.stat(self.__filename).st_size:
                log_writer.writeheader()

            log_writer.writerow(asdict(log))

    def get_base_form(self) -> List[LogEntry]:
        with open(self.__filename, "r") as csv_file:
            log_reader = csv.DictReader(
                csv_file, fieldnames=LogEntry.get_field_names()
            )
            log_entries = []

            # testing header
            if None in next(log_reader).keys():
                raise InvalidCSVHeaderException

            for idx, row in enumerate(log_reader):
                # this looks bad but and i do not know how to
                # make this part better
                if None in row.values():
                    raise InvalidCSVFileException(
                        f"Given csv file ({self.__filename}) is invalid! "
                        f"Line {idx+1}: {row} does not contain all nessesary fields!"
                    )

                log_entries.append(
                    LogEntry(
                        date=datetime.fromisoformat(row["date"]),
                        level=row["level"],
                        msg=row["msg"],
                    )
                )

        return log_entries
