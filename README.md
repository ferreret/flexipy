# FlexiPy - Arquitectura del Proyecto

FlexiPy es un sistema de procesamiento de documentos diseñado para ofrecer dos arquitecturas distintas, dependiendo de la complejidad y las necesidades del usuario. Ambas versiones comparten algunos módulos comunes para garantizar una base de código reutilizable y eficiente.

## 🏆 FlexiPy Lite
**FlexiPy Lite** es una aplicación de escritorio sencilla construida con **Python y PySide6**. Su propósito es proporcionar una solución liviana y rápida para la gestión y visualización de documentos sin depender de servicios adicionales.

### Características principales:
- Aplicación de escritorio autónoma basada en **PySide6**.
- Interfaz gráfica intuitiva para la gestión de documentos.
- No requiere base de datos ni servidores adicionales.
- Ideal para usuarios individuales o pequeñas empresas con requisitos básicos de procesamiento de documentos.

## 🚀 FlexiPy Advanced
**FlexiPy Advanced** es una solución más robusta y escalable diseñada para manejar grandes volúmenes de documentos y procesamiento automatizado en segundo plano. Incluye los siguientes componentes:

### Componentes principales:
1. **Aplicación de escritorio con PySide6:**
   - Similar a FlexiPy Lite, pero con más funcionalidades avanzadas.
   - Interfaz mejorada para la gestión de lotes de documentos.
   
2. **API con FastAPI:**
   - Proporciona una API REST para gestionar lotes de documentos.
   - Permite la integración con otros sistemas mediante endpoints bien estructurados.
   - Conexión a una base de datos para almacenar información sobre los documentos procesados.
   
3. **Servicio de procesamiento en segundo plano:**
   - Utiliza **Watchdog** para detectar cambios en directorios de lotes de documentos.
   - Emplea **multiprocessing** para ejecutar tareas en paralelo y optimizar el procesamiento de grandes volúmenes de datos.
   - Se activa automáticamente cuando hay documentos pendientes, asegurando un procesamiento eficiente sin intervención manual.

## 📂 Estructura del Proyecto
La arquitectura del proyecto ha sido diseñada para ser modular y reutilizable.

```
FlexiPy/
│── common/                 # 📌 Módulos compartidos entre Lite y Advanced
│   ├── logging_config/     # Configuración de logs
│   ├── utils/              # Utilidades comunes (helpers, validaciones, etc.)
│   ├── models/             # Modelos de datos compartidos
│   ├── config.py           # Configuración global (carga de variables de entorno)
│   ├── database.py         # Conexión a la base de datos (si se usa en ambas versiones)
│   ├── __init__.py         
│
│── lite/                   # 📌 FlexiPy Lite (solo escritorio con PySide6)
│   ├── app/                # Aplicación de escritorio
│   │   ├── ui/             # Archivos de UI (QML/PyQt/PySide6)
│   │   ├── controllers/    # Controladores de la UI
│   │   ├── models/         # Modelos de la aplicación
│   │   ├── views/          # Vistas
│   │   ├── main.py         # Punto de entrada de la aplicación
│   │   ├── __init__.py     
│   ├── resources/          # Archivos estáticos (iconos, imágenes)
│   ├── tests/              # Pruebas unitarias
│   ├── README.md           
│   ├── requirements.txt    # Dependencias específicas de Lite
│
│── advanced/               # 📌 FlexiPy Advanced
│   ├── desktop/            # Aplicación de escritorio con PySide6
│   ├── api/                # API con FastAPI
│   ├── service/            # Servicio de monitorización de lotes
│   │   ├── watchdog_monitor.py  # Monitorización con Watchdog
│   │   ├── batch_processor.py   # Procesamiento de lotes
│   ├── tests/              # Pruebas para API, escritorio y servicio
│   ├── requirements.txt    # Dependencias de Advanced
│
│── docs/                   # 📌 Documentación del proyecto
│   ├── lite/               # Documentación de FlexiPy Lite
│   ├── advanced/           # Documentación de FlexiPy Advanced
│   ├── setup_guide.md      # Guía de instalación y configuración
│   ├── api_docs.md         # Documentación de la API
│
│── scripts/                # 📌 Scripts útiles
│   ├── setup_env.py        # Configurar variables de entorno
│   ├── start_lite.sh       # Iniciar FlexiPy Lite
│   ├── start_advanced.sh   # Iniciar FlexiPy Advanced
│
│── .gitignore              # Archivos a ignorar en el repositorio
│── pyproject.toml          # Configuración de dependencias (si usas Poetry)
│── README.md               # Documentación general del proyecto
```

## 🔥 Instalación y Configuración
### Requisitos previos
- **Python 3.9+**
- **pip** (o Poetry si prefieres gestionar dependencias de manera avanzada)
- **Virtualenv** (recomendado para entornos aislados)

### Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-repo/FlexiPy.git
   cd FlexiPy
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate   # En Windows
   ```

3. Instalar dependencias según la versión que desees ejecutar:
   ```bash
   pip install -r lite/requirements.txt  # Para FlexiPy Lite
   pip install -r advanced/requirements.txt  # Para FlexiPy Advanced
   ```

## 🚀 Uso
### FlexiPy Lite
Para ejecutar la versión Lite:
```bash
python lite/app/main.py
```

### FlexiPy Advanced
Para iniciar la API y el servicio de procesamiento de lotes:
```bash
./scripts/start_advanced.sh
```

## 📌 Contribución
Si deseas colaborar en el proyecto, revisa `docs/contributing.md` para conocer las pautas de desarrollo y estándares de código.

## 📜 Licencia
Este proyecto se encuentra bajo la licencia **MIT**.

---

💡 **FlexiPy** es desarrollado por Nicolás Barceló Lozano y está en constante evolución para mejorar el procesamiento de documentos de manera eficiente y escalable.


