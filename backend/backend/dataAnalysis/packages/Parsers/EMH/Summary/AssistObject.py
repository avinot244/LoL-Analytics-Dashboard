class AssistObject:
    def __init__(
        self,
        idPlayerKilling : str,
        idPlayerAssisting : str,
        killAssistsReceived : int
    ):
        self.idPlayerKilling = idPlayerKilling
        self.idPlayerAssisting = idPlayerAssisting
        self.killAssistsReceived = killAssistsReceived