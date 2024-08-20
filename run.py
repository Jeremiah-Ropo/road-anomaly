from dotenv import load_dotenv
import os
from app.src import create_app
load_dotenv()

# Access environment variables
debug_mode = os.getenv("DEBUG")


app = create_app()

if __name__ == '__main__':
    app.run(debug=debug_mode)
