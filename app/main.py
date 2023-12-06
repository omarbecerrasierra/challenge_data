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

# Step 2: get the list of departments
@app.route("/metrics/employees_per_job_department", methods=["GET"])
def employees_per_job_department():
    try:
        start_date = request.args.get("start_date", "2021-01-01")
        end_date = request.args.get("end_date", "2021-12-31")
        print(start_date, end_date)
        sql_query = text("""
            SELECT
                department,
                job,
                COUNT(hired_employee.id) AS hired,
                EXTRACT(quarter FROM datetime) AS quarter
            FROM hired_employee
            JOIN department ON department.id = hired_employee.department_id
            JOIN job ON job.id = hired_employee.job_id
            WHERE datetime BETWEEN :start_date AND :end_date
            GROUP BY department, job, quarter
            ORDER BY department, job, quarter
            """)
    
        result = db.session.execute(sql_query, {"start_date": start_date, "end_date": end_date}).fetchall()

        data = {}
        for row in result:
            key = (row.department, row.job)
            if key not in data:
                data[key] = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
            data[key][f'Q{row.quarter}'] = row.hired

        output = [{'department': department, 'job': job, **quarters} for (department, job), quarters in data.items()]
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": "Invalid request"}), 400

@app.route("/metrics/departments_more_than_mean", methods=["GET"])
def departments_more_than_mean():
    try:
        start_date = request.args.get("start_date", "2021-01-01")
        end_date = request.args.get("end_date", "2021-12-31")
        sql_query =  text("""
            SELECT id, department, hired
            FROM (
                SELECT
                    department.id AS id,
                    department.department AS department,
                    COUNT(hired_employee.id) AS hired,
                    AVG(COUNT(hired_employee.id)) OVER () AS avg_hired
                FROM department
                JOIN hired_employee ON department.id = hired_employee.department_id
                WHERE hired_employee.datetime BETWEEN :start_date AND :end_date
                GROUP BY department.id, department.department
            ) subquery
            WHERE hired > avg_hired
            ORDER BY hired DESC
            """)

        result = db.session.execute(sql_query, {"start_date": start_date, "end_date": end_date}).fetchall()
        output = [{'id': row.id, 'department': row.department, 'hired': row.hired} for row in result]
        return jsonify(output)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
