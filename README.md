# Invera ToDo-List Challenge

## Objetivo

El presente repositorio ofrece una solución desarrollada en Python para el desafío propuesto por Invera, con el objetivo
de crear el backend de una aplicación de gestión de tareas, utilizando Django.

## Stack tecnólogico

Para la elaboración de la presente aplicación, se utilizaron las siguientes tecnologías:

- [Python](https://www.python.org/): como lenguaje de desarrollo.
- [Django](https://www.djangoproject.com/): framework web para la construcción del backend.
- [Django REST Framework](https://www.django-rest-framework.org/): meta-framework construído sobre Django, para falicitar la creación de API REST.
- [SQLite](https://www.sqlite.org/): como base de datos simplificada.
- [JSON Web Token](https://jwt.io/): como método de autenticación a través de la emisión de tokens certificados.
- [logging](https://docs.python.org/3/library/logging.html) y [unittest](https://docs.python.org/3/library/unittest.html): como librerías de gestión de logs y de pruebas unitarias/integración para la aplicación, a través de la API provistas por los frameworks antes mencionados.

## Despliegue

1. Crear un entorno virtual de Python:

```bash
python -m venv .venv
```

2. Activar el entorno virtual, [según la terminal](https://docs.python.org/es/3/library/venv.html#how-venvs-work) en que se esté ejecutando:

```bash
# Ejemplo para bash en Windows
source .venv/bin/activate
```

3. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

4. Setear la variables de entorno, ya sea en un archivo `.env` (siguiendo de ejemplo a [.env.example](./.env.example)) o a través de las variables del sistema operativo:

5. Generar las migraciones a la base de datos:

```bash
python manage.py migrate
```

6. Crear un super usuario para la aplicación (que permita el login):

```bash
python manage.py createsuperuser
```

Completando los campos solicitados por consola (nombre, email, password).

7. Ejecutar el servidor provisto por Django:

```bash
python manage.py runserver
```

El comando mostrará la URL (HOST + PORT) en la que está corriendo el proceso, ej.: `http://127.0.0.1:8000/`.

8. Utilizar un cliente REST para realizar el login y luego los requests a los endpoints definidos.

## Testing

Para revisar los resultados de los tests definidos, ejecutar el siguiente comando:

```bash
python manage.py test
```
