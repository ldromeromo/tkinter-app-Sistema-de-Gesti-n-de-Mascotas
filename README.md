# Sistema de Gestión de Mascotas

Este sistema permite a los usuarios gestionar información sobre mascotas, incluyendo tipos de animales, recomendaciones de alimentación, y detalles específicos de cada mascota. Se compone de una API desarrollada con Flask y una aplicación de escritorio con Tkinter, que juntas forman una solución integral para clínicas veterinarias o dueños de mascotas que desean mantener un registro detallado de la salud y cuidados de sus animales.

## Características

- **API Flask**: Proporciona endpoints para obtener tipos de animales, recomendaciones nutricionales, y para exportar notas sobre las mascotas en formato Excel.
- **Aplicación de escritorio Tkinter**: Interfaz gráfica para interactuar fácilmente con la API, permitiendo visualizar y modificar detalles de las mascotas, así como agregar o eliminar información.

## Arquitectura SOA (Service-Oriented Architecture)

El proyecto utiliza una arquitectura orientada a servicios (SOA), lo cual significa que la funcionalidad está dividida en servicios independientes que pueden ser consumidos por diferentes clientes. En este caso, la API Flask actúa como un servicio back-end que gestiona la lógica y el acceso a los datos, mientras que la aplicación Tkinter actúa como cliente, consumiendo los servicios proporcionados por la API. Esta separación permite una mayor escalabilidad y flexibilidad, facilitando la integración con otros sistemas y la actualización de componentes de forma independiente.

## Requisitos

- Python 3
- Flask
- Pandas
- Tkinter
- Requests
