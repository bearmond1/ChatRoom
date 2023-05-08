import json
from jsonschema import validate
import os



config_schema = {
    "type": "object",
    "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer"},
        "password": {"type": "string"}
    },
    "required":["host","port","password"],
}


class Config():
    def __init__(self,host,port,password):
        self.password = password
        self.host = host
        self.port = port


def get_config() -> Config:
    default_config = Config("localhost",8888,"")
    if os.path.isfile("config.json"):
        with open("config.json") as file_config:
            try:
                config = json.loads(file_config.read())
                validate(instance=config, schema=config_schema)
                print("Config successfully validated")
                config = Config(host = config["host"],port= config["port"], password= config["password"])
                return config
            except Exception as e:
                print(f"exception, {e.__dict__}")
                return default_config
    else:
        return default_config