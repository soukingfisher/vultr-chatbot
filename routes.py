from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Portfolio
from .utils import get_stock_prediction

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@api_bp.route('/portfolio', methods=['POST'])
@jwt_required()
def add_stock():
    user_id = get_jwt_identity()
    data = request.get_json()
    stock_symbol = data.get('stock_symbol')
    quantity = data.get('quantity')
    purchase_price = data.get('purchase_price')

    portfolio = Portfolio(user_id=user_id, stock_symbol=stock_symbol, quantity=quantity, purchase_price=purchase_price)
    db.session.add(portfolio)
    db.session.commit()
    return jsonify({'message': 'Stock added to portfolio'}), 201

@api_bp.route('/portfolio', methods=['GET'])
@jwt_required()
def get_portfolio():
    user_id = get_jwt_identity()
    portfolios = Portfolio.query.filter_by(user_id=user_id).all()
    result = [{'stock_symbol': p.stock_symbol, 'quantity': p.quantity, 'purchase_price': p.purchase_price} for p in portfolios]
    return jsonify(result), 200

@api_bp.route('/recommendation', methods=['GET'])
@jwt_required()
def get_recommendation():
    user_id = get_jwt_identity()
    portfolios = Portfolio.query.filter_by(user_id=user_id).all()
    recommendations = []
    for portfolio in portfolios:
        prediction = get_stock_prediction(portfolio.stock_symbol)
        recommendations.append({
            'stock_symbol': portfolio.stock_symbol,
            'predicted_value': prediction
        })
    return jsonify(recommendations), 200
