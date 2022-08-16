from flask_app import app
import os
print(os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)
    