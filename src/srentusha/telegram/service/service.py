from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient

from srentusha.parser.service.service import CollegeParserService
from srentusha.settings import Settings
from srentusha.telegram.routers.group.router import ChangeGroupRouter
from srentusha.telegram.routers.schedule.router import ScheduleRouter
from srentusha.telegram.routers.start.router import StartCommandRouter
from srentusha.user.service.service import UserService


class TelegramService:
    __bot: Bot

    def __init__(
        self,
        user_service: UserService,
    ) -> None:
        self.__bot = Bot(
            token=Settings.TELEGRAM_BOTAPI_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.__dispatcher = Dispatcher(
            storage=MongoStorage(
                client=AsyncIOMotorClient(host=Settings.MONGO_CONNECTION_STRING),
            ),
        )

        self.__dispatcher.include_router(router=StartCommandRouter())
        self.__dispatcher.include_router(
            router=ChangeGroupRouter(
                parser_service=CollegeParserService(),
                user_service=user_service,
            ),
        )
        self.__dispatcher.include_router(
            router=ScheduleRouter(
                parser_service=CollegeParserService(),
                user_service=user_service,
            ),
        )

    async def start(self) -> None:
        await self.__dispatcher.start_polling(self.__bot)
