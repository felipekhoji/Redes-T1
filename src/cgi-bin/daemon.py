#!/usr/bin/env python

import handlepackages
import socket
import sys
import thread
import subprocess
import math
import time

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024 

# cria socket TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# atrela um IP e uma porta ao socket
s.bind((TCP_IP, TCP_PORT))

s.listen(1)

def processaRequisicao(conn):
	# recebe o pacote
	data = conn.recv(BUFFER_SIZE)
	if data:
		# verifica checksum do pacote
		if(handlepackages.verificaChecksum(data[0:160])):
			protocol, source_address, dest_address, option = handlepackages.desempacota(data)

			# interpreta comando e argumentos
			comando = ''
			dicionario_comandos = {1:'ps', 2:'df', 3:'finger', 4:'uptime'}
			comando += dicionario_comandos[protocol]
			args = ''.join(chr(int(option[i:i+8], 2)) for i in xrange(0, len(option), 8)).split(" ")
			if args[0] != '':
        	        	for i in range(0, len(args)):
                	        	comando += " " + args[i]

			# executa comando
			try:
				output = subprocess.check_output(comando, stderr=subprocess.STDOUT, shell=True)
			except subprocess.CalledProcessError as e:
				output = e.output

			tamanho_msg = len(output)		
			msg = output

			# divide o output do comando em pedacos para caber em cada pacote
			for i in range(0, (tamanho_msg / 32) + 1):
				tupla = [0,0,msg[i*32:i*32+32]]
				data = handlepackages.empacota(tupla,dest_address,source_address)
				# envia pacotes da resposta
				conn.send(data)
				# tempo para o webserver receber todas as respostas
				time.sleep(0.005)
	conn.close()

while True:
	# o accept espera uma requisicao
	conn, addr = s.accept()
	# cria uma thread para processar a requisicao
	thread.start_new_thread(processaRequisicao, (conn,))

