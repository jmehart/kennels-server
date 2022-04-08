# A package in Python is just a directory with a certain file in it.

# That directory needs to have a file called __init__.py in it. It's that file, with its weird name, that magically makes a directory into a package.

# With Python packages, you don't need to specify the file path and name. 
# You can combine all of the files in sub-directories, and sub-directories of sub-directories, into a single namespace.

from .animal_requests import get_all_animals, get_single_animal, get_animals_by_location_id, get_animals_by_status, delete_animal

from .location_requests import get_all_locations, get_single_location

from .employee_requests import get_all_employees, get_single_employee, get_employees_by_location_id

from .customer_requests import get_all_customers, get_single_customer, get_customers_by_email