
# Globant Data Engineering Coding Challenge

Welcome to the Globant Data Engineering Coding Challenge. In this challenge, I've implemented a local REST API for a database migration with three tables (departments, jobs, employees). Additionally, I explored the data and created endpoints for specific metrics for the stakeholders. Let's walk through the sections and features.

## Section 1: API

### 1. Receive historical data from CSV files
- The API provides an endpoint `/upload_csv` to receive historical data from CSV files in  **multipart/form-data**.
- Files can be uploaded using the `files` parameter in a POST request.

### 2. Upload these files to the new DB
- Upon receiving CSV files, the API inserts the data into a SQL database.
- Database details can be configured in the application.

### 3. Be able to insert batch transactions
- The API supports batch transactions for inserting 1 to 1000 rows with a single request.
- Batch processing is implemented to optimize data insertion.

**Setup and Run Instructions:**
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure the database connection details in `app.py`.
4. Run the application using `python app.py`.

## Section 2: SQL

### 1. Number of employees hired for each job and department in 2021 divided by quarter
- Endpoint: `/metrics/employees_per_job_department`
- Outputs a table sorted alphabetically by department and job with quarterly hiring metrics.

### 2. List of ids, name, and number of employees hired for each department
- Endpoint: `/metrics/departments_more_than_mean`
- Outputs a table of departments that hired more employees than the mean, sorted by the number of employees hired (descending).


**Cloud Services Used:**
- [AWS](https://aws.amazon.com/es/)

**Testing Library Used:**
- [pytest](https://docs.pytest.org/en/7.4.x/)


## CSV Files Structures

### hired_employees.csv
| Field         | Type    | Description                                             |   |   |
|---------------|---------|---------------------------------------------------------|---|---|
| id            | INTEGER | Id of the employee                                      |   |   |
| name          | STRING  | Name and surname of the employee                        |   |   |
| datetime      | STRING  | Hire datetime in ISO format                             |   |   |
| department_id | INTEGER | Id of the department which the employee was hired for   |   |   |
| job_id        | INTEGER | Id of the job which the employee was hired for          |   |   |

### departments.csv
| Field      | Type    | Description                 |   |   |
|------------|---------|-----------------------------|---|---|
| id         | INTEGER | Id of the department        |   |   |
| department | STRING  | Name of the department      |   |   |

### jobs.csv
| Field | Type    | Description           |   |   |
|-------|---------|-----------------------|---|---|
| id    | INTEGER | Id of the job          |   |   |
| job   | STRING  | Name of the job         |   |   |


## Conclusion

Thank you for reviewing my solution to the Globant Data Engineering Coding Challenge. If you have any questions or feedback, please feel free to reach out.