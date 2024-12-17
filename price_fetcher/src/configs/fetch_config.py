import yaml
import os, logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)


class YamlParser:
    """
    This function will help to read and return data of the files.
    This act as common utility for file read
    """
    conf_path = "./src/configs"

    @classmethod
    def read_config(cls, config_file: str, conf_path_override = None) -> dict:
        if conf_path_override:
            cls.conf_path = conf_path_override
        logging.info(f"reading config file {os.path.join(cls.conf_path,config_file)}")
        with open(os.path.join(cls.conf_path,config_file)) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return config
