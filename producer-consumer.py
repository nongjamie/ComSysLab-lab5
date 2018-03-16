import sys
import time
import random
import threading

value = 1
value_lock = threading.Lock()

class Producer( threading.Thread ):
	def __init__( self , items , limit , condition ):
		threading.Thread.__init__( self )
		self.items = items
		self.limit = limit
		self.condition = condition


	def produce_item( self ):
		global value
		value_lock.acquire()
		value = value + 1
		value_lock.release()
		self.items.append( value )
		print ( "{}: i produced an item {}".format( self.name , value ) )
		print ( "{} waiting consummer".format( len( self.items ) ) )


	def wait( self ):
		time.sleep( random.uniform( 0 , 3 ) )

	def run( self ):
		while 1:
			self.wait()
			self.condition.acquire()
			if len( self.items ) < self.limit :
				self.produce_item()
				self.condition.notify()
			else :
				self.condition.notifyAll()
			self.condition.release()


class Consumer( threading.Thread ):
	def __init__( self , items , limit , condition ):
		threading.Thread.__init__( self )
		self.items = items
		self.limit = limit
		self.condition = condition

	def consume_item( self ):
		item = self.items.pop()
		print ( "{}: i consumed an item {}".format( self.name , item ) )
		print ( "{} waiting consummer".format( len( self.items ) ) )

	def wait( self ):
		time.sleep( random.uniform( 0 , 3 ) )

	def run( self ):
		while 1:
			self.wait()
			self.condition.acquire()
			if len( self.items ) > self.limit :
				self.consume_item()
			else :
				self.condition.wait()
			self.condition.release()

def usage( script ):
	print ( "Usage:\t%s count_producers count_consumers buffer_length" % script )

if __name__ == "__main__":

	if len( sys.argv ) != 4:
		usage( sys.argv[0] )
		sys.exit( 0 )
	value = 1
	count_producers = int( sys.argv[1] )
	count_consumers = int( sys.argv[2] )
	buffer_length = int( sys.argv[3] )

	items = []
	producers = []
	consumers = []

	condition = threading.Condition()

	#acquire while buffer is not full
	can_produce = buffer_length

	#acquire while buffer is not empty
	can_consume = 0

	for i in range( count_producers ):
		producers.append( Producer( items , can_produce , condition ) )
		producers[-1].start()

	for i in range( count_consumers ):
		consumers.append( Consumer( items , can_consume , condition ) )
		consumers[-1].start()

	for p in producers:
		p.join()

	for c in consumers:
		c.join()
