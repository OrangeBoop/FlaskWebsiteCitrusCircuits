from website import create_app
from website.views import initialize_database
app=create_app()

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

with app.app_context():
    initialize_database()

if __name__ == '__main__':
    app.run(debug=True)

