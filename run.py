"""
Workshop Management API - Application Entry Point

This script starts the Flask development server for the Workshop Management API.
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Run the Flask development server
    # host='0.0.0.0' makes the server accessible from other machines
    # port=5000 is the default Flask port
    # debug=True enables auto-reload and detailed error messages
    app.run(host='0.0.0.0', port=5000, debug=True)
