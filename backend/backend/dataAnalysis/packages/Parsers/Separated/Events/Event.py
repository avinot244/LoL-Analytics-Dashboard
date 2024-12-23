import importlib


class Event():
    def __init__(self, event_type : str):
        super().__init__()
        self.event_type = event_type
        
    def getEvent(self):
        self.event_type = ''.join(word.capitalize() for word in self.event_type.split('_')) + 'Event'
        module_name = f"dataAnalysis.packages.Parsers.Events.EventTypes.{self.event_type}"
        try:
            module = importlib.import_module(module_name)
            event_class = getattr(module, self.event_type)
        except ModuleNotFoundError:
            event_class = None
            print(f"Event Type {self.event_type} not found in EventTypes")
        return event_class