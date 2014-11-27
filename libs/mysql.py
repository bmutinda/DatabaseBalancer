import MySQLdb
class MySQLConnector:
	def __init__( self ):
		self.db = None
		
	def connect( self, db_host, db_user, db_password, db_database ):
		try:
			self.db = MySQLdb.connect( db_host, db_user, db_password, db_database )
		except MySQLdb.OperationalError, e:
			raise e		
		return self.db 
		
	def get_connection( self ):
		print self.db
		
	def disconnect( self ):
		if self.db:
			self.db.close()
		return True
		
	def check_version( self ):
		pass 
		
class QueryBuilder:
	def __init__( self, db ):
		self.db = db
		
	def run_query( self, query ):
		cursor = self.db.cursor()
		cursor.execute( query )
		return cursor
		
	def run_insert( self, table, insert_data ):
		done = False
		keys = insert_data.keys()
		values = insert_data.values()
		query = "INSERT INTO %s (%s) VALUES  ('%s')" %(table, ",".join( keys ), "','".join( '%s' %x for x in values) )
		try:
			self.run_query(query)
			self.db.commit()
			done = True
		except Exception, e :
			self.db.rollback()
			print str(e)
			
		return done	

	def run_select( self, table, what = '*', condition = None, limit = None ):
		condition_keys = condition.keys()
		condition_values = condition.values()
		what_data = ",".join( what )

		query = "SELECT %s FROM %s " %( ",".join(what_data), table )
		# If their was a condition set 
		# we add it to our query 
		total_condition_data = len(condition_keys)
		if total_condition_data>0:
			query+=" WHERE "
			counter = 0
			separator = " AND "
			for key, val in condition.items():
				counter+=1
				if counter>=total_condition_data:
					separator = ""
				
				query+=' %s = \'%s\' %s' %(str(key), str(val), separator )
		
		if limit and is_integer(limit):
			query+=' LIMIT %d' %(limit)
			
		cursor = self.run_query( query )
		
		data = cursor.fetchall()
		return data