from src import balancer
from src.logger import Logger
from src.db_instances import DBInstance

# enable debugging 
Logger.debug = True 

# create our balancers object 
myBalancer = balancer.Balancer( )

# create our database instances
instance1 = DBInstance('127.0.0.1', 'root', '' )
instance2 = DBInstance('192.168.1.27', 'boni', '', 'store')

# Add our instances to the balancer 
myBalancer.add_db_instance( instance1 )
myBalancer.add_db_instance( instance2 )

# Connect to all instances 
# NB: ->>>>Fails if one of them cannot be connected to ->>> Not implemented for now  
myBalancer.connect_all()

# Get any failed connections 
print myBalancer.get_total_failed_connections()

# Go ahead and select one instance to use in the next connection
# NB: Returns instance object->
instance = myBalancer.choose_instance( )
print instance.to_string()

# close all connections 
myBalancer.disconnect_all()