from abc import ABC, abstractmethod


class JsonLogger(ABC):
    @abstractmethod
    def log_message(self, message: str) -> None:
        pass


class XmlLogger:
    def log(self, xml_message: str) -> None:
        print(xml_message)


class LoggerAdapter(JsonLogger):
    def __init__(self, xml_logger: XmlLogger) -> None:
        self.xml_logger = xml_logger

    def log_message(self, message: str) -> None:
        self.xml_logger.log(message)


logger = LoggerAdapter(XmlLogger())
logger.log_message("<message>hello</message>")
