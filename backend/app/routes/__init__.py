from flask import Blueprint, jsonify

# Blueprint: chia app thành modules
# 'main' = tên nội bộ của blueprint (phải unique)
# __name__ = giúp Flask tìm templates/static files relative tới module này
main_bp = Blueprint('main', __name__)


@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Dùng để:
    - Kiểm tra app đang chạy
    - Docker/AWS dùng để biết container còn sống
    - Verify nhanh sau deploy
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Phishing Detection API is running'
    }), 200
