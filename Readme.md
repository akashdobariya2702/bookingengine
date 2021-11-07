# run below command to run project.
source dj_run.sh

# get available Apartments and Hotels based on date range and availability
http://localhost:8000/api/v1/units/?max_price=100&check_in=2021-12-09&check_out=2021-12-12

# admin panel
http://127.0.0.1:8000/admin/
username - admin
password - admin
