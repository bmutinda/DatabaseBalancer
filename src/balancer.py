import logger 
Logger = logger.Logger

class Balancer:
	def __init__( self ):
		self.instances = []
	
	# Add a database server instance 
	def add_db_instance( self, db_instance ):
		if db_instance:
			self.instances.append( db_instance )
		
	# Connects to all the instances specified 
	def connect_all( self ):
		Logger.log( 'connecting to %d instances' %(len(self.instances)))
		
		for instance in self.instances:
			instance.connect()
			
	def disconnect_all( self ):
		Logger.log( 'disconnecting %d instances' %(len(self.instances)))
		
		for instance in self.instances:
			instance.disconnect()
	
	# Get the connection status of an instance 
	def get_status( self , db_instance ):
		return db_instance.is_connected()
	
	# Get all the failed connections as objects
	def get_failed_connections( self ):
		failed_instances = []
		for instance in self.instances:
			if not instance.is_connected():
				failed_instances.append( instance )
				
		return failed_instances
		
	# Get the total no of failed connections 
	def get_total_failed_connections( self ):
		return len( self.get_failed_connections() )
		
	# This does the actual work of selecting the best instance to connect from 
	# We actually pull total process list for all the instances then choose the 
	# with fewer of them for the next connection
	#
	# This can be changed in the future to select an instance based on the 
	# previous selections made by the balancer or based on the type 
	# of the queries which are actually in the queue 
	def choose_instance( self ):
		instances_info = []
		for instance in self.instances:
			if instance.is_connected():
				total_processes = instance.get_total_processes( )
				instance_info = {}
				instance_info["instance"] = instance
				instance_info["total"] = total_processes
		
				instances_info.append( instance_info )
		# we sort the instances by the no of running processes 
		sorted_instances = sorted( instances_info, key = lambda instance: instance["total"] )
		
		# check cores usage 
		# http://code.google.com/p/psutil/ --- works perfect 
		# https://github.com/giampaolo/psutil
		return sorted_instances[0]["instance"]