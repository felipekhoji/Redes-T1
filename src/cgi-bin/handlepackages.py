import math
#calcula o checksum de um pacote de ate 256 bits, somando de 16 em 16 bits
#lembrando que o checksum eh feito apenas no cabecalho do pacote, desconsiderando o proprio campo checksum (o parametro deve ser um binario com 144 bits)
def calculaChecksum(pacote):
	pacote = pacote.zfill(256)
        nOctetos = len(pacote) / 16

        checksum = 0
        for i in range(0, nOctetos):
                checksum = checksum + int(pacote[i*16:i*16+16],2)
                carry = checksum - checksum % 65536
                while(carry != 0): #soma o carry
                        checksum = checksum % 65536
                        checksum = checksum + 1
                        carry = checksum - checksum % 65536
        #inverte bits
        checksum = checksum ^ 0xFFFF

        return bin(checksum)[2:].zfill(16)
###
#verifica o checksum
def verificaChecksum(pacote):
	#campo header_checksum
	pacote = pacote.zfill(256)
	checksum = pacote[96+80:96+96]
	pacote = pacote[:96+80] + pacote[96+96:]
	if calculaChecksum(pacote) == checksum:
		return True
	else: 
		return False
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
	ihl		= '0000'	#4 bits
	type_of_service = int_to_binary_str(0,8)
	total_length = '0000000000000000'	#16 bits
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
	header_checksum = calculaChecksum(version+ihl+type_of_service+total_length\
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

#Desempacota o pacote (string de binarios) e converte para inteiros na base decimal
def desempacota(pacote):
	version = int(pacote[0:4], 2)
	ihl = int(pacote[4:8], 2)
	type_of_service = int(pacote[8:16], 2)
	total_length = int(pacote[16:32], 2)
	identification = int(pacote[32:48], 2)
	flags = int(pacote[48:51], 2)
	frag_offset = int(pacote[51:64], 2)
	time_to_live = int(pacote[64:72], 2)
	protocol = pacote[72:80] #verificar
	header_checksum = int(pacote[80:96], 2)
	source_address = int(pacote[96:128],2)
	dest_address = int(pacote[128:160], 2)
	option = pacote[160:total_length]
	#padding = pacote[] - irrelevante

	return (version, ihl, type_of_service, total_length, identification, \
			flags, frag_offset, time_to_live, protocol, header_checksum, \
			source_address, dest_address, option) 
