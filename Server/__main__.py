from Common import setup_logging
from Server import Server

setup_logging(__file__)

if __name__ == "__main__":
    Server().run()
