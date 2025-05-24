from abc import ABC, abstractmethod
from optparse import Option
from typing import Optional
from PySide6.QtWidgets import QWidget
from enum import Enum, auto

from utils.prefix_stdout import prefix_stdout

class StatusLevel(Enum):
    OK = auto()         # Running normally
    HINT = auto()       # Hint available to improve functionality
    WARNING = auto()    # Something needs attention
    ERROR = auto()      # Something failed

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if not isinstance(other, StatusLevel):
            return NotImplemented
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, StatusLevel):
            return NotImplemented
        return self.value > other.value

class PluginMessage:
    def __init__(self, level: StatusLevel, title: str, message: str):
        self.level = level
        self.title = title
        self.message = message

    def __lt__(self, other):
        if not isinstance(other, PluginMessage):
            return NotImplemented
        return self.level < other.level

    def __gt__(self, other):
        if not isinstance(other, PluginMessage):
            return NotImplemented
        return self.level > other.level

class Plugin(ABC):
    active: bool

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def start(self) -> Optional[PluginMessage]:
        """
        Start the plugin and optionally return a status message.
        """

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def widget(self) -> QWidget:
        """Return the main widget/view for this plugin."""
        pass

    @abstractmethod
    def report_status(self) -> list[PluginMessage]:
        pass

    def start_plugin(self) -> Optional[PluginMessage]:
        """
        Starts the plugin. Wraps the output into `prefix_stdout` to show plugin name before each line.
        """
        with prefix_stdout(f"[PLUGIN {self.name()}] "):
            self.start()

    def stop_plugin(self):
        """
        Stops the plugin. Wraps the output into `prefix_stdout` to show plugin name before each line.
        """
        with prefix_stdout(f"[PLUGIN {self.name()}] "):
            self.stop()