import os
import json
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Challenge, Profile, Resume
from datetime import datetime
from typing import List
from security import encrypt_data, decrypt_data  # Importar funciones de seguridad
import csv

# Ruta para el archivo de estado
STATE_FILE = "last_processed_index.json"

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para obtener el índice del último registro procesado para una tabla específica
def get_last_processed_index(table_name: str):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get(table_name, 0)  # Devuelve el índice de la tabla específica, o 0 si no existe
    return 0  # Si no existe, significa que no hemos procesado nada

# Función para guardar el índice del último registro procesado para una tabla específica
def save_last_processed_index(table_name: str, index: int):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {}

    state[table_name] = index  # Actualiza el índice de la tabla específica

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)  # Guarda el diccionario actualizado en el archivo

# -----------------------------------------------
# LOAD CSV ENDPOINT para transacciones en lote
# -----------------------------------------------

@app.post("/load_csv/{table_name}")
async def load_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if table_name not in ["users", "challenges", "profiles", "resumes"]:
        raise HTTPException(status_code=400, detail="Invalid table name")

    try:
        content = await file.read()
        decoded_content = content.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_content)

        # Obtener el índice del último registro procesado
        last_processed_index = get_last_processed_index(table_name)
        rows = list(reader)

        # Verificar que hay registros restantes
        remaining_rows = rows[last_processed_index:]

        if len(remaining_rows) == 0:
            raise HTTPException(status_code=400, detail="No more records to process")

        # Procesar los registros en lotes de 3000 por archivo
        batch_size = 3000
        total_processed = 0
        while total_processed < len(remaining_rows):
            batch_rows = remaining_rows[total_processed: total_processed + batch_size]
            print(f"Procesando un total de {len(batch_rows)} registros para la tabla {table_name}.")
            
            # Procesar el lote de registros
            for row in batch_rows:
                try:
                    # Validar que el 'id' es un entero
                    if not row.get("id") or not row["id"].isdigit():
                        print(f"Registro omitido debido a 'id' inválido o no entero: {row}")
                        continue  # Omite el registro si 'id' no es un número entero

                    if table_name == "users":
                        encrypted_email = encrypt_data(row["email"])  # Encriptar el correo electrónico
                        encrypted_identification_number = encrypt_data(row["identification_number"])  # Encriptar el número de identificación
                        row["email"] = encrypted_email
                        row["identification_number"] = encrypted_identification_number
                        user = User(**row)
                        db.add(user)
                    elif table_name == "challenges":
                        challenge = Challenge(**row)
                        db.add(challenge)
                    elif table_name == "profiles":
                        profile = Profile(**row)
                        db.add(profile)
                    elif table_name == "resumes":
                        resume = Resume(**row)
                        db.add(resume)
                    else:
                        raise HTTPException(status_code=400, detail=f"Unknown table: {table_name}")
                except Exception as e:
                    print(f"Error processing row: {row}. Error: {str(e)}")
                    continue  # Continuar con el siguiente registro si hay error

            # Confirmar la transacción en lote
            db.commit()

            # Actualizar el índice del último registro procesado
            total_processed += len(batch_rows)
            save_last_processed_index(table_name, last_processed_index + total_processed)

        return {"message": f"Successfully loaded {total_processed} rows into {table_name}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")
