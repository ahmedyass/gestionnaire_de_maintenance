from app import app
from app.models import db


app.secret_key = "super secret key"

if __name__ == '__main__':
    app.run(debug = True)