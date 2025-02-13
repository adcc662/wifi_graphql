import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
import uuid
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
        print(f"📊 Registros encontrados en el CSV: {len(df)}")
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        return

    # Reemplazar NaN en columnas de texto con "Desconocido"
    df['colonia'].fillna("Desconocido", inplace=True)
    df['alcaldia'].fillna("Desconocido", inplace=True)

    # Verificar duplicados en ID
    duplicated_ids = df[df.duplicated(subset=['id'], keep=False)]
    if not duplicated_ids.empty:
        print(f"⚠️ Se encontraron {len(duplicated_ids)} IDs duplicados. Asignando nuevos IDs únicos...")

        # Agregar un UUID para diferenciar los duplicados
        df['id'] = df.apply(lambda row: f"{row['id']}_{uuid.uuid4().hex[:8]}"
        if row['id'] in duplicated_ids['id'].values else row['id'], axis=1)

    print(f"✅ Registros después de eliminar duplicados: {len(df)}")

    async with AsyncSessionLocal() as session:
        # Verificar registros antes de borrar
        count_before = await session.execute(text('SELECT COUNT(*) FROM wifi_access_points'))
        print(f"📉 Registros en la BD antes de la inserción: {count_before.scalar()}")

        # Limpiar la tabla solo si es necesario
        await session.execute(text('DELETE FROM wifi_access_points'))
        await session.commit()

        count_after = await session.execute(text('SELECT COUNT(*) FROM wifi_access_points'))
        print(f"✅ Registros en la BD después de la limpieza: {count_after.scalar()}")

        # Insertar datos en lotes de 1000
        default_date = datetime(2024, 1, 1)
        batch_size = 1000

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size].to_dict(orient="records")
            print(f"🚀 Procesando lote {i // batch_size + 1} de {len(df) // batch_size + 1}")

            insert_statements = [
                insert(WifiAccessPoint).values(
                    id=row['id'],
                    program=row['programa'],
                    installation_date=default_date if pd.isna(row['fecha_instalacion']) else pd.to_datetime(
                        row['fecha_instalacion']),
                    latitude=row['latitud'],
                    longitude=row['longitud'],
                    neighborhood=row['colonia'],
                    district=row['alcaldia'],
                    location=f'SRID=4326;POINT({row["longitud"]} {row["latitud"]})'

                ).on_conflict_do_nothing(index_elements=['id'])  # Evita conflictos de clave duplicada
                for row in batch
            ]

            for stmt in insert_statements:
                await session.execute(stmt)

            await session.commit()
            print(f"✅ Lote {i // batch_size + 1} insertado exitosamente")

    print("🎉 Carga de datos finalizada con éxito")


if __name__ == "__main__":
    asyncio.run(load_csv_data())
