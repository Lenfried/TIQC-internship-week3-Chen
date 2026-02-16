from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from mysql_db import MySQLDatabase
from mongodb_db import MongoDBDatabase
import json

app = Flask(__name__)
CORS(app)

# Initialize database connections
mysql_db = MySQLDatabase()
mongodb_db = MongoDBDatabase()

@app.route('/')
def index():
    """Serve the dashboard page"""
    return render_template('dashboard.html')

def _parse_filters():
    """Parse search/filter query params from request."""
    filters = {}
    if request.args.get('search'):
        filters['search'] = request.args.get('search').strip()
    if request.args.get('manufacturer'):
        filters['manufacturer'] = request.args.get('manufacturer').strip()
    if request.args.get('memory_type'):
        filters['memory_type'] = request.args.get('memory_type').strip()
    try:
        if request.args.get('memory_min') not in (None, ''):
            filters['memory_min'] = int(request.args.get('memory_min'))
    except (TypeError, ValueError):
        pass
    try:
        if request.args.get('memory_max') not in (None, ''):
            filters['memory_max'] = int(request.args.get('memory_max'))
    except (TypeError, ValueError):
        pass
    try:
        if request.args.get('price_min') not in (None, ''):
            filters['price_min'] = float(request.args.get('price_min'))
    except (TypeError, ValueError):
        pass
    try:
        if request.args.get('price_max') not in (None, ''):
            filters['price_max'] = float(request.args.get('price_max'))
    except (TypeError, ValueError):
        pass
    return filters if filters else None

# MySQL Routes
@app.route('/api/mysql/cards', methods=['GET'])
def mysql_get_all():
    """Get graphics cards from MySQL with optional search/filters"""
    try:
        filters = _parse_filters()
        cards = mysql_db.read_all(filters=filters)
        for card in cards:
            if 'price_usd' in card and card['price_usd'] is not None:
                card['price_usd'] = float(card['price_usd'])
            if 'release_date' in card and card['release_date']:
                card['release_date'] = str(card['release_date'])
            if 'created_at' in card and card['created_at']:
                card['created_at'] = str(card['created_at'])
            if 'updated_at' in card and card['updated_at']:
                card['updated_at'] = str(card['updated_at'])
        return jsonify({'success': True, 'data': cards})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mysql/cards', methods=['POST'])
def mysql_create():
    """Create a new graphics card in MySQL"""
    try:
        data = request.json
        card_id = mysql_db.create(data)
        return jsonify({'success': True, 'id': card_id, 'message': 'Card created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mysql/cards/<int:card_id>', methods=['PUT'])
def mysql_update(card_id):
    """Update a graphics card in MySQL"""
    try:
        data = request.json
        success = mysql_db.update(card_id, data)
        if success:
            return jsonify({'success': True, 'message': 'Card updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mysql/cards/<int:card_id>', methods=['DELETE'])
def mysql_delete(card_id):
    """Delete a graphics card from MySQL"""
    try:
        success = mysql_db.delete(card_id)
        if success:
            return jsonify({'success': True, 'message': 'Card deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# MongoDB Routes
@app.route('/api/mongodb/cards', methods=['GET'])
def mongodb_get_all():
    """Get graphics cards from MongoDB with optional search/filters"""
    try:
        filters = _parse_filters()
        cards = mongodb_db.read_all(filters=filters)
        return jsonify({'success': True, 'data': cards})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mongodb/cards', methods=['POST'])
def mongodb_create():
    """Create a new graphics card in MongoDB"""
    try:
        data = request.json
        card_id = mongodb_db.create(data)
        return jsonify({'success': True, 'id': card_id, 'message': 'Card created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mongodb/cards/<card_id>', methods=['PUT'])
def mongodb_update(card_id):
    """Update a graphics card in MongoDB"""
    try:
        data = request.json
        success = mongodb_db.update(card_id, data)
        if success:
            return jsonify({'success': True, 'message': 'Card updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mongodb/cards/<card_id>', methods=['DELETE'])
def mongodb_delete(card_id):
    """Delete a graphics card from MongoDB"""
    try:
        success = mongodb_db.delete(card_id)
        if success:
            return jsonify({'success': True, 'message': 'Card deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        mysql_db.close()
        mongodb_db.close()
