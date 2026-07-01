"""
Servidor de práctica — Arquitectura e Infraestructura de la Nube
------------------------------------------------------------------
Un servidor mínimo pensado para desplegarse en una VM de Google Cloud
o AWS y ser consumido desde clientes escritos en Google Colab.

Cada endpoint ilustra un concepto visto en la presentación:

  GET  /                -> Cliente-Servidor básico ("¿Hay alguien ahí?")
  GET  /health          -> Chequeo de salud del servidor
  POST /echo             -> El "mesero" (API): recibe, traduce y responde
  POST /sensor/lectura    -> Recibir datos de un sensor (ej. PPG, audio, etc.)
  GET  /sensor/historial   -> La "despensa" (Base de Datos): consultar lo guardado
  POST /clasificar        -> Simulación de un modelo de IA en la nube

Ejecutar localmente:
    pip install -r requirements.txt
    uvicorn app:app --host 0.0.0.0 --port 8000

En la VM (GCP o AWS), recuerda:
  1) Abrir el puerto 8000 en el Firewall / Security Group.
  2) Ejecutar el servidor con --host 0.0.0.0 (para escuchar en todas
     las interfaces, no solo localhost).
  3) Los alumnos se conectarán usando la IP pública de tu VM:
     http://TU-IP-PUBLICA:8000
"""

import random
import sqlite3
import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Servidor de Práctica - Nube",
    description="Servidor mínimo para probar clientes desde Google Colab",
    version="1.0.0",
)

# CORS abierto para que cualquier notebook de Colab pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path(__file__).parent / "datos.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno TEXT,
            sensor TEXT,
            valor REAL,
            fecha TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------------------
# Modelos de datos (lo que el "mesero"/API espera recibir)
# ---------------------------------------------------------------------
class EchoRequest(BaseModel):
    mensaje: str


class LecturaSensor(BaseModel):
    alumno: str
    sensor: str  # ej: "ppg", "fonocardiograma", "temperatura"
    valor: float


class DatosClasificar(BaseModel):
    valores: list[float]


# ---------------------------------------------------------------------
# 1) Cliente-Servidor básico
# ---------------------------------------------------------------------
@app.get("/")
def raiz():
    return {
        "mensaje": "Servidor activo. Este es el 'Servidor' de la diapositiva "
        "'El hardware detrás de la pantalla'.",
        "hora_servidor": datetime.utcnow().isoformat(),
    }


@app.get("/health")
def salud():
    return {"status": "ok", "uptime_check": time.time()}


# ---------------------------------------------------------------------
# 2) El "mesero" / API: recibe, traduce, responde
# ---------------------------------------------------------------------
@app.post("/echo")
def echo(payload: EchoRequest):
    return {
        "recibido_del_cliente": payload.mensaje,
        "respuesta_del_servidor": f"El servidor recibió: '{payload.mensaje}' "
        f"y lo devuelve procesado ✅",
    }


# ---------------------------------------------------------------------
# 3) Recibir datos de un sensor y guardarlos ("la despensa")
# ---------------------------------------------------------------------
@app.post("/sensor/lectura")
def guardar_lectura(lectura: LecturaSensor):
    conn = get_db()
    conn.execute(
        "INSERT INTO lecturas (alumno, sensor, valor, fecha) VALUES (?, ?, ?, ?)",
        (lectura.alumno, lectura.sensor, lectura.valor, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return {"status": "guardado", "lectura": lectura}


@app.get("/sensor/historial")
def obtener_historial(alumno: str | None = None, limite: int = 20):
    conn = get_db()
    if alumno:
        rows = conn.execute(
            "SELECT * FROM lecturas WHERE alumno = ? ORDER BY id DESC LIMIT ?",
            (alumno, limite),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM lecturas ORDER BY id DESC LIMIT ?", (limite,)
        ).fetchall()
    conn.close()
    return {"total": len(rows), "lecturas": [dict(r) for r in rows]}


# ---------------------------------------------------------------------
# 4) Simulación de un modelo de IA en la nube (cómputo)
# ---------------------------------------------------------------------
@app.post("/clasificar")
def clasificar(datos: DatosClasificar):
    if not datos.valores:
        raise HTTPException(status_code=400, detail="Envía al menos un valor")

    promedio = sum(datos.valores) / len(datos.valores)
    # Clasificación de juguete, solo para practicar el flujo cliente -> servidor -> IA
    etiqueta = random.choice(["Sano", "Revisar", "Anómalo"]) if promedio > 0 else "Sin datos"

    return {
        "n_valores_recibidos": len(datos.valores),
        "promedio": round(promedio, 3),
        "clasificacion": etiqueta,
        "nota": "Este endpoint simula el paso 'Clasificación ML' de la Fase 3 "
        "del Viaje del Mensaje. Reemplázalo con tu propio modelo.",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
