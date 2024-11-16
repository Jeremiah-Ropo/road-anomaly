from dotenv import load_dotenv
import os
import threading
from flask_cors import CORS
from app.src import create_app
from app.src import batch_prediction  # Import the batch_prediction module

# Load environment variables
load_dotenv()
debug_mode = os.getenv("DEBUG")

# Initialize Flask app
app = create_app()
CORS(app)

def start_batch_prediction():
    # Start the batch prediction job in the background
    batch_prediction.main()

if __name__ == '__main__':
    # Start the batch prediction in a separate thread
    threading.Thread(target=start_batch_prediction, daemon=True).start()
    
    # Run the Flask app
    app.run(debug=debug_mode)
