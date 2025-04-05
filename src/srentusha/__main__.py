import asyncio

from srentusha.settings import Settings
from srentusha.telegram.service.service import TelegramService
from srentusha.user.repository.repository import UserRepository
from srentusha.user.service.service import UserService


async def main() -> None:
    telegram_service = TelegramService(
        user_service=UserService(
            repository=UserRepository(),
            admin_user_ids=Settings.TELEGRAM_ADMIN_IDS,
        ),
    )
    await telegram_service.start()


if __name__ == "__main__":
    asyncio.run(main=main())
