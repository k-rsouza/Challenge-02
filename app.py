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
def edit_meal(meal_id):
    data = request.json
    meals = Meal.query.filter_by(meal_id)  # Busca a refeição pelo id ou retorna 404

    if not meals:
        return jsonify({
            "message": "The meal you`ew"
        })
    # Atualiza os campos recebidos no JSON
    meal.name = data.get('name', meal.name)
    meal.description = data.get('description', meal.description)
    
    if 'date_time' in data:
        meal.date_time = datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S')
    
    if 'is_on_diet' in data:
        meal.is_on_diet = data['is_on_diet']
    
    if 'user_id' in data:
        meal.user_id = data['user_id']

    db.session.commit()

    return jsonify(meal.to_dict()), 200

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
@app.route('/users/<int:user_id>/meals', methods=['GET'])
def list_meals(user_id):
    meals = Meal.query.filter_by(user_id=user_id).all()
    if not meals:  # nenhum resultado encontrado
       return jsonify({
           "message": f"No meals found for user {user_id}..."
       }), 404
    
    return jsonify([meal.to_dict() for meal in meals]), 200

# Visualizar uma única refeição
@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meals = Meal.query.filter_by(id=meal_id).all()
    
    if not meals:
        return jsonify({
            "message": f"Meal {meal_id} not found..."
        })
    
    return jsonify([meal.to_dict() for meal in meals]), 200

if __name__ == '__main__':
    app.run(debug=True)
