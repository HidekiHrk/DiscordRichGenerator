from pcw import Config as pConfig

class Config(pConfig):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = pConfig.__new__(cls)
            cls.__instance.__initialized = True
        return cls.__instance

    def __init__(self, filename="config.json"):
        self.__initialized = False
        super().__init__(filename)
