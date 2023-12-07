# test_app.py
import unittest
import os
import io
from main import app, db
from werkzeug.datastructures import FileStorage
from sqlalchemy.orm import sessionmaker

# Import models
from main import Department, Job, HiredEmployee

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()

    def test_upload_csv(self):
        with app.app_context():
            # Create the database tables
            db.create_all()
            # Create a test file in the current directory
            departments_data = "1,Supply Chain\n2,Maintenance\n3,Staff\n"
            jobs_data = "1,Recruiter\n2,Manager\n3,Analyst\n"
            employees_data = "4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,2\n4572,Lidia Mendez,2021-07-27T19:04:09Z,1,2\n"

            departments_file = FileStorage(
                stream=io.BytesIO(departments_data.encode("utf-8")),
                filename="departments.csv",
                content_type="text/csv",
            )

            jobs_file = FileStorage(
                stream=io.BytesIO(jobs_data.encode("utf-8")),
                filename="jobs.csv",
                content_type="text/csv",
            )

            hired_employees_file = FileStorage(
                stream=io.BytesIO(employees_data.encode("utf-8")),
                filename="hired_employees.csv",
                content_type="text/csv",
            )

            # Send a POST request to the endpoint with the file
            response = self.app.post("/upload_csv", 
                content_type='multipart/form-data',
                data={
                    "files": [
                        departments_file,
                        jobs_file,
                        hired_employees_file
                    ]
                }
            )
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"message": "Files uploaded successfully"})

            # Check if the uploaded data is correctly stored in the database
                # Check if the departments table was correctly populated
            departments = Department.query.all()
            self.assertEqual(len(departments), 3)
            self.assertEqual(departments[0].department, "Supply Chain")
            self.assertEqual(departments[1].department, "Maintenance")
            self.assertEqual(departments[2].department, "Staff")

            # Check if the jobs table was correctly populated
            jobs = Job.query.all()
            self.assertEqual(len(jobs), 3)
            self.assertEqual(jobs[0].job, "Recruiter")
            self.assertEqual(jobs[1].job, "Manager")
            self.assertEqual(jobs[2].job, "Analyst")

            # Check if the hired_employees table was correctly populated
            employees = HiredEmployee.query.all()
            self.assertEqual(len(employees), 2)
            self.assertEqual(employees[0].name, "Marcelo Gonzalez")
            self.assertEqual(employees[0].department_id, 1)
            self.assertEqual(employees[0].job_id, 2)
            self.assertEqual(employees[1].name, "Lidia Mendez")
            self.assertEqual(employees[1].department_id, 1)
            self.assertEqual(employees[1].job_id, 2)


if __name__ == "__main__":
    unittest.main()