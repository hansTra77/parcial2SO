### Parcial 2
Universidad ICESI  
Curso: Sistemas Operativos  
Estudiante: Juan Pablo Medina Mora 
Código: 11112010

Link: https://github.com/hansTra77/parcial2SO/


### Instalación de Jenkins

Primero se instalo Jenkins en la maquina virtual siguiendo la guia del profesor.
Se actualiza la fecha del servidor.

```
# yum install ntp ntpdate ntp-doc
# chkconfig ntpd on
# ntpdate pool.ntp.org
# /etc/init.d/ntpd start
```

Con la fecha actualizada se instalan las dependiencias de Jenkins.

```
# yum install java-1.7.0-openjdk
# yum install wget -y
# yum install git -y
# sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
# sudo rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
# sudo yum install jenkins
```

Se abre en el archivo iptables el puerto 8080 sobre el que corre Jenkins.

```
# chkconfig jenkins on
# service jenkins start
# iptables -I INPUT 5 -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
# service iptables save
```

```
# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
```

Se instala virtualenv.

```
# pip install virtualenv
```

Se permite a Jenkins usar la consola, en este caso bash.

```
# vi /etc/passwd
# change for user jenkins /bin/false with /bin/bash
```

Se crea el entorno virtual para las pruebas.

```
# su jenkins
$ mkdir /var/lib/jenkins/.virtualenvs
$ cd /var/lib/jenkins/.virtualenvs
$ virtualenv testproject
$ . testproject/bin/activate
```

Se instalan las dependencias de PYTEST

```
$ pip install xmlrunner
$ pip install unittest2
$ pip install pytest
$ pip install pytest-cov
$ pip install flask
```
Con Jenkins instalado se procede a continuar con el ejercicio propuesto en el parcial.

### Creación del repositorio en GitHub

Se creó el repositorio parcial2SO en el cual posteriormente se usara para configurar el proyecto en Jenkins.

![][1]

### Creación del archivo test_prueba.py

Inicialmente se crea el archivo de pruebas para los métodos de python, esto se realiza por medio del framework pytest.

![][2]

```python
import pytest
import files, json, files_recently

@pytest.fixture
def client(request):
    client = files.app.test_client()
    return client

def test_get_files(client):
	result = client.get('/v1.0/files',follow_redirects=True)
	assert "prueba1" in result.data
	assert "prueba2" in result.data
	
def test_post_create(client):
        nuevo = {'filename': 'casaaaa', 'content': 'esta es una casa'}
	result = client.post('/v1.0/files', data = json.dumps(nuevo), content_type='application/json')
	assert result.status == '200 OK'
	assert get_file_content("casaaaa") == "esta es una casa"

def test_delete_file(client):
	client.delete('/v1.0/files', follow_redirects=True)
	result = client.get('/v1.0/files',follow_redirects=True)
	assert "prueba1" not in result.data
	
def test_get_recents(client):
	result = client.get('/v1.0/files/recently_created',follow_redirects=True)
	assert "pruebaa" in result.data
```

### Creación del archivo run_tests.sh

Este archivo se crea con el propósito de tener un punto de acceso al test que realizamos y que este tenga a su vez los permisos necesarios para realizar los test desde Jenkins.

![][3]

```
#!/usr/bin/env bash
set -e 

. ~/.virtualenvs/testproject/bin/activate

PYTHONPATH=. py.test --junitxml=python_tests.xml
```

Tras crearse el archivo se observaron los permisos del mismo y se modificaron los permisos de forma que se permitiera la ejecución.

```
$ ls -l
$ chmod +x run_test.sh
```
![][4]

### Configuración del servidor de integración continua Jenkins

Se crea un free-style project con el nombre de testParcial. Se usó la configuración que se muestra a continuación.

Es importante recordar poner la url en la que se encuentran los documentos del proyecto en el campo GitHub project.

![][5]
![][6]
![][7]
![][8]
![][9]

### Archivos utilizados para comprobar los test

Se hace uso de los archivos creados en el parcial 1, file_commands.py, files.py, file_res_commands.py y files_recently.py.


```python
from flask import Flask, abort, request
import json

from file_commands import get_all_files, add_file, remove_file

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['POST'])
def create_file():
  content = request.get_json(silent=True)
  filename = content['filename']
  contenido = content['content']
  if not filename:
    return "El archivo no tiene nombre", 400
  if filename in get_all_files():
    return "El archivo ya existe", 400
  if add_file(filename,contenido):
    return "Archivo creado", 201
  else:
    return "Error al crear el archivo", 400

@app.route(api_url+'/files',methods=['GET'])
def list_files():
  list = {}
  list["files"] = get_all_files()
  return json.dumps(list), 200

@app.route(api_url+'/files',methods=['DELETE'])
def delete_files():
  remove_file()
  return 'Todos los archivos se han eliminado correctamente', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=9090,debug='True')
```
```python
from subprocess import Popen, PIPE

def get_all_files():
  ls_process = Popen(["ls","/home/filesystem_user/"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["awk",'-F',' ','{print $1}'], stdin=ls_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  return filter(None,file_list)

def add_file(filename,content):
  contenido = "'"+content+"'"
  nombre = "/home/filesystem_user/"+filename+".txt"
  add_process = Popen(["touch",nombre], stdout=PIPE, stderr=PIPE)
  add_process.wait()
  with open(filename,"W") as fo:
    fo.Write(content)
  return True if filename in get_all_files() else False

def remove_file(filename):
   remove_process = Popen(["rm",'-r',"/home/filesystem_user/*.txt"], stdout=PIPE, stderr=PIPE)
   remove_process.wait()
```
```python
from subprocess import Popen, PIPE

def get_recent_files():
  ls_process = Popen(["ls","/home/filesystem_user/"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["head",'-5'], stdin=ls_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  return filter(None,file_list)
```
```python
from flask import Flask, abort, request
import json

from file_res_commands import get_recent_files

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files/recently_created',methods=['GET'])
def recent_created():
  list = {}
  list["recently created"] = get_recent_files()
  return json.dumps(list), 200
  
if __name__ == "__main__":
  app.run(host='0.0.0.0',port=9191,debug='True')
```
De entre estos archivos el método que se probara será el list_files() del archivo files.py.

### Prueba del test desde consola

Se corre el comando 

```
$ pytest
```

![][10]

### Prueba usando Jenkins

A continuación se procede a realizar la prueba desde la interfaz de Jenkins, Se selecciona el proyecto creado y se oprime en aplicar, esto correrá la prueba.
A continuación, se presenta el resultado.

![][11]
![][12]

Con lo anterior queda completado el parcial 2.

[1]: images/0.JPG
[2]: images/1.JPG
[3]: images/2.JPG
[4]: images/3.JPG
[5]: images/4.JPG
[6]: images/5.JPG
[7]: images/6.JPG
[8]: images/7.JPG
[9]: images/8.JPG
[10]: images/9.JPG
[11]: images/10.JPG
[12]: images/11.JPG
