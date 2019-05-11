import os

# Split all IP in list
fichier = open("ip_bootnode.txt", "r")
list_ip = fichier.read()
ip = list_ip.split(" ")
fichier.close()

# Write good IP in file
fichier = open("ip_bootnode.txt", "w")

if(ip[0][0:4] == "10.0"):
	fichier.write(ip[0])
elif(ip[1][0:4] == "10.0"):
	fichier.write(ip[1])
else:
	fichier.write(ip[2])

fichier.close()
