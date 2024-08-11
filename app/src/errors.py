from flask import jsonify
from pymongo import errors

def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request'}), 400
    
    @app.errorhandler(403)
    def unauthorized_token(error):
        return jsonify({'error': "Invalid token"}), 403
    
    @app.errorhandler(errors.PyMongoError)
    def handle_database_error(error):
        print(f"Database error: {error}")
        return jsonify({'error': 'Database Error'}), 500
    
    