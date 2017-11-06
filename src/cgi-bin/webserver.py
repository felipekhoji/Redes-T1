#!/usr/bin/env python

import socket
import cgi
import cgitb

### funcoes auxiliares ###

def obtemDadosDoFormulario( form ):
	possiveisCampos = ['maq1_ps', 'maq1_df', 'maq1_finger', 'maq1_uptime', 'maq2_ps', 'maq2_df', 'maq2_finger', 'maq2_uptime', 'maq3_ps', 'maq3_df', 'maq3_finger', 'maq3_uptime']
	
	#padrao definido pelo professor
	dicionario_comandos = {'ps':1, 'df':2, 'finger':3, 'uptime':4}
	
	#constroi lista de trincas, onde cada trinca tem o numero da maquina, o numero do comando e os parametros do comando
	lista = []
	for campo in possiveisCampos:
        	if campo in form:
	                lista.append([int(campo[3]), dicionario_comandos[campo[5:]], form.getvalue(campo.replace('_','-'), '')])
	return lista

### main ###

print "Content-Type: text/html;charset=utf-8\r\n\r\n"

cgitb.enable()

form = cgi.FieldStorage()
#print form

lista = obtemDadosDoFormulario(form)

#print lista

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = str(lista)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data
