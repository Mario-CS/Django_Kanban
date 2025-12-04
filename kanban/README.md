# Django Kanban Board

Aplicación Django de tablero Kanban moderno con drag & drop, diseño responsive y soporte táctil para móviles.

## Características

✨ **Funcionalidades principales:**
- 🎯 Drag & drop para mover tarjetas entre columnas (desktop y móvil)
- ➕ Crear nuevas tarjetas con modal de edición
- ✏️ Editar tarjetas haciendo clic en ellas
- 🗑️ Eliminar tarjetas individuales o todas a la vez
- ⬆️⬇️ Reordenar tarjetas con botones up/down
- 📊 Contadores de tarjetas por columna y total
- 🎨 Diseño moderno con gradientes y animaciones
- 📱 Responsive design optimizado para móviles
- 👆 Soporte completo para eventos táctiles

## Requisitos
- Python 3.10+
- Django 5.2+

## Instalación en un proyecto nuevo

### 1. Copiar la aplicación kanban

Copia la carpeta `kanban/` completa a tu proyecto Django:

```bash
cp -r kanban/ /ruta/a/tu/proyecto/
```

### 2. Configurar settings.py

Añade `kanban` a tus INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kanban',  # ← Añadir aquí
]
```

### 3. Configurar URLs

En tu archivo principal de URLs (ej: `config/urls.py` o `proyecto/urls.py`):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kanban.urls')),      # ← Vistas del Kanban
    path('api/', include('kanban.api_urls')),  # ← API endpoints
]
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations kanban
python manage.py migrate
```

### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

### 7. Crear tablero y columnas

Accede al admin en http://127.0.0.1:8000/admin/ y crea:

1. Un **Board** (tablero)
2. **Columnas** para ese tablero (ej: "To Do", "Working", "Done")
3. Opcionalmente asigna colores a las columnas en formato hex (ej: `#2a92bf`)

O usa el script de datos de prueba (ver sección "Crear datos de prueba" más abajo).

## Instalación en este proyecto

```bash
# 1) Activar entorno virtual
source .venv/bin/activate

# 2) Ejecutar servidor (ya instalado y migrado)
python manage.py runserver
```

## Crear datos de prueba

```bash
# Generar tablero con tarjetas de ejemplo
python create_sample_data.py
```

## Acceso

- **Lista de tableros**: http://127.0.0.1:8000/
- **Tablero ejemplo**: http://127.0.0.1:8000/board/1/

## Estructura del proyecto

```
Django_proyect/
├── config/              # Configuración del proyecto (antes kanban_project)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── kanban/              # App principal del Kanban
│   ├── models.py        # Board, Column, Card
│   ├── views.py         # Vistas + API endpoints
│   ├── urls.py          # Rutas
│   ├── admin.py
│   ├── static/
│   │   └── kanban/
│   │       ├── css/
│   │       │   └── kanban.css    # Estilos del tablero
│   │       └── js/
│   │           └── kanban.js     # Drag & drop + CRUD
│   └── templates/
│       └── kanban/
│           ├── board_list.html
│           └── kanban_board.html # Template principal
├── manage.py
├── requirements.txt
└── create_sample_data.py
```

## API Endpoints

- `POST /api/board/<board_id>/card/create/` - Crear tarjeta
- `PUT /api/card/<card_id>/update/` - Actualizar tarjeta
- `POST /api/card/<card_id>/move/` - Mover tarjeta
- `DELETE /api/card/<card_id>/delete/` - Eliminar tarjeta

## Uso

### Crear nueva tarjeta
1. Clic en botón "+" (NEW TASK)
2. Se abre modal automáticamente
3. Escribe descripción y clic en "Ok"

### Editar tarjeta
- Clic en el texto de la tarjeta
- Modifica en el modal y guarda

### Mover tarjeta
- Arrastra y suelta en otra columna
- O usa botones ⬆️ ⬇️ para reordenar

### Eliminar tarjeta
- Clic en icono 🗑️ de la tarjeta
- O arrastra a zona "ARRASTRA AQUÍ"

## Admin

Accede al admin de Django para gestionar tableros y columnas:

```bash
# Crear superusuario
python manage.py createsuperuser

# Acceder
http://127.0.0.1:8000/admin/
```

## Personalización

### Colores (en `kanban/static/kanban/css/kanban.css`)

```css
:root {
    --icon-new-task: #2a92bf;    /* To Do */
    --list-working: #ffc000;      /* Working */
    --list-done: #00b91f;         /* Done */
    --icon-remove: #ff6347;       /* Delete */
    --dark-color: #282828;        /* Header */
}
```

### Añadir más columnas

```python
# En el admin o shell
from kanban.models import Board, Column
board = Board.objects.get(id=1)
Column.objects.create(board=board, name="En Revisión", position=2)
```
