from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({
        'status': 'healthy',
        'message': 'Phishing Detection API is running'
    }), 200
