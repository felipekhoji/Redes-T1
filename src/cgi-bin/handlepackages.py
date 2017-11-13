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
	version = int(pacote[0:3], 2)
	ihl = int(pacote[4:7], 2)
	type_of_service = int(pacote[8:15], 2)
	total_length = int(pacote[16:31], 2)
	identification = int(pacote[32:47], 2)
	flags = int(pacote[48:50], 2)
	frag_offset = int(pacote[51:63], 2)
	time_to_live = int(pacote[64:71], 2)
	protocol = pacote[72:79] #verificar
	header_checksum = int(pacote[80:95], 2)
	source_address = int(pacote[96:127],2)
	dest_address = int(pacote[128:159], 2)
	#option = pacote[]
	#padding = pacote[]

	return (version, ihl, type_of_service, total_length, identification, \
			flags, frag_offset, time_to_live, protocol, header_checksum, \
			source_address, dest_address) #falta option e padding
