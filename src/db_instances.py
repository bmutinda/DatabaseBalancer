import logger
Logger = logger.Logger
from libs import mysql

class DBInstance:
	def __init__( self, host, user, password, database = 'mysql' ):
		self.host = host 
		self.user = user 
		self.password = password
		self.database = database
		
		self.db = mysql.MySQLConnector()
		self.conn = None 
		self.connected  = False
		self.sql = None 
		
		Logger.log('DbInstance created : %s ' %(self.to_string()))
		
	# Creates a connection to the db server 
	def connect( self ):
		Logger.log( 'Connecting to instance at : %s' %(self.to_string()))
		try:
			self.conn = self.db.connect( self.host, self.user, self.password, self.database )
			self.connected  = True
		except Exception, e :
			Logger.log( 'Connection to the instance failed with error = %s ::: %s ' %( str(e), self.to_string() ))
			
		if self.is_connected():
			self.sql = mysql.QueryBuilder( self.conn )
	
	# Closes database connection 
	def disconnect( self ):
		self.db.disconnect()
		
	# Gets the connection status to this instance 
	def is_connected( self ):
		return self.connected
	
	# Get a list of all the mysql processes running on this db server
	def get_processes( self ):
		processes = []
		if( self.is_connected() ):
			cursor = self.sql.run_query( "SHOW FULL PROCESSLIST")
			data = cursor.fetchall()
			for row in data:
				process = {}
				process["user"] = row[1]
				processes.append( process )
				
		return processes
			
	# Get the total processes in this db server 
	def get_total_processes( self ):
		return len( self.get_processes() )
	
	# Returns the class params as string 
	# To easily identify the instance from the others 
	def to_string( self ):
		return '[ host = %s, user=%s, password=%s ]' %(self.host, self.user, self.password )