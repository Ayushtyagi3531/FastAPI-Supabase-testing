
import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Supabase FastAPI Test")

DATABASE_URL = os.getenv("DATABASE_URL")


class Worker(BaseModel):
    name: str
    city: str


# Test 1 - Check FastAPI
@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


# Test 2 - Check database connection
@app.get("/db-check")
def check_database():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()

    return {
        "message": "Supabase connected successfully",
        "result": result[0]
    }


# Test 3 - Insert data into Supabase
@app.post("/workers")
def add_worker(worker: Worker):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO public.test_workers (name, city)
                VALUES (%s, %s)
                RETURNING id, name, city
                """,
                (worker.name, worker.city)
            )
            result = cur.fetchone()

    return {
        "message": "Worker saved successfully",
        "data": result
    }


# Test 4 - Read data from Supabase
@app.get("/workers")
def get_workers():

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, name, city
                FROM public.test_workers
                ORDER BY id DESC
                LIMIT 100
                """
            )
            result = cur.fetchall()

    return {"workers": result}
