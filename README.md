# Django Kanban Board

Una aplicación de gestión de tareas estilo Kanban construida con Django. Permite crear tableros, columnas y tarjetas para organizar proyectos de manera visual.

## Características

*   **Gestión de Tableros**: Crea múltiples tableros para diferentes proyectos.
*   **Columnas Personalizables**: Define los estados de tus tareas (ej. "Por hacer", "En progreso", "Hecho").
*   **Tarjetas Interactivas**: Crea, edita y mueve tarjetas entre columnas.
*   **Interfaz Drag & Drop**: Mueve las tareas fácilmente arrastrándolas.
*   **API REST**: Backend robusto con Django REST Framework.
*   **Autenticación de Usuarios**: Registro e inicio de sesión seguro.

## Requisitos

*   Python 3.8+
*   Django 5.x

## Instalación

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Mario-CS/Django_Kanban.git
    cd Django_Kanban
    ```

2.  **Crear y activar un entorno virtual:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar migraciones:**

    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (opcional):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecutar el servidor:**

    ```bash
    python manage.py runserver
    ```

    Accede a la aplicación en `http://127.0.0.1:8000/`.

## Estructura del Proyecto

*   `kanban/`: Aplicación principal con modelos, vistas y lógica de negocio.
*   `config/`: Configuración del proyecto Django.
*   `templates/`: Plantillas HTML para la interfaz de usuario.
*   `static/`: Archivos CSS y JavaScript.

## Contribuir

1.  Haz un Fork del proyecto.
2.  Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3.  Haz Commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
4.  Haz Push a la rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un Pull Request.
