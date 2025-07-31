from Common import global_config, setup_logging
from Server import Server

setup_logging(__file__)

if __name__ == "__main__":
    config = global_config["server"]["api"]
    Server(config=config).run()
