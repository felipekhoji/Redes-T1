# Redes-T1

# Servidor de consultas Linux

### Descrição do projeto

O projeto desenvolvido permite que um usuário possa inserir instruções numa página na web para que um aplicativo backend em python se
conecte a um conjunto de daemons que estão sendo executados por três máquinas. Em seguida, cada máquina remota receberá os comandos a serem executados localmente por cada máquina correspondente. Por fim, os resultados são exibidos numa página de web criada pelo backend.

### Configurando o ambiente

* Primeiramente, é necessário editar o arquivo ***apache2.conf***  por meio de `sudo vi /etc/apache2/apache2.conf`e mudar o caminho do diretório
 para ser o caminho **<.../src/>** do projeto

* Em seguida, inserir a linha: **ScriptAlias "cgi-bin" ".../cgi-bin/"**
 e mudar o caminho do diretório para **<.../cgi-bin/>** do projeto

* Depois disso, modificar o arquivo **000-default.conf** usando `sudo vi /etc/apache2/sites-avaiable/000-default.conf`
 alterando o caminho do diretório em **DocumentRoot** para o caminho onde de encontra o html do projeto: **.../src/html**

* Para finalizar, deve-se **reiniciar** o apache2 por meio de
`sudo service apache2 restart`

## Contribuidores

* [Felipe Myose](https://github.com/felipekhoji)
* [Nicole Zafalon Kovacs](https://github.com/nicolezk1)
* [Leonardo Cristovão](https://github.com/LeoCristovao)

