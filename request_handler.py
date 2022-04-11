import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from views import get_all_animals, get_single_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_all_customers, get_single_customer, get_customers_by_email, get_animals_by_location_id, get_employees_by_location_id, get_animals_by_status, delete_animal, update_animal, create_animal, create_employee

# What is a HTTP status code?
# An HTTP status code is a server response to a browser's request.
# When you visit a website, your browser sends a request to the site's server,
# and the server then responds to the browser's request with a three-digit code:
# the HTTP status code.

# The HTTP 200 OK success status response code indicates that the request has succeeded.
# A 200 response is cacheable by default.
# The meaning of a success depends on the HTTP request method:
# GET : The resource has been fetched and is transmitted in the message body.

# The HTTP 201 Created success status response code indicates that the request has succeeded
# and has led to the creation of a resource.

# The HTTP headers are used to pass additional information between the clients and the server
# through the request and response header.

# A function is a reusable block of programming statements designed to perform a certain task.
# To define a function, Python provides the def keyword.

# A Python if block no longer uses paranthesis 

# A Python list is like an array - booleans are now capitalized

# A Python dictionary looks like a JSON object and is used to create a collection of key value pairs
# a key doesn't have to be a string with Python

# Python print() function is similar to console.log()

# Whitespace / indentation defines scope rather than {}

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

# A tuple is a specialized list in Python and is surrounded by parenthesis.
# What makes it different is that it is immutable - meaning it cannot be changed after it is created.
# You can't add things, remove things, or change the position of anything in it.
# In Python, there is a very powerful tuple assignment feature that assigns the right-hand side of values into the left-hand side.
# In another way, it is called unpacking of a tuple of values into a variable.
# In packing, we put values into a new tuple while in unpacking we extract those values into a single variable.
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value ) # This is a tuple

        # No query string parameter
        else:
            id = None
            # Try to get the item at index 2
            try:
                id = int(path_params[2]) # int() Python function to convert a string to an integer
                # Convert the string "1" to the integer 1
                # This is the new parseInt()
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
        
    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            # Parse the URL and capture the tuple that is returned
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"                

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
                
            if key == "location_id" and resource == "animals":
                response = get_animals_by_location_id(value)
                
            if key == "location_id" and resource == "employees":
                response = get_employees_by_location_id(value)
                
            if key == "status" and resource == "animals":
                response = get_animals_by_status(value)          

        self.wfile.write(response.encode())
        
        
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request: creates a new object that's converted from a string into a Python dictionary,
    # then added to the ANIMALS list or other list you choose in views
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

    #     # Convert JSON string to a Python dictionary
    #     # In Python, you convert a string to a dictionary with json.loads().
        post_body = json.loads(post_body)

    #     # Parse the URL
        (resource, id) = self.parse_url(self.path)

    #     # Initialize new animal, location, employee, etc.
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_resource = create_animal(post_body)   

        # Add a new location to the list. Don't worry about
        # the orange squiggle, you'll define the create_location
        # function next.
    #     if resource == "locations":
    #         new_resource = create_location(post_body)   

    #     # Add a new employee to the list. Don't worry about
    #     # the orange squiggle, you'll define the create_employee
    #     # function next.
        if resource == "employees":
            new_resource = create_employee(post_body)   

    #     # Add a new customer to the list. Don't worry about
    #     # the orange squiggle, you'll define the create_customer
    #     # function next.
    #     if resource == "customers":
    #         new_resource = create_customer(post_body)   

    #     # Encode the new resource and send in response
        self.wfile.write(f"{new_resource}".encode())
        

    def do_DELETE(self):
    #     # Set a 204 response code
    #     # A 204 response code in HTTP means, 
    #     # "I, the server, successfully processed your request, 
    #     # but I have no information to send back to you."
        self._set_headers(204)

    #     # Parse the URL
        (resource, id) = self.parse_url(self.path)

    #     # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            
        # if resource == "locations":
        #     delete_location(id)    
            
        # if resource == "employees":
        #     delete_employee(id) 
            
        # if resource == "customers":
        #     delete_customer(id)       

    #     # Encode the new animal and send in response
        self.wfile.write("".encode())
        
        
    # def do_PUT(self):
    #     self._set_headers(204)
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     post_body = json.loads(post_body)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     # Delete a single animal from the list
    #     # if resource == "animals":
    #     #     update_animal(id, post_body)
            
    #     if resource == "locations":
    #         update_location(id, post_body)
            
    #     if resource == "employees":
    #         update_employee(id, post_body)
            
    #     if resource == "customers":
    #         update_customer(id, post_body)

    #     # Encode the new animal and send in response
    #     self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
