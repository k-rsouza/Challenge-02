from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3307/flask-diet'

db.init_app(app)


# Criar refeição
@app.route('/meals', methods=['POST'])
def create_meal():
    data = request.json
    meal = Meal(
        name=data['name'],
        description=data['description'],
        date_time=datetime.now(),  #seta como horario da refeição a hora que ela foi postada
        is_on_diet=data['is_on_diet'],
        user_id=data['user_id']
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": f"Meal {meal.name} added successfully!"}), 200

# Editar refeição
@app.route('/meals/<int:meal_id>', methods=['PUT'])
def edit_meal(user_id):
    data = request.json
    meal = Meal.query.get_or_404(user_id)
    meal.name = data.get('name', meal.name)
    meal.description = data.get('description', meal.description)
    if 'date_time' in data:
        meal.date_time = datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S')
    if 'is_on_diet' in data:
        meal.is_on_diet = data['is_on_diet']
    if 'user_id' in data:
        meal.user_id = data['user_id']
    db.session.commit()
    return jsonify(meal.to_dict())

# Apagar refeição
@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)  # retorna 404 automático se não encontrar

    db.session.delete(meal)
    db.session.commit()

    return jsonify({
        "message": f"Meal {meal.name} has been deleted!"
}), 200

# Listar refeições de um usuário
@app.route('/meals', methods=['GET'])
def list_meals():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    meals = Meal.query.filter_by(user_id=user_id).all()
    return jsonify([meal.to_dict() for meal in meals])

# Visualizar uma única refeição
@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    return jsonify(meal.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
