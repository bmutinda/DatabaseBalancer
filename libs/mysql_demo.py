import mysql
import sys

DB_HOST = '127.0.0.1'
DB_NAME = 'mysql'
DB_PASSWORD = ''
DB_USER = 'root'

# create a mysql connection 
db = mysql.MySQLConnector()
conn = None
try:
	conn = db.connect( DB_HOST, DB_USER, DB_PASSWORD, DB_NAME )
except Exception, e:
	print e
	sys.exit(0)
	
print 'Connection established...'

# Build query runner 
# We will use this to run sql queries 
sql = mysql.QueryBuilder( conn )

# Run custom sql query
cursor = sql.run_query ( 'SHOW FULL PROCESSLIST' )
data = cursor.fetchall()
total = cursor.rowcount
print total
for row in data:
	user = row[1]
	print row
	
print cursor