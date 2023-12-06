# Import the necessary libraries and modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, request
from dotenv import load_dotenv
from sqlalchemy import text
import os
import pandas as pd
load_dotenv()


# Create a Flask app
app = Flask(__name__)

HOST_DB = os.getenv('HOST_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB =  os.getenv('PASSWORD_DB')
DATABASE = os.getenv('DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define database models
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    department = db.Column(db.String, nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String,  nullable=False)

class HiredEmployee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True )
    datetime = db.Column(db.DateTime, nullable=True)
    department_id = db.Column(db.Integer, nullable=True)
    job_id = db.Column(db.Integer, nullable=True)

with app.app_context():
    db.create_all()

# Step 1: upload the CSV files
@app.route('/upload_csv', methods=['POST'])
def upload():
        files = request.files.getlist("files")
        # for made the load in batch is used the chunksize parameter
        for file in files: 
                if file.filename == "jobs.csv":
                        df = pd.read_csv(file, names = ['id', 'job'] ,header=None)
                        df.to_sql('job', con=db.engine, if_exists='replace', index=False, chunksize=1000)
                elif file.filename == "departments.csv":
                        df = pd.read_csv(file, names = ['id', 'department'] ,header=None)
                        df.to_sql('department', con=db.engine, if_exists='replace', index=False, chunksize=1000)
                elif file.filename == "hired_employees.csv":
                        df = pd.read_csv(file, names = ['id', 'name', 'datetime', 'department_id', 'job_id'] ,header=None)
                        df.to_sql('hired_employee', con=db.engine, if_exists='replace', index=False, dtype={'datetime': db.DateTime}, chunksize=1000)
                else:
                        return jsonify({"error": "Invalid file name"}), 400
        
        return jsonify({"message": "Files uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
