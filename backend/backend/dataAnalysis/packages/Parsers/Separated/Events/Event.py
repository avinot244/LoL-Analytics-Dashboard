class Event() :
    def __init__(
        self, 
        event_type : str,
        data : dict
    ):
        super().__init__()
        self.event_type = ''.join(word.capitalize() for word in event_type.split('_')) + 'Event'
        self.data = data
        
    def getEvent(self):
        event_class = globals().get(self.event_type)
        if event_class:
            filtered_dict : dict = {k: v for k, v in self.data.items() if k in event_class.__annotations__}
            return event_class(**filtered_dict)
        else:
            raise ValueError(f"Unknown event type: {self.event_type}")
