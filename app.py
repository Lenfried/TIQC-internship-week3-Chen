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

# MySQL Routes
@app.route('/api/mysql/cards', methods=['GET'])
def mysql_get_all():
    """Get all graphics cards from MySQL"""
    try:
        cards = mysql_db.read_all()
        # Convert Decimal and date objects to strings for JSON serialization
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
    """Get all graphics cards from MongoDB"""
    try:
        cards = mongodb_db.read_all()
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
