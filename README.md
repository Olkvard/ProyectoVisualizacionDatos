# Dashboard de Estadísticas de Jugadores de Baloncesto 🏀

Este proyecto consiste en un dashboard interactivo que permite visualizar las estadísticas de jugadores de baloncesto a través de gráficos de radar. La aplicación está desarrollada en Python utilizando el framework Dash y se despliega en un entorno web donde puedes filtrar y analizar datos individuales de cada jugador.

## Características 📊

- **Visualización de Radar**: Un gráfico de radar permite visualizar rápidamente las fortalezas y debilidades de cada jugador en diferentes aspectos del juego.
- **Filtros Personalizables**: Selecciona a un jugador específico desde un menú desplegable para ver sus estadísticas en el gráfico.
- **Tabla de Datos**: Muestra todas las estadísticas detalladas de los jugadores en un formato de tabla interactiva.
- **Diseño Intuitivo**: Interfaz limpia y fácil de usar, basada en Bootstrap para un diseño moderno y receptivo.

## Tecnologías Utilizadas 🛠️

- [Dash](https://dash.plotly.com/) y [Plotly](https://plotly.com/python/): Framework para la creación de aplicaciones web en Python.
- [Pandas](https://pandas.pydata.org/): Utilizado para la manipulación y el análisis de los datos de los jugadores.
- [Matplotlib](https://matplotlib.org/): Para generar los gráficos de radar.
- [Bootstrap](https://getbootstrap.com/): Para el diseño y la responsividad de la aplicación.
  
## Estructura de Datos 📝

El archivo de datos `jugadores.xlsx` debe incluir al menos las siguientes columnas para un análisis completo:

- `Nombre`: Nombre del jugador.
- `Minutos Jugados`: Total de minutos jugados por el jugador.
- `Puntos Totales`, `Rebotes Ofensivos`, `Asistencias`, `Tapones Recibidos`, `Pérdidas`, `Recuperaciones`, `Rebotes Defensivos`, `Tapones Cometidos`, `Faltas Personales Recibidas`, `Faltas Personales Cometidas`: Estadísticas de rendimiento individual del jugador.
- `TCP2 (%)`, `TCP3 (%)`, `TCP1 (%)`: Porcentajes de acierto en tiros de campo de dos, tres puntos y tiros libres.

Las métricas **Ataque** y **Defensa** se calculan directamente en el script.

## Instalación 🚀

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/usuario/nombre-del-repo.git
   cd nombre-del-repo
   ```
2. Instala las dependencias: Asegúrate de tener Python 3.7+ y ejecuta:

```bash
pip install -r requirements.txt
```
3. Prepara el archivo de datos: Coloca el archivo jugadores.xlsx con los datos de los jugadores en el directorio raíz del proyecto.

## Uso 📈
Para ejecutar la aplicación, usa el siguiente comando:

```bash
python app.py
```
Luego abre tu navegador en http://127.0.0.1:8050 para ver el dashboard.

## Estructura del Código 📂
- `app.py`: Script principal para ejecutar el dashboard.
- `jugadores.xlsx`: Archivo de datos con las estadísticas de los jugadores.
- `requirements.txt`: Archivo con las dependencias necesarias.

## Funcionalidades del Código ⚙️
- **Gráfico de Radar**: La función radar_chart(player_name) genera un gráfico de radar con cinco métricas clave para cada jugador.
- **Interfaz Dash**: La interfaz permite seleccionar un jugador para visualizar su rendimiento y ver un resumen de todos los jugadores en una tabla interactiva.
- **Callback de Actualización**: El callback de Dash actualiza el gráfico de radar cada vez que se selecciona un jugador diferente.

## Personalización ✨
Puedes ajustar las métricas o columnas en jugadores.xlsx para adaptarlas a nuevas estadísticas o análisis. Además, se pueden agregar más funcionalidades al dashboard o personalizar el estilo mediante ajustes en Dash y Bootstrap.

## Contribución 🤝
¡Las contribuciones son bienvenidas! Para contribuir:

Realiza un fork del proyecto.
Crea una rama con tus cambios (git checkout -b feature/nueva-funcionalidad).
Realiza un commit de tus cambios (git commit -m 'Añadir nueva funcionalidad').
Sube tus cambios (git push origin feature/nueva-funcionalidad).
Abre un Pull Request.
## Licencia 📄
Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto ✉️
Si tienes preguntas o sugerencias, no dudes en contactar con nosotros.

¡Gracias por visitar este proyecto y feliz análisis de estadísticas de baloncesto! 🏀📈
