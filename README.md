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

Variables de entorno:
```bash
cp .env.example .env
```

### 2. Entorno virtual
#### 2.1 Crear el entorno virtual
```bash
python3 -m venv venv
```
#### Activar el entorno virtual
En linux: 
```bash
source venv/bin/activate  
```
O en Windows: 

```bash
venv\Scripts\activate
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
sudo mariadb -u root -p
```
Usar la contraseña de root que se ha configurado anteriormente. Una vez dentro de la consola de MariaDB, para crear las bases de datos ejecutar el siguiente comando:
```sql
source resources/database.sql;
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
source resources/database.sql;
```
#### 3.3 Migraciones
Crear las migraciones que reflejan los cambios en los modelos de la base de datos. No es necesario ejecutar este comando si no se han realizado cambios en los modelos desde la última vez que se ejecutó:
```bash
cd backend
python manage.py makemigrations
```
Nota: es posible que si aun no se han creado las carpetas de migration dentro de las aplicaciones de Django, se deba ejecutar el comando makemigrations especificando una por una las aplicaciones:
```bash
python manage.py makemigrations user installation booking
```
Aplicar las migraciones a la base de datos:
```bash
python manage.py migrate
```

Nota: durante la ejecución de `manage.py` migrate puede aparecer un error `Table 'django_admin_log' already exists`. Para solucionarlo, seguir los siguientes pasos:
```bash
mariadb -u root -p
DROP TABLE django_admin_log;
source resources/database.sql;
exit;
python manage.py migrate
```

#### 3.4 Popular la base de datos
```bash
python populate_db.py
```

### 4. Iniciar el servidor de backend
```bash
python manage.py runserver
```
El backend debe arrancarse en el puerto 7777

#### 4.1 Crear un superusuario
Para acceder al panel de administración de Django, es necesario crear un superusuario. Para ello, ejecutar el siguiente comando:
```bash
python manage.py createsuperuser
```
El comando como respuesta pedirá que se introduzcan los siguientes datos:
```bash
DNI: <tu_dni>
password: <tu_contraseña>
```
El panel de administración de Django se encuentra en la siguiente dirección: http://127.0.0.1:7777/admin/

Al crear un superusuario solo le da valor a las dos propiedades de User mencionadas anteriormente. Para configurar más atributos de User, se ha de acceder al panel de administración de Django y modificar el usuario creado. También se puede modificar un usuario ya creado y hacerlo superusuario.


### 5. Instalar e iniciar el servidor de frontend
```bash
cd frontend
npm install
npm start
```
El frontend debe arrancarse en el puerto 3000. Si se quiere modificar se ha de añadir la variable de entorno: *PORT=<xxxx>* al fichero *./frontend/.env*

### 6. Estructura de carpetas

- **`mideporte/`**: Directorio raíz del proyecto.
  - **`backend/`**: Contiene el código del backend de Django.
  - **`frontend/`**: Contiene el código del frontend de React.
  - **`docs/`**: Documentación del proyecto.
    - **`Mockups/`**: Mockups de las pantallas de la aplicación.
    - **`UML/`**: Diagramas UML del proyecto.
  - **`resources/`**: Recursos necesarios para la configuración de la base de datos.
  - **`Selenium_tests/`**: Tests de Selenium para el frontend.
  - **`README.md`**: Documentación del proyecto.
  - **`.gitignore`**: Archivo de configuración de Git.
  - **`requirements.txt`**: Archivo con las dependencias de Python.
  - **`.env.example`**: Archivo de ejemplo para las variables de entorno.
  - **`LICENSE`**: Licencia del proyecto.

#### 6.1. Estructura de carpetas del backend
El backend está organizado por aplicaciones que engloban funcionalidades relacionadas:
- **`user/`**: Aplicación para la gestión de usuarios.
- **`installation/`**: Aplicación para la gestión de instalaciones deportivas.
- **`booking/`**: Aplicación para la gestión de reservas.
- **`main/`**: Aplicación que contiene la configuración de Django y las URL base del la aplicación.

Además de las aplicaciones, el backend contiene los siguientes archivos y carpetas:
- **`media`**: Carpeta donde se almacenan los archivos multimedia subidos por los usuarios.
- **`manage.py`**: Archivo de Django para la gestión del proyecto que se usará para ejecutar comandos desde la terminal.
- **`populate_db.py`**: Script para poblar la base de datos.

