import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        res = []
        for user in User.query.all():
            res.append(user.get_dict())
        return jsonify(res)
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return 'Пользователь создан'


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return 'Пользователь не найден', 404
        else:
            return jsonify(user.get_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return 'Пользователь не найден',
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        return f'Пользователь с id {user_id} изменен'
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return 'Пользователь не найден', 404
        db.session.delete(user)
        db.session.commit()
        return f'Пользователь с id {user_id} удален'


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        res = []
        for order in Order.query.all():
            res.append(order.get_dict())
        return jsonify(res)
    if request.method == 'POST':
        order = json.loads(request.data)
        month_start, day_start, year_start = order['start_date'].split('/')
        month_end, day_end, year_end = order['end_date'].split('/')
        new_order = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()
        return 'Заказ создан'


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return 'Заказ не найден'
        else:
            return jsonify(order.get_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        month_start, day_start, year_start = order_data['start_date'].split('/')
        month_end, day_end, year_end = order_data['end_date'].split('/')
        if order is None:
            return 'Заказ не найден', 404
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
        order.end_date = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return f'Заказ с id {order_id} изменен'
    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return 'Заказ не найден', 404
        db.session.delete(order)
        db.session.commit()
        return f'Заказ с id {order_id} удален'


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        res = []
        for offer in Offer.query.all():
            res.append(offer.get_dict())
        return jsonify(res)
    if request.method == "POST":
        offer = json.loads(request.data)
        new_offer = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()
        return 'Предложение создано'


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return 'Предложение не найдено'
        else:
            return jsonify(offer.get_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return 'предложение не найдено', 404
        offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return f'Предложение с id {offer_id} изменено'
    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return 'Предложение не найдено', 404
        db.session.delete(offer)
        db.session.commit()
        return f'Предложение с id {offer_id} удалено'


if __name__ == '__main__':
    app.run()
