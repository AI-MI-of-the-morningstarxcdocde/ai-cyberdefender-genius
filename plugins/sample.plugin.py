from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel
from plugins.plugin import Plugin, PluginMessage, StatusLevel


class SamplePlugin(Plugin):
    def __init__(self):
        self.active = False
    
    def name(self):
        return "Sample Plugin"
    
    def description(self) -> str:
        return "A simple example plugin."
    
    def widget(self) -> QWidget:
        return QLabel("Hello from Sample Plugin!")
    
    def report_status(self) -> list[PluginMessage]:
        return [PluginMessage(StatusLevel.OK, "OK", "Everything is fine!")]
    
    def start(self) -> Optional[PluginMessage]:
        self.active = True
        print("Sample plugin started!")

        return PluginMessage(StatusLevel.OK, "Started", "Successfully started.")
    
    def stop(self) -> None:
        self.active = False
        print("Sample plugin stopped!")