from sshtunnel import SSHTunnelForwarder
import os
from getpass import getpass

class tunnel:
    """ Class can initialise he tunnel with the users username and password. Store the port within an 
    environment variable so it can be used within the database connection. The tunnel class is used to 
    establish a tunnel to the university CIM server so that the team can easily establish a connection to 
    the server without running the commands. This should speed up development since the people in the 
    team with less confidence in their abilities are able to continue programming without worrying about 
    tunneling.

    Attributes:
        server (SSHTunnelForwarder): The tunnel which allows the app to connect to CIM.
    """
    def __init__(self):
        self.server = SSHTunnelForwarder(
            'linux.cim.rhul.ac.uk',
            ssh_username=input("Username: "),
            ssh_password=getpass(),
            remote_bind_address=('teachdb.cs.rhul.ac.uk', 5432)
        )
        self.server.start()
        os.environ['PORT'] = str(self.server.local_bind_port)
        print("----- tunnel opened -----")

    '''
    Close the tunnel
    '''
    def close_tunnel(self):
        print("----- tunnel closed -----")
        self.server.stop()