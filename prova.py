
foto = open("./Foto/Culo/13121.jpg", "rb").read()
lun = len(foto)
password = b"\x10"*lun
ris = [foto[i] ^ password[i] for i in range(lun)]
print(ris)
ris = bytearray(ris)
print (ris)
ris2 = [password[i] ^ ris[i] for i in range (lun)]
ris2 = bytearray(ris2)
foto_n = open("./prova.jpg", "wb").write(ris2)

