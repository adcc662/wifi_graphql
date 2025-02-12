# src/scripts/load_data.py
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from src.database.session import AsyncSessionLocal
from src.models.wifi_point import WifiAccessPoint


async def load_csv_data():
    csv_path = Path(__file__).parent / '2024-06-30-puntos_de_acceso_wifi.csv'
    print(f"📂 Intentando leer archivo desde: {csv_path}")

    # Leer el CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"📊 Registros encontrados: {len(df)}")
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        return

    # Eliminar IDs duplicados antes de insertar
    df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    print(f"✅ Registros después de eliminar duplicados: {len(df)}")

    # Reemplazar NaN en columnas de tipo VARCHAR
    df['colonia'].fillna("Desconocido", inplace=True)
    df['alcaldia'].fillna("Desconocido", inplace=True)

    async with AsyncSessionLocal() as session:
        # Verificar cantidad de registros antes de borrar
        count_before = await session.execute(text('SELECT COUNT(*) FROM wifi_access_points'))
        print(f"📉 Registros antes de limpiar: {count_before.scalar()}")

        # Limpiar tabla antes de insertar nuevos datos
        await session.execute(text('DELETE FROM wifi_access_points'))
        await session.commit()

        count_after = await session.execute(text('SELECT COUNT(*) FROM wifi_access_points'))
        print(f"✅ Registros después de limpiar: {count_after.scalar()}")

        # Cargar nuevos datos en lotes
        default_date = datetime(2024, 1, 1)
        batch_size = 1000

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size].to_dict(orient="records")
            print(f"🚀 Procesando lote {i // batch_size + 1} de {len(df) // batch_size + 1}")

            insert_statements = [
                insert(WifiAccessPoint).values(
                    id=row['id'],
                    program=row['programa'],
                    installation_date=default_date if pd.isna(row['fecha_instalacion']) else pd.to_datetime(row['fecha_instalacion']),
                    latitude=row['latitud'],
                    longitude=row['longitud'],
                    neighborhood=row['colonia'],
                    district=row['alcaldia']
                ).on_conflict_do_nothing(index_elements=['id'])  # Evita errores de clave duplicada
                for row in batch
            ]

            for stmt in insert_statements:
                await session.execute(stmt)

            await session.commit()
            print(f"✅ Lote {i // batch_size + 1} cargado exitosamente")

    print("🎉 Carga de datos finalizada con éxito")


if __name__ == "__main__":
    asyncio.run(load_csv_data())
