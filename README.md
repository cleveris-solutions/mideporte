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

### 2. Configurar el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  
# En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias del entorno virtual
```bash
pip install -r requirements.txt
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