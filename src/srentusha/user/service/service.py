from srentusha.user.core.user import User
from srentusha.user.repository.repository import UserRepository
from srentusha.user.service.scheme import UserAddSchema


class UserService:
    __admin_user_ids: list[int]
    __repository: UserRepository

    def __init__(self, repository: UserRepository, admin_user_ids: list[int]):
        self.__repository = repository
        self.__admin_user_ids = admin_user_ids

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.__admin_user_ids

    async def insert_user(
        self,
        id_: int,
    ) -> User:
        return await self.__repository.get_and_add(id_=id_)

    async def insert_group_to_user(
        self,
        user: UserAddSchema,
    ) -> User:
        return await self.__repository.insert_group_to_user(
            user=User(user_id=user.user_id, user_group=user.user_group),
        )
