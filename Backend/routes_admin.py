from flask import Blueprint, render_template, jsonify
from admin_analysis import get_basic_stats, get_trend_prediction

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template('/admin/dashboard.html')

@admin_bp.route('/api/admin/stats')
def fetch_admin_stats():
    stats = get_basic_stats()
    return jsonify(stats)

@admin_bp.route('/api/admin/trends')
def fetch_admin_trends():
    trend = get_trend_prediction()
    return jsonify(trend)
