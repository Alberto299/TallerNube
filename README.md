# 🌩️ VM Cloud Lab

Repositorio de práctica para el curso **Arquitectura e Infraestructura de
la Nube**. Contiene un servidor mínimo para desplegar en tu propia VM
(Google Cloud o AWS) y notebooks de cliente listos para correr en
**Google Colab**, para que los alumnos practiquen el flujo completo
cliente → Internet → servidor → base de datos → respuesta.

```
vm-cloud-lab/
├── server/                      # Se despliega en la VM del profesor/alumno
│   ├── app.py                   # Servidor FastAPI
│   ├── requirements.txt
│   └── README.md                # Instrucciones de despliegue (GCP/AWS)
└── clients/                     # Se ejecutan en Google Colab
    ├── 01_cliente_basico.ipynb
    ├── 02_cliente_sensor.ipynb
    └── 03_cliente_clasificador.ipynb
```

## ¿Cómo se usa en clase?

1. **El servidor lo levanta una persona** (el profesor, o cada alumno en
   su propia VM) siguiendo `server/README.md`. Esa VM es la que se creó
   con la guía *"Pasos Críticos"* de la presentación (Google Cloud o
   AWS).
2. **Los alumnos abren los notebooks de `clients/`** directamente en
   Google Colab (ver botones abajo), cambian la variable `IP_SERVIDOR`
   por la IP pública del servidor, y ejecutan las celdas.
3. Cada notebook conecta con un concepto distinto de la presentación:
   cliente-servidor, API, base de datos, y cómputo/IA en la nube.

## Abrir los notebooks en Google Colab

Sube este repositorio a tu cuenta de GitHub y reemplaza `TU-USUARIO` en
los enlaces de abajo (o simplemente ábrelos desde Colab con
**Archivo → Abrir notebook → GitHub** y pega la URL del repositorio):

| Notebook | Qué practica | Abrir en Colab |
|---|---|---|
| `01_cliente_basico.ipynb` | GET/POST básicos, la API como "mesero" | `https://colab.research.google.com/github/TU-USUARIO/vm-cloud-lab/blob/main/clients/01_cliente_basico.ipynb` |
| `02_cliente_sensor.ipynb` | Enviar datos de sensores y consultarlos (base de datos) | `https://colab.research.google.com/github/TU-USUARIO/vm-cloud-lab/blob/main/clients/02_cliente_sensor.ipynb` |
| `03_cliente_clasificador.ipynb` | Simular un modelo de IA corriendo en la nube | `https://colab.research.google.com/github/TU-USUARIO/vm-cloud-lab/blob/main/clients/03_cliente_clasificador.ipynb` |

## Requisitos

- Una VM en Google Cloud o AWS con el puerto **8000** abierto (ver la
  diapositiva *"Pasos Críticos"* de la presentación).
- Python 3.10+ en la VM para correr el servidor.
- Una cuenta de Google para abrir los notebooks en Colab (no requiere
  instalar nada localmente).

## Notas de seguridad para el aula

- El servidor de ejemplo **no tiene autenticación** — es solo para
  fines educativos. No lo uses con datos sensibles ni lo dejes corriendo
  fuera de la clase.
- Recuerda **apagar o eliminar la VM** al terminar la sesión para evitar
  cargos inesperados.

## Licencia

MIT — úsalo y modifícalo libremente para tus clases.
