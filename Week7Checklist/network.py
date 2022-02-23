from pickle import NONE
import socket

class Network:
	def __init__(self):
		self.serverIP = "192.168.36.36"
		self.portNumber = 5180
		self.checker = 0 
		self.message = "test message"
		self.socket = None
        # self.bufferLength = 4096

	def initialiseConnection(self):
        # ConnectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print ("Socket successfully created")
			self.socket.connect((self.serverIP,self.portNumber))
			print("Successfully connected!")
			# msg = "grp"
			# s.send(msg.encode())
			# print(s.recv(2048).decode())
			# s.close()
		except socket.error as err:
			print ("socket creation failed with error %s" %(err))

	def readMessage(self):
		if self.socket:
			try:
				data = self.socket.recv(2048).decode()
				return data
			except Exception as e:
				print("Error: %s " % str(e))
				print("Value not read")

	def writeMessage(self,message):
		if self.socket:
			try:
				self.socket.send(message.encode())
			except Exception as e:
				print("Error: %s " % str(e))
				print("Value not sent")
	
	def sendObstacleIdToAndroid(self,obstacleID):
		message = "ALG," + str(obstacleID)
		# print(message)
		self.sendMessage(message)
		return 1

	def generateAndroidMessage(x,y,facingDirection,stmMsgNumber):
		message = ["f","r","fr","fl","rr","rl","sr","sl"]


	def endConnection(self):
		self.socket.close()


		

	# def sendMessage(self):	
	# 	pass

	# def readMessage(self):
	# 	pass
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # print(s)
            # s.connect((self.serverIP, self.portNumber))
            # s.sendall(b"Hello, world")
            # data = s.recv(1024)

        # print(f"Received {data!r}")

    # def initialiseConnection():
    
    # def sendTCP(self,message=''):
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         sock.connect((self.serverIP,self.portNumber))
    #         print("Successful")
    #     except socket.error:
    #         pass
    #     else:
    #         sock.send(message)
    #     sock.close
    
    # def pc_is_connected(self):
	# 	"""
	# 	Check status of connection to PC
	# 	"""
	# 	return self.pc_is_connect

	# def init_pc_comm(self):
	# 	"""
	# 	Initiate PC connection over TCP
	# 	"""
	# 	# Create a TCP/IP socket
	# 	try:
	# 		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 		self.conn.bind((self.tcp_ip, self.port))
	# 		self.conn.listen(1)		#Listen for incoming connections
	# 		print "Listening for incoming connections from PC..."
	# 		self.client, self.addr = self.conn.accept()
	# 		print "Connected! Connection address: ", self.addr
	# 		self.pc_is_connect = True
	# 	except Exception, e: 	#socket.error:
	# 		print "Error: %s" % str(e)
	# 		print "Try again in a few seconds"


	# def write_to_PC(self, message):
	# 	"""
	# 	Write message to PC
	# 	"""
	# 	try:
	# 		self.client.sendto(message, self.addr)
	# 		# print "Sent [%s] to PC" % message
	# 	except TypeError:
	# 		print "Error: Null value cannot be sent"


	# def read_from_PC(self):
	# 	"""
	# 	Read incoming message from PC
	# 	"""
	# 	try:
	# 		pc_data = self.client.recv(2048)
	# 		# print "Read [%s] from PC" %pc_data
	# 		return pc_data
	# 	except Exception, e:
	# 		print "Error: %s " % str(e)
	# 		print "Value not read from PC"

