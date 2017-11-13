#!/usr/bin/env python
import handlepackages
import socket
import cgi
import cgitb
import math


#obtem os dados (maquina, comando, parametros) do formulario da pagina html
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

#converte inteiro para string de binario
#num: numero a converter
#tamanho: tamanho da string de bits
def int_to_binary_str(num, tamanho): 
	temp = bin(num)[2:]
	return temp.zfill(tamanho)

#converte string para string de binario
def str_to_binary_str(string):
	return ''.join('{0:08b}'.format(ord(x), 'b') for x in string)

#montar o pacote dado uma tupla (comando)
#retorna o pacote
def empacota(tupla,source_address_param, dest_address_param):
	version = int_to_binary_str(2,4)
	ihl		= ''	#4 bits
	type_of_service = int_to_binary_str(0,8)
	total_length = ''	#16 bits
	identification = int_to_binary_str(0,16)
	flags	= int_to_binary_str(0,3) 
	frag_offset = int_to_binary_str(0,13)
	time_to_live = int_to_binary_str(0,8)
	protocol = int_to_binary_str(tupla[1],8)
	#header_checksum = int_to_binary_str(0,16)
	source_address = ''	#32 bits
	dest_address = '' #32 bits
	option = str_to_binary_str(tupla[2])
	
	#enderecos
	source_address_aux = source_address_param.split('.')
	dest_address_aux = dest_address_param.split('.')
	for x in source_address_aux:
		source_address = source_address + int_to_binary_str(int(x), 8)
	for x in dest_address_aux:
		dest_address = dest_address + int_to_binary_str(int(x), 8)
	
	#header_checksum 
	header_checksum = handlepackages.calculaChecksum(version+ihl+type_of_service+total_length\
					+identification+flags+frag_offset+time_to_live+protocol\
					+source_address+dest_address)

	#tamanho total do pacote
	tamanho_total = len(version+ihl+type_of_service+total_length\
				+identification+flags+frag_offset+time_to_live\
				+protocol+header_checksum+source_address\
				+dest_address+option)
	#tamanho do ihl, em words
	ihl_value = int(math.ceil(float(tamanho_total)/32))
	
	total_length = int_to_binary_str(tamanho_total,16)
	ihl = int_to_binary_str(ihl_value, 4)
	padding = str_to_binary_str(''.ljust((ihl_value*32 - tamanho_total)/8))

	empacotado = (version+ihl+type_of_service+total_length+identification+flags\
			+frag_offset+time_to_live+protocol+header_checksum+source_address\
			+dest_address+option+padding)

	return empacotado

def desempacota(pacote):
	version = pacote[0:3]
	ihl = pacote[4:7]
	type_of_service = pacote[8:15]
	total_length = pacote[16:31]
	identification = pacote[32:47]
	flags = pacote[48:50]
	frag_offset = pacote[51:63]
	time_to_live = pacote[64:71]
	protocol = pacote[72:79] #verificar
	header_checksum = pacote[80:95]
	source_address = pacote[96:127]
	dest_address = pacote[128:159]
	#option = pacote[]
	#padding = pacote[]

	return (version, ihl, type_of_service, total_length, identification, \
			flags, frag_offset, time_to_live, protocol, header_checksum, \
			source_address, dest_address) #falta option e padding


### main ###

print "Content-Type: text/html;charset=utf-8\r\n\r\n"

cgitb.enable()

form = cgi.FieldStorage()
#print form

lista = obtemDadosDoFormulario(form)

TCP_IP = '127.0.0.1'
TCP_PORT = {1:8001, 2:8002, 3:8003}
BUFFER_SIZE = 1024

for item in lista:
	MESSAGE = handlepackages.empacota(item, TCP_IP, TCP_IP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT[item[0]]))
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	s.close()
	print "received data:", data
