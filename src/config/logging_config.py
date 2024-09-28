import logging
import logging.config

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',  # Log to file
        filemode='a'
    )

# You can also define more advanced configurations here
