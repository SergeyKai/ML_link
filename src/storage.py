from dataclasses import dataclass


class Text:
    TEXT: str = None
    CHARS_COUNT: int = None
    ROWS_COUNT: int = None
    DATA: list = None
    FILE_NAME: str = None
    LANGUAGE: str = None

    @classmethod
    def save_data(
            cls,
            text,
            chars_count,
            row_count,
            data,
            filename,
            lang: str,
    ):
        cls.TEXT = text
        cls.CHARS_COUNT = chars_count
        cls.ROWS_COUNT = row_count
        cls.DATA = data
        cls.FILE_NAME = filename
        cls.LANGUAGE = lang


@dataclass
class FirstFile(Text):
    pass


@dataclass
class SecondFile(Text):
    pass