Las aplicaciones tienen la siguiete estructura:
- **`migrations/`**: Carpeta con las migraciones de la aplicación generadas por Django.
- **`fixtures/`**: Carpeta con los datos de prueba de la aplicación para la población inicial.
- **`validators/`**: Carpeta con los validadores personalizados de la aplicación.
- **`admin.py`**: Archivo de Django para la configuración del panel de administración en el que se incluyen los modelos que podrán ser listados y modificables.
- **`apps.py`**: Archivo de Django para la configuración base de la aplicación.
- **`models.py`**: Archivo de Django donde se definen los modelos de la aplicación que se guardarán en la base de datos.
- **`serializers.py`**: Archivo de Django donde se definen los serializadores de los modelos de la aplicación que transforman un objeto de Django a JSON.
- **`tests.py`**: Archivo de Django donde se definen los tests unitarios de la aplicación.
- **`urls.py`**: Archivo de Django donde se definen las URL de la aplicación. Las URLs que se definan aquí se pondrán después de la ruta establecida en urls.py en `main.py` para la aplicación.
- **`views.py`**: Archivo de Django donde se definen las vistas de la aplicación. Las vistas son las funciones que se ejecutan cuando se accede a una URL de la aplicación y que contienen la lógica de negocio.

#### 6.2. Estructura de carpetas del frontend
El frontend está construido con React y está organizado en las siguientes carpetas y archivos:
- **`public/`**: Carpeta con los archivos estáticos del frontend que aparecerán en la web incluso antes de autenticarse.
- **`src/`**: Carpeta con los archivos de código fuente del frontend.
- **`.env.example`**: Archivo de ejemplo para las variables de entorno de React.
- **`README.md`**: Documentación del frontend autogenerada por Create React App.
- **`package.json`**: Archivo de configuración de Node.js con las dependencias del frontend.

La carpeta `src/` contiene las siguientes carpetas y archivos:
- **`assets/`**: Carpeta con los archivos multimedia del frontend.
- **`auth/`**: Carpeta quecontiene la lógica de autenticación de la aplicación.
- **`components/`**: Carpeta con los componentes de React reutilizables de la aplicación.
- **`screens/`**: Carpeta con las pantallas de la aplicación.
- **`utils/`**: Carpeta con funciones auxiliares de la aplicación.
- **`App.js`**: Archivo principal de React que contiene la estructura de la aplicación.
- **`App.css`**: Archivo de estilos de la aplicación.
- **`App.test.js`**: Archivo de tests de la aplicación autogenerado por React.
- **`index.js`**: Archivo de React que renderiza la aplicación en el DOM.
- **`index.css`**: Archivo de estilos global de la aplicación.
- **`logo.svg`**: Archivo de imagen autogenerado por Create React App.
- **`reportWebVitals.js`**: Archivo de React para medir el rendimiento de la aplicación.
- **`setupTests.js`**: Archivo de configuración de tests autogenerado por React.



### 7. Variables de entorno
En MiDeporte se utilizan variables de entorno para configurar únicamente el entorno de pruebas del frontend con Selenium. Para ello, se ha de copiar el fichero `.env.example` a `.env` y modificar las variables para adaptarlas al entorno de ejecución.

Será necesario además tener instalado en el sistema el driver de Chrome para Selenium. 
```bash
CHROMEDRIVER_BIN_PATH=""
DNI_EXAMPLE=""
FRONTEND_DOMAIN=""
FRONTEND_PORT=""
FRONTEND_PROTOCOL=""
FRONTEND_ENDPOINT="${FRONTEND_PROTOCOL}://${FRONTEND_DOMAIN}:${FRONTEND_PORT}"
```

Un ejemplo de configuración (en Linux):
```bash
CHROMEDRIVER_BIN_PATH="/usr/bin/chromedriver"
DNI_EXAMPLE="12345678A"
FRONTEND_DOMAIN="localhost"
FRONTEND_PORT="3000"
FRONTEND_PROTOCOL="http"
FRONTEND_ENDPOINT="${FRONTEND_PROTOCOL}://${FRONTEND_DOMAIN}:${FRONTEND_PORT}"
```

### 8. Ejecución de tests
#### 8.1. Tests de Django
Para ejecutar los tests de Django, ejecutar el siguiente comando en el directorio `backend`:
```bash
python manage.py test
```

#### 8.2. Test de Selenium
Para ejecutar los tests de Selenium, ejecutar el siguiente comando en el directorio raíz del proyecto:
```bash
python selenium_tests/run.py 
```


## Documentación de la API
La API está documentada usando drf-spectacular. Puedes acceder a la documentación en los siguientes endpoints (es necesario tener el servidor de backend en ejecución):

- Swagger: http://127.0.0.1:7777/api/docs/swagger/
- Redoc: http://127.0.0.1:7777/api/docs/redoc/