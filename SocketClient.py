import socket
from General import General
from Clock import Clock

class SocketClient (General):
	def __init__ (self, host = "localhost", port = 8080, _buffer = 1024):
		self.host = host;
		self.port = port;
		self._buffer = _buffer;
		self.socket = socket.socket();
		self.receiving = False; # This variable determines whether the client socket is receiving data or not
		self.connected = False; # This variable determines wheether the client socket is connected or not

		# Callback definitions
		self.onConnectCallback = self.emptyFunction;
		self.onReceiveCallback = self.emptyFunction;
		self.onSendCallback = self.emptyFunction;
		self.onDisconnectCallback = self.emptyFunction;


	def emptyFunction (self, *args, **kwargs):
		pass;


	def connect (self, callback, _async = False):
		if not self.connected:
			if _async:
				self.setImmediate(self.onBeforeConnectCallback, {"callback": callback});
			else:
				self.onBeforeConnectCallback(callback = callback);


	def onBeforeConnectCallback (self, **kwargs):
		try:
			self.socket.connect((self.host, self.port));
			self.connected = True;
			self.Clock = Clock();

			kwargs["callback"](True, None);
		except Exception as e:
			kwargs["callback"](False, e);


	def startRecvFrom (self, client, _async = False):
		self.startReceivingFromServer(client, _async);


	def startReceivingFromServer (self, _async = False):
		if _async:
			def method ():
				self.receive();
				
			self.setInterval(method, 1);
		else:
			while True:
				self.receive();


	def recv (self, _async = False):
		self.receive(_async);


	def receive (self, _async = False):
		if self.connected:
			if _async:
				self.setImmediate(self.processReceivedData);
			else:
				self.processReceivedData();


	def processReceivedData(self):
		try:
			data = self.socket.recv(self._buffer)
			data = data.decode("utf-8")
			if data != "":
				data = self.jsonize(data); # Convert the data to json format (i.e: dict)

				self.onReceiveCallback(data, None);
		except Exception as e:
			self.onReceiveCallback(False, e);


	def send (self, data, _async = False):
		if self.connected:
			if _async:
				self.setImmediate(self.onBeforeSendCallback, {"data": data});
			else:
				self.onBeforeSendCallback(data = data)


	def onBeforeSendCallback (self, **kwargs):
		try:
			data = {
				"date": self.Clock.date(),
				"time": self.Clock.time(),
				"data": kwargs["data"]
			}

			self.socket.send(self.unjsonize(data).encode("utf-8"));

			self.onSendCallback(data, None);
		except Exception as e:
			self.onSendCallback(False, e);


	def onReceive (self, callback):
		self.onReceiveCallback = callback;


	def onSend (self, callback):
		self.onSendCallback = callback;


	def onDisconnect (self, callback):
		self.onDisconnectCallback = callback;


	def disconnect (self):
		if self.connected:
			self.socket.close();

if __name__ == '__main__':
	client = SocketClient();

	def onConnect (connected, err):
		if connected:
			print("Connection successful!");
		else:
			print("Connection failed!");

	def onReceive (data, err):
		if err:
			print("No data receieved!");
			print(err);
		else:
			print("Received data from server!");
			print(data);
			
	def onSend (data, err):
		if err:
			print("An error occurred while sending data.");
			print(err);
		else:
			print("successfully sent data to server!");

	client.connect(onConnect);
	client.onReceive(onReceive);
	client.onSend(onSend);

	client.send("Hello server! I've arrived");
	client.receive();

	client.Clock.wait(5);
	client.send("Are you still there?");

	client.Clock.wait(5);
	client.send("I'm going to disconnect now!");
	client.disconnect();