### Parcial 2
Universidad ICESI  
Curso: Sistemas Operativos  
Estudiante: Juan Pablo Medina Mora 
Código: 11112010

Link: https://github.com/hansTra77/parcial2SO/

### Creacion del repositorio en Github

Se creo el repositorio parcial2SO en el cual posteriormente se usara para configurar el proyecto en Jenkins.

### Creación del archivo test.py

Inicialmente se crea el archivo de pruebas para los metodos de python, esto se realiza por medio del framework pytest.



### Creacion del archivo run_tests.sh

Este archivo se crea con el proposito de tener un punto de acceso al test que realizamos y que este tenga a su vez los permisos necesarios para realizar los test desde Jenkins.

### Configuracion del servidor de integracion continua Jenkins

Se crea un free-style project con el nombre de testParcial. Se uso la configuracion que se muestra a continuacion.

Es importante recordar poner la url en la que se encuentran los documentos dell proyecto en el campo GitHub project.

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
De entre estos archivos el metodo que se probara sera el list_files() del archivo files.py.

### Prueba del test desde consola

Se corre el comando 

```
$ pytest
```

### Prueba usando Jenkins

A continuacion se procede a realizar la prueba desde la interfaz de Jenkins, Se selecciona el proyecto creado y se oprime en aplicar, esto correra la prueba.
A continuacion, se presenta el resultado.



