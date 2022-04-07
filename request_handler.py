import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from views import get_all_animals, get_single_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_all_customers, get_single_customer, create_animal, create_location, create_employee, create_customer, delete_animal, delete_location, delete_employee, delete_customer

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



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple
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
        response = {}  # Default response

            # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = f"{get_single_animal(id)}"

            else:
                response = f"{get_all_animals()}"
                
        if resource == "locations":
            if id is not None:
                response = f"{get_single_location(id)}"

            else:
                response = f"{get_all_locations()}"        
        
        if resource == "employees":
            if id is not None:
                response = f"{get_single_employee(id)}"

            else:
                response = f"{get_all_employees()}"   
                
        if resource == "customers":
            if id is not None:
                response = f"{get_single_customer(id)}"

            else:
                response = f"{get_all_customers()}"              

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal, location, employee, etc.
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_resource = create_animal(post_body)   

        # Add a new location to the list. Don't worry about
        # the orange squiggle, you'll define the create_location
        # function next.
        if resource == "locations":
            new_resource = create_location(post_body)   

        # Add a new employee to the list. Don't worry about
        # the orange squiggle, you'll define the create_employee
        # function next.
        if resource == "employees":
            new_resource = create_employee(post_body)   

        # Add a new customer to the list. Don't worry about
        # the orange squiggle, you'll define the create_customer
        # function next.
        if resource == "customers":
            new_resource = create_customer(post_body)   

        # Encode the new resource and send in response
        self.wfile.write(f"{new_resource}".encode())
        

    def do_DELETE(self):
        # Set a 204 response code
        # A 204 response code in HTTP means, 
        # "I, the server, successfully processed your request, 
        # but I have no information to send back to you."
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            
        if resource == "locations":
            delete_location(id)    
            
        if resource == "employees":
            delete_employee(id) 
            
        if resource == "customers":
            delete_customer(id)       

        # Encode the new animal and send in response
        self.wfile.write("".encode())


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
