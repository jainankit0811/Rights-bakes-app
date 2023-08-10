from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Using SQLite database
db = SQLAlchemy(app)

# Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:id>')
def recipe(id):
    selected_recipe = Recipe.query.get(id)
    if selected_recipe:
        return render_template('recipes/recipe.html', recipe=selected_recipe)
    else:
        return "Recipe not found"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
