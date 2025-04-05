from dataclasses import asdict

from motor.motor_asyncio import AsyncIOMotorClient

from srentusha.settings import Settings
from srentusha.user.core.user import User


class ModelNotFoundError(Exception): ...


class UserMapper:
    def add_info_about_user(self, entity: User) -> User:
        return asdict(entity)

    def extract_info_from_user(self, record: dict) -> User:
        return User(
            user_id=record["user_id"],
            user_group=record["user_group"],
            user_sections=record["user_sections"],
        )


class UserRepository:
    __mapper: UserMapper = UserMapper()
    __client: AsyncIOMotorClient = AsyncIOMotorClient(
        host=Settings.MONGO_CONNECTION_STRING,
        connect=False,
    )

    async def get_and_add(self, id_: str | None, group: str | None = None) -> User:
        if id_ is None:
            return self.__client.srentusha.users.find({})

        if record := await self.__client.srentusha.users.find_one(
            filter={"user_id": id_},
        ):
            return self.__mapper.extract_info_from_user(record=record)

        return await self.add(
            user=User(user_id=id_, user_group=group),
        )

    async def add(self, user: User) -> User:
        await self.__client.srentusha.users.insert_one(
            document=self.__mapper.add_info_about_user(entity=user),
        )
        return user

    async def insert_group_to_user(
        self,
        user: User,
    ) -> User:
        await self.__client.srentusha.users.update_one(
            {"user_id": user.user_id},
            {"$set": {"user_group": user.user_group}},
        )

        return user
