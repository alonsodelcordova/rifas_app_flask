# RIFAS APP

## Requerimientos

- Python 3.x
- Pip

## Instalación

1. Clona el repositorio.
2. Ejecuta `pip install -r requirements.txt` para instalar las dependencias.

## Uso

1. Ejecuta `flask run` para iniciar el servidor.
2. Abre tu navegador y ve a `http://localhost:5000`.
3. Inicia sesión con tu usuario y contraseña.
4. Si no tienes usuario, puedes crear uno con el botón "Register".
5. Si tienes permisos de administrador, puedes acceder a la página de administración con el botón "Admin".
6. Si no tienes permisos de administrador, no podrás acceder a la página de administración.

## Comandos Flask

flask run: Inicia el servidor.
flask shell: Inicia un intérprete interactivo.

## Comandos Flask-Migrate
```bash
- flask db init: Inicializa un repositorio de migraciones en tu proyecto.
- flask db migrate -m "show": Detecta cambios en los modelos y crea un nuevo script de migración.
- flask db upgrade: Aplica la migración más reciente a la base de datos.
- flask db downgrade: Revierte la última migración aplicada.
- flask db show [ID]: Muestra detalles de una migración específica.
```


## Roles
### 👤 CLIENT (cliente)
- Ver rifas públicas
- Ver detalles de una rifa
- Comprar números
- Ver sus compras
- Ver ganador
- Descargar comprobante (opcional)

### 🧑‍💼 SELLER (vendedor / organizador)
- Crear rifas
- Definir precios y cantidad de números
- Ver ventas
- Confirmar pagos (si aplica)
- Ver ganador
- Descargar acta


## rutas
| Función            | Client | Seller | Admin |
| ------------------ | :----: | :----: | :---: |
| Ver rifas          |    ✅   |    ✅   |   ✅   |
| Comprar números    |    ✅   |    ❌   |   ❌   |
| Ver mis compras    |    ✅   |    ❌   |   ❌   |
| Subir comprobante  |    ✅   |    ❌   |   ❌   |
| Crear rifa         |    ❌   |    ✅   |   ❌   |
| Publicar rifa      |    ❌   |    ✅   |   ❌   |
| Ver ventas         |    ❌   |    ✅   |   ✅   |
| Confirmar pagos    |    ❌   |    ✅   |   ✅   |
| Ejecutar sorteo    |    ❌   |    ❌   |   ✅   |
| Ver ganador        |    ✅   |    ✅   |   ✅   |
| Descargar acta     |    ❌   |    ✅   |   ✅   |
| Gestionar usuarios |    ❌   |    ❌   |   ✅   |

