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
            return event_class(**self.data)
        else:
            raise ValueError(f"Unknown event type: {self.event_type}")
