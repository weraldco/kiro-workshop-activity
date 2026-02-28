"""
Workshop Management API - Flask Application Initialization
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS


def create_app(config=None):
    """
    Factory function to create and configure the Flask application.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Default configuration
    # Path is now backend/workshop_data.json
    app.config['JSON_FILE_PATH'] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'workshop_data.json'
    )
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    # Configure CORS for frontend communication
    # SECURITY NOTE: Update origins for production deployment
    # Development origins allow common frontend dev server ports
    CORS(app, 
         origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:3001'],
         methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
    
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            "success": False,
            "error": str(error.description) if hasattr(error, 'description') else "Bad request",
            "data": {}
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            "success": False,
            "error": str(error.description) if hasattr(error, 'description') else "Resource not found",
            "data": {}
        }), 404
    
    @app.errorhandler(409)
    def conflict(error):
        """Handle 409 Conflict errors"""
        return jsonify({
            "success": False,
            "error": str(error.description) if hasattr(error, 'description') else "Conflict",
            "data": {}
        }), 409
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error"""
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.workshop_routes_v2 import workshop_bp_v2
    app.register_blueprint(workshop_bp_v2)
    
    from app.routes.participant_routes import participant_bp
    app.register_blueprint(participant_bp)
    
    # Keep old workshop routes for backward compatibility
    from app.routes.workshop_routes import workshop_bp
    app.register_blueprint(workshop_bp)
    
    return app
