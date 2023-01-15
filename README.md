# Nombre Proyecto: MODULO ADMIN

### Descripción


Al ser un proyecto en Python, se siguen las siguientes convenciones:

### Construcción 🛠️
* **Tipo:** App Engine
* **Lenguaje:** Python 3
* **Framework:** Flask, SqlAlchemy

### Pre-requisitos 📋

- Docker.
- Docker-compose.

### Instalación 🔧

- Clonar proyecto.
- Crear archivo `.env` en la carpeta raíz. Se incluye archivo `.env.example` como referencia, que se puede usar tal cual como está.
- Ejecutar `docker-compose build` para construir las imágenes de Docker. Sólo es necesario hacerlo una vez.
- Ejecutar `docker-compose up` para levantar los servicios.
- Crear la base de datos `users`, nose adjunta script debido a que la tabla se genera automaticamente al levantar el docker

### Autores ✒️

**Autor:** Darwin Acuña,       darwin182008@gmail.com
