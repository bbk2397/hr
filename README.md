# hr


# Help
#1 Create a Python virtual environment

#2 Activate this environment

#3 Install the requirements (there is a requirements.txt file)


#4 Some commands that could be helpful

python manage.py makemigrations

python manage.py migrate

python manage.py etl

python manage.py runserver


#5 Some paths that could be helpful

- used data: business/hr/data/MOCK_DATA.json
- database: business/db.sqlite3
- etl command file: business/hr/management/commands/etl.py

#6 Even more paths
- models: business/hr/models.py
- most of the relevant code: business/hr/api (views.py, serializers.py, urls.py, filters.py)
- not forgetting about the settings and the main urls files at business/business: settings.py, urls.py

#7 Implemented functionality:
- an etl for the initial data
- endpoints for this data:
  - read all
    - sorting
    - pagination
    - filtering based on URL parameters
- endpoints for statistics:
  - average age per industry
  - average salaries per industry
  - average salaries per years of experience
  - more:
    - average salaries per years of experience and industry
    - average salaries per years of experience intervals

#8 Some endpoints that might be useful:
  - GET api/v1/employees/
    - it has pagination, sorting, filtering
  - GET api/v1/employees/<id>
  - PUT api/v1/employees/<id>
  - DELETE api/v1/employees/<id>
  - GET api/v1/statistics/average-salaries-per-industry
  - GET api/v1/statistics/average-salaries-per-yoe
  - GET api/v1/statistics/average-age-per-industry
  - GET api/v1/statistics/average-salaries-per-yoe-and-industry
  - GET api/v1/statistics/agg-salaries-per-yoe-intervals

#9 Some of the used tools: Django Rest Framework, Pandas, Django-Filter

#10 There is also some basic data validation and initial data cleaning.

#11 Pandas was used with vectorization and performance in mind. And without for loops.
 
