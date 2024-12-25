import importlib
import json

class Event:
    def __init__(
        self, 
        event_type: str, 
        data: dict
    ):
        super().__init__()
        # Convert event_type to PascalCase and append "Event"
        self.event_type = ''.join(word.capitalize() for word in event_type.split('_')) + 'Event'
        self.data = data

    def getEvent(self):
        # Module path without the class name
        module_path = "dataAnalysis.packages.Parsers.Separated.Events.EventTypes"

        try:
            # Dynamically import the module
            module = importlib.import_module(module_path)
            
            # Dynamically get the class
            event_class = getattr(module, self.event_type)
            
            # Filter the data to match the class's annotations
            filtered_data = {
                k: v for k, v in self.data.items() if k in event_class.__annotations__
            }
            
            # Return an instance of the event class
            return event_class(**filtered_data)
        
        except ModuleNotFoundError:
            print(f"Module '{module_path}' not found!")
            raise
        
        except AttributeError:
            print(f"Class '{self.event_type}' not found in module '{module_path}'!")
            raise
        
        except TypeError as e:
            print(json.dumps(self.data, indent=4))
            print(f"Error initializing class '{self.event_type}': {e}")
            raise
