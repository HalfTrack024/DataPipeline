from opcua import Server
from random import randint
import datetime
import time

# Setup the server
server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

# Setup the namespace, not to be confused with the server's URI
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create a new object as the root node
myobj = server.nodes.objects.add_object(idx, "MyObject")

# Add a string variable to our object
myvar = myobj.add_variable(idx, "MyStringVariable", "Hello World")

# Add a numeric variable to our object
mynumvar = myobj.add_variable(idx, "MyNumericVariable", 42)
mynumvar1 = myobj.add_variable(idx, "MyNumericVariable1", 42)
mynumvar2 = myobj.add_variable(idx, "MyNumericVariable2", 42)
mynumvar3 = myobj.add_variable(idx, "MyNumericVariable3", 42)
mynumvar4 = myobj.add_variable(idx, "MyNumericVariable4", 42)
mynumvar5 = myobj.add_variable(idx, "MyNumericVariable5", 42)
mynumvar6 = myobj.add_variable(idx, "MyNumericVariable6", 42)
# Set the variables to be writable by clients
myvar.set_writable()

mynumvar.set_writable()
mynumvar1.set_writable()
mynumvar2.set_writable()
mynumvar3.set_writable()
mynumvar4.set_writable()
mynumvar5.set_writable()
mynumvar6.set_writable()

# Start the server
server.start()

print("Server started at {}".format(server.endpoint))
try:
    # Let the server run for some time (e.g., 1 hour)
    while True:
        time.sleep(10)

        # Update the numeric variable with a random number every second
        mynumvar.set_value(randint(0, 100))

except KeyboardInterrupt:
    print("Server offline")
    server.stop()
