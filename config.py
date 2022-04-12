import configparser
import os
class config:
    @staticmethod
    def getConfig(configName,sections='default'):
        filename=configName+".conf"
        filepath = os.path.dirname(os.path.dirname(__file__))+"/xlib/config/"+filename #
        config = configparser.ConfigParser()
        config.read(filepath)
        config=config.items(sections)
        config= {key: value for key, value in config for kv in config}
        return config