import logging

def setup_logging():
    logging.basicConfig(
        level=logging.WARNING, # Set the logging level
        format='%(asctime)s - %(levelname)s - %(message)s', # Define log message format
        handlers=[
            logging.StreamHandler() # Output logs to console
            # logging.FileHandler('game.log') # Uncomment to also log to a file
        ]
    )
    logging.info("Logging setup complete.")
