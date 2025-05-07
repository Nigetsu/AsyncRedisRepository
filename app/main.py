import asyncio
import redis.asyncio as redis
from redis.asyncio import RedisError
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class AsyncRedisRepository:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    async def set_user(self, user_id: int, full_name: str):
        key = f"user:{user_id}"

        try:
            await self.redis_client.set(key, full_name)
            logger.info(f"Успешно добавлен пользователь {user_id}: {full_name}")
        except RedisError as e:
            logger.error(f"Ошибка при отправике данныx: {str(e)}")
            raise e

    async def get_user(self, user_id: int) -> str | None:
        key = f"user:{user_id}"

        try:
            res = await self.redis_client.get(key)
            if res:
                logger.info(f"Успешно получен пользователь {user_id}")
                return res.decode("utf-8")
            logger.info(f"Пользователь {user_id} не найден")
            return None
        except RedisError as e:
            logger.error(f"Ошибка при получении user: {str(e)}")
            raise e

    async def delete_user(self, user_id: int) -> bool:
        key = f"user:{user_id}"

        try:
            res = await self.redis_client.delete(key)
            deleted_user = bool(res)
            if deleted_user:
                logger.info(f"Успешно удален пользователь {user_id}")
            else:
                logger.info(f"Пользователь {user_id} не найден")
            return deleted_user
        except RedisError as e:
            logger.error(f"Ошибка при удалении user: {str(e)}")
            raise e

async def main():
    repository = AsyncRedisRepository()

    await repository.set_user(1, "Petrov Petr Petrovich")
    await repository.get_user(1)
    await repository.delete_user(1)
    await repository.get_user(1)

if __name__ == "__main__":
    asyncio.run(main())