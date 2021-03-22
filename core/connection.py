import os
from databases import Database, DatabaseURL
from core.setting import get_setting

setting = get_setting(os.getenv("APP_ENV"))


class Connection:
    def __init__(self, key: str, host: str = None, db: str = None) -> None:
        self.database = self.init_connection(key, host, db)

    def make_connection_url(
        self,
        driver: str,
        username: str,
        password: str,
        host: str,
        port: str,
        database: str,
    ) -> DatabaseURL:
        return DatabaseURL(f"{driver}://{username}:{password}@{host}:{port}/{database}")

    def init_connection(self, key: str, host: str = None, db: str = None) -> Database:
        connections = {}
        if key == "local":
            connections["local"] = self.make_connection_url(
                driver="mysql",
                username=setting.USERNAME,
                password=setting.PASSWORD,
                host=setting.DATABASE_HOST,
                port=setting.DATABASE_PORT,
                database=setting.DATABASE,
            )
        return Database(connections[key], ssl=False, min_size=1, max_size=5, pool_recycle=200)

    async def connect(self) -> None:
        await self.database.connect()

    async def disconnect(self) -> None:
        if self.database.is_connected:
            await self.database.disconnect()
