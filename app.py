from flask import Flask, request, jsonify
from models.user import User
from models.meal import Meal
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@127.0.0.1:5432/daily-diet-python-api'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# view login
login_manager.login_view = 'login'
# Session <- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create User
@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email and password:
        hashed_password_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashed_password_string = hashed_password_bytes.decode('utf-8')
        user = User(email=email, password=hashed_password_string)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "id": user.id})

    return jsonify({"message": "Dados invalidos"}), 400

# Login User
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email and password:
        # Login
        user = User.query.filter_by(email=email).first()
        hashed_password_bytes = user.password.encode('utf-8')
        
        isHashedTrue = bcrypt.checkpw(password.encode(), hashed_password_bytes)

        if user and isHashedTrue:
            login_user(user)
            return jsonify({"message": "User authenticated!"})

    return jsonify({"message": "Invalid credentials"}), 400

# Logout User
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User logged out!"})

# Read User
@app.route('/user/<string:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)

  if user:
    return {"email": user.email}
  
  return jsonify({"message": "Usuario não encontrado"}), 404

# Update User
@app.route('/user/<string:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id:
        return jsonify({"message": "Action not allowed"}), 403

    if user and data.get("password"):

        hashed_password_bytes = bcrypt.hashpw(data.get("password").encode(), bcrypt.gensalt())
        hashed_password_string = hashed_password_bytes.decode('utf-8')

        user.password = hashed_password_string
        db.session.commit()

        return jsonify({"message": f"User {id_user} updated", "id": user.id})

    return jsonify({"message": "User not found"}), 404

# Delete User
@app.route('/user/<string:user_id>', methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if user_id != current_user.id:
        return jsonify({"message": "Action not allowed"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted"})

    return jsonify({"message": "User not found"}), 404

# Create Meal
@app.route('/meal', methods=["POST"])
@login_required
def create_meal():
    data = request.json

    user_id = current_user.id
    name = data.get("name")
    description = data.get("description")
    inside_diet = data.get("inside_diet")

    if name and description and inside_diet:
        meal = Meal(user_id=user_id, name=name, description=description, inside_diet=inside_diet)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Meal created successfully", "id": meal.id})

    return jsonify({"message": "Dados invalidos"}), 400

# Fetch Meals
@app.route('/meals', methods=["GET"])
@login_required
def fetch_meals():
    meals = Meal.query.join(User).filter(User.id == current_user.id).all()
    
    if meals:
        return jsonify({"message": "Meals fetched successfully", "meals": [meal.to_dict() for meal in meals]})

    return jsonify({"message": "Dados invalidos"}), 400

# Update Meal
@app.route('/meal/<string:meal_id>', methods=["PUT"])
@login_required
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)
    
    if meal:
        data = request.json
        meal.name = data.get("name")
        meal.description = data.get("description")
        meal.inside_diet = data.get("inside_diet")
        db.session.commit()
        return jsonify({"message": "Meal updated successfully", "id": meal.id})

    return jsonify({"message": "Dados invalidos"}), 400

@app.route('/routes', methods=['GET'])
def list_routes():
    result = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        result.append(f"{rule} ({methods})")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
