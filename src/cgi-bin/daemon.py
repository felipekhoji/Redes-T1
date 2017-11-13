#!/usr/bin/env python

import socket
import sys
import thread
import subprocess

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024 

# cria socket TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# atrela um IP e uma porta ao socket
s.bind((TCP_IP, TCP_PORT))

s.listen(1)

def processaRequisicao(conn):
	data = conn.recv(BUFFER_SIZE)
	if data:
		print "received data:", data
		#desempacota(data)
		comando = [] # comando e argumentos a serem executados
		comando.append("ps")
		#comando.append(argumentos)
		p = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True) # executa comando com possiveis argumentos
		(output, erros) = p.communicate()
		#data = empacota(output)
		conn.send(data)  # envia resposta
	conn.close()

while True:
	# o accept espera uma requisicao
	conn, addr = s.accept()
	print 'Endereco da conexao:', addr
	# cria uma thread para processar a requisicao
	thread.start_new_thread(processaRequisicao, (conn,))

