# Taller1_MLOPS_PENGUINS
Taller de contenedores de docker y FastAPI para clase operación de aprendizaje de máquina

## Configuración inicial

Para empezar se debe clonar el repositorio en el equipo o máquina utilizada. Para ello ejecutamos:

`git clone https://github.com/massimomg2/Taller1_MLOPS_PENGUINS.git`

Después se debe ejecutar el archivo que entrena los modelos (no hacer si antes haber instalado librerías con `pip install -r requirements.txt`)

`Python Modelos/modelomlops.py`

Posterior a eso podemos crear la imagen de docker como sigue:

`docker build -f Docker/Dockerfile --tag penguins_api .`

Una vez que se construya, se construye el contenedor de docker como tal

`docker run -p 8989:8989 penguins`

Y listo, con esto ya queda expuesto el servidor a la URL `http://localhost:8989/` con su método POST `/pred`.
