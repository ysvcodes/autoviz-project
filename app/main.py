"""
Author: autoviz-project user
File Purpose: Main application file for the autoviz-project.
              A simple Flask web server.
Dependencies: Flask
"""
from flask import Flask

app_instance = Flask(__name__) # Renamed to avoid clash with 'app' in Dockerfile CMD if we use Gunicorn later

@app_instance.route('/')
def hello():
    """
    Route for the home page.
    Returns a simple greeting.
    """
    return "Hello from autoviz-project (v2 pipeline)!"

if __name__ == '__main__':
    app_instance.run(host='0.0.0.0', port=5000) 