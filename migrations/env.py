from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.db.init_db import Base
from app.models.models import *
from app.core.config import settings

config = context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    url = settings.DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(lambda conn: context.configure(
            connection=conn,
            target_metadata=target_metadata,
            compare_type=True
        ))
        async with connection.begin():
            await connection.run_sync(lambda conn: context.run_migrations())


import asyncio
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())