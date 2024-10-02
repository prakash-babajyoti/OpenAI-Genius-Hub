from flask import Flask
import threading
import logging

from src.rest_service.routes.translate import translate_bp

# Initialize Flask app and logger
app = Flask(__name__)
logger = logging.getLogger(__name__)

# Register the Blueprint
app.register_blueprint(translate_bp)

def run_flask():
    """
    Function to run the Flask app in a separate thread.
    """
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def start_flask_in_thread():
    """
    Starts the Flask server on a new thread.
    """
    logger.info("Starting Flask server in a separate thread.")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Daemon thread will close when the main thread closes
    flask_thread.start()

if __name__ == "__main__":
    run_flask()
