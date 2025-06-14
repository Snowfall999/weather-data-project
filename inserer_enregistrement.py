from api_request import fetch_weather, extract_fetch_weather
import psycopg2
from psycopg2 import sql
from datetime import datetime

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5000,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        print("Connexion à la base de données PostgreSQL réussie...")
        return conn
    except psycopg2.Error as e:
        print(f"Connexion à la base de données échouée: {e}")
        return None

def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS dev;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (                                                                             
                id SERIAL PRIMARY KEY,
                ville VARCHAR(100) NOT NULL,
                heure TIME NOT NULL,  
                date DATE NOT NULL,                                                             
                temperature REAL,                                           
                pression REAL,                                                     
                humidite INTEGER,
                vent REAL,
                description TEXT
            );
        """)
        conn.commit()
        print("Table créée avec succès.")
    except psycopg2.Error as e:
        print(f"Création de la table échouée: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()

def inserer_enregistrement(conn, data):
    if data is None:
        print("Aucune donnée à insérer. Insertion annulée.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dev.raw_weather_data (
                ville,
                heure,
                date,
                temperature,
                pression,
                humidite,
                vent,
                description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['ville'],
            data['heure'],
            data['date'],
            data['temperature'],
            data['pression'],
            data['humidite'],
            data['vent'],
            data['description']
        ))
        conn.commit()
        print("Données insérées avec succès.")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion des données: {e}")
        conn.rollback()
    finally:
        cursor.close()

# main
if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        create_table(conn)

        # Récupération des données météo
        brut_data = fetch_weather()
        data = extract_fetch_weather(brut_data)

        if data:
            inserer_enregistrement(conn, data)
        else:
            print("Aucune donnée météo valide récupérée, insertion non effectuée.")

        conn.close()
