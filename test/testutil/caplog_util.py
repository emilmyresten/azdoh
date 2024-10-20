from logging import LogRecord


def pprint(records: list[LogRecord]):
    for record in records:
        print(f"{record.levelname}: {record.message}")
