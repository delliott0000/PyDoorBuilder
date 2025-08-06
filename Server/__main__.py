from Common import PostgresConfig, ServerAPIConfig, global_config, setup_logging
from Server import Server

setup_logging(__file__)

if __name__ == "__main__":
    config = ServerAPIConfig(**global_config["server"]["api"])
    db_config = PostgresConfig(
        **global_config["postgres"] | global_config["server"]["postgres"]
    )

    server = Server(config=config, db_config=db_config)
    server.run()
