"""
Workshop Management API - Main Application Entry Point
"""
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application in development mode
    app.run(host='0.0.0.0', port=5001, debug=True)
