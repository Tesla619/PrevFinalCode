import os
#import bluetooth
import socket

#os.system("sudo rfcomm connect hci0 24:6F:28:A2:73:F2 1")
ESP_MAC = "24:6F:28:A2:73:F2"
 
def receiveMessages():
  #server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
  
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
  #sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock = socket.socket(socket.BTPROTO_RFCOMM)
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("[00619]: 1")
  sock.close()
  
# def lookUpNearbyBluetoothDevices():
#   nearby_devices = bluetooth.discover_devices()
#   for bdaddr in nearby_devices:
#    print(str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
    
#lookUpNearbyBluetoothDevices()
sendMessageTo(ESP_MAC) 