import os
import bluetooth

ESP32_MAC = "24:6F:28:15:95:0A" #Test
#ESP32_MAC = "24:6F:28:A2:73:F2"
OMNIW_MAC = "00:21:13:01:08:BE"
 
def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print("Accepted connection from " + str(address))
  
  data = client_sock.recv(1024)
  print("received [%s]" % data)
  
  client_sock.close()
  server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  #sock.send("[00619]: 1")
  sock.send("1")
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print(str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
    
#lookUpNearbyBluetoothDevices()
sendMessageTo(ESP32_MAC)
#sendMessageTo(OMNIW_MAC)
