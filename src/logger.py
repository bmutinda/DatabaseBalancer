
class Logger:
	debug = False 
	
	def __init__( self , debug = False ):
		Logger.debug = debug
		
	@staticmethod
	def log( message, verbose = None ):
		print '%s :::-> %s' %(verbose, message)