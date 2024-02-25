import constants
from typing import TextIO
from datetime import datetime
import codecs


class _GameMessageHandler:
    buffer: list[str]

    def __init__(self):
        self.buffer = []

    def push(self, message: str):
        self.buffer.append(message)
        if len(self.buffer) > constants.GameMessageBufferMaxLimit:
            self.buffer = self.buffer[len(self.buffer) - constants.GameMessageBufferMaxLimit:]

    def retrieve(self) -> str:
        return self.buffer[-1]


class _EventLogHandler:
    log_file: TextIO

    def __init__(self):
        log_file_name: str = datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".log"
        self.log_file = codecs.open(log_file_name, mode='a', encoding='utf-8')

    def __del__(self):
        if not self.log_file.closed:
            self.log_file.close()

    def push(self, message: str):
        print(message, file=self.log_file)


class LogWriter:
    game_message_handler: _GameMessageHandler
    event_log_handler: _EventLogHandler

    def __init__(self):
        self.game_message_handler = _GameMessageHandler()
        self.event_log_handler = _EventLogHandler()

    def write_player_log(self, message_name: str, *args):
        message: str = constants.PlayerVisiblePrompts[message_name].format(*args)
        self.game_message_handler.push(message)
        self.event_log_handler.push(message)

    def write_internal_log(self, message_name: str, *args):
        message: str = constants.InternalLogPrompts[message_name].format(*args)
        self.event_log_handler.push(message)

    def retrieve(self) -> str:
        return self.game_message_handler.retrieve()