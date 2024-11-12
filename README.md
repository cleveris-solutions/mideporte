# MiDeporte - Proyecto de Reservas de Pistas Deportivas

Proyecto pensado para la reserva de pistas para el municipio de Villanueva de las Cruces. Desarrollado con Django y React como tecnologías principales.

Proyecto desarrollado por Cleveris Solutions.

## Requisitos

- Python 3.x
- Node.js y npm (para el frontend con React)
- Django y otras dependencias listadas en `requirements.txt`

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/cleveris-solutions/mideporte.git
cd mideporte
```

### 2. Entorno virtual
#### 2.1 Crear y activar el entorno virtual
```bash
python3 -m venv venv
En linux: source venv/bin/activate  
En Windows: venv\Scripts\activate
```

#### 2.2 Instalar dependencias del entorno virtual
```bash
pip install -r requirements.txt
```

### 3. Configurar MariaDB
#### 3.1 En Ubuntu
```bash
sudo apt install mariadb-server -y
sudo systemctl start mariadb
sudo mysql_secure_installation
```
Valores a introducir tras ejecutar el comando `mysql_secure_installation`:
```bash
- Enter current password for root (enter for none): (enter)
- Switch to unix_socket authentication [Y/n]: `y`
- Change the root password? [Y/n]: `y`
    - New password: <tu_contraseña_de_root>
    - Re-enter new password: <tu_contraseña_de_root>
- Remove anonymous users? [Y/n]: `y`
- Disallow root login remotely? [Y/n]: `y` 
- Remove test database and access to it? [Y/n]: `y`
- Reload privilege tables now? [Y/n] : `y`
```
A continuación, para continuar con la creación de la base de datos:
```bash
sudo mariabd -u root -p
```
Usar la contraseña de root que se ha configurado anteriormente. Una vez dentro de la consola de MariaDB, para crear las bases de datos ejecutar el siguiente comando:
```sql
source resources/mariadb.sql;
```

#### 3.2 En Windows
Descargar MariaDB de la página oficial y configurar el superusuario root durante la instalación. A continuación, abrir una terminal en el directorio base del proyecto (mideporte) y ejecutar el siguiente comando:
```bash
mariadb -u root -p
```
Nota: Si no se reconoce el comando `mariadb`, añadir la ruta de instalación de MariaDB al PATH del sistema.

(Opcional) Si se desea realizar una instalación segura igual que en Ubuntu, ejecutar las siguientes sentencias SQL:
```sql
DELETE FROM mysql.user WHERE User='';
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
```	
Para crear las bases de datos, ejecutar el siguiente comando:
```sql
source resources/mariadb.sql;
```
#### 3.3 Migraciones
Crear las migraciones que reflejan los cambios en los modelos de la base de datos. No es necesario ejecutar este comando si no se han realizado cambios en los modelso desde la última vez que se ejecutó:
```bash
python manage.py makemigrations
```
Aplicar las migraciones a la base de datos:
```bash
python manage.py migrate
```

### 4. Iniciar el servidor de backend
```bash
cd backend
python manage.py runserver
```
El backend debe arrancarse en el puerto 7777

### 5. Instalar e iniciar el servidor de frontend
```bash
cd frontend
npm install
npm start
```
El frontend debe arrancarse en el puerto 3000. Si se quiere modificar se ha de añadir la variable de entorno: *PORT=<xxxx>* al fichero *./frontend/.env*


### 6. Variables de entorno
De momento no existen variables de entorno del proyecto global. De todas formas, para generar el archivos .env realizar lo siguiente:
```bash
cp .env.example .env
```

## Documentación de la API
La API está documentada usando drf-spectacular. Puedes acceder a la documentación en los siguientes endpoints:

- Swagger: http://127.0.0.1:7777/api/docs/swagger/
- Redoc: http://127.0.0.1:7777/api/docs/redoc/