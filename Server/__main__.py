from Common import setup_logging
from Server import MainService

setup_logging(__file__)

if __name__ == "__main__":
    MainService().start()
