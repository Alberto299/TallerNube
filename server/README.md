# Servidor de práctica

Servidor FastAPI mínimo para desplegar en tu VM de Google Cloud o AWS
(las que creaste siguiendo la guía "Pasos Críticos" de la presentación).

## 1. Conéctate a tu VM por SSH

- **Google Cloud**: botón "SSH" junto a tu instancia en Compute Engine.
- **AWS**: `ssh -i tu-llave.pem ubuntu@TU-IP-PUBLICA`

## 2. Instala Python y clona este repositorio

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git
git clone https://github.com/TU-USUARIO/vm-cloud-lab.git
cd vm-cloud-lab/server
```

## 3. Crea un entorno virtual e instala dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Abre el puerto 8000 en el firewall

- **Google Cloud**: VPC Network → Firewall → Crear regla → permitir TCP:8000
  desde `0.0.0.0/0` (o restringe a tu IP para más seguridad).
- **AWS**: Security Group de tu instancia → Inbound rules → Add rule →
  Custom TCP, puerto 8000, origen `0.0.0.0/0`.

## 5. Ejecuta el servidor

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Déjalo corriendo (o usa `tmux`/`screen`/`nohup` para que siga activo
al cerrar la terminal SSH):

```bash
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

## 6. Prueba que responde

Desde tu propia computadora (no la VM):

```bash
curl http://TU-IP-PUBLICA:8000/health
```

Deberías ver algo como:

```json
{"status": "ok", "uptime_check": 1234567.89}
```

Si responde, ¡tu servidor ya está listo para recibir clientes desde
Google Colab! Comparte tu IP pública con los alumnos y apunta a la
carpeta `clients/` para los notebooks de ejemplo.

## Endpoints disponibles

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/` | Verifica que el servidor está vivo |
| GET | `/health` | Chequeo de salud |
| POST | `/echo` | Envías un mensaje, el servidor lo regresa procesado |
| POST | `/sensor/lectura` | Guarda una lectura de sensor en la base de datos |
| GET | `/sensor/historial` | Consulta las lecturas guardadas |
| POST | `/clasificar` | Simula un modelo de IA clasificando datos |

## Apaga la VM cuando termines

Recuerda apagar o eliminar la instancia al terminar la práctica para
evitar cargos inesperados.
