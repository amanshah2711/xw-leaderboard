 

from app import app
import os

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=os.getenv('DEBUG', True))
