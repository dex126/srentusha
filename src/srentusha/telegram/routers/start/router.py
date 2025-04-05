from aiogram import Router, types
from aiogram.filters import CommandStart

from srentusha.telegram.routers.start import keyboard


class StartCommandRouter(Router):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.message.register(self.welcome_text, CommandStart(deep_link=False))

    async def welcome_text(self, message: types.Message) -> None:
        await message.answer(
            f"<b>Добро пожаловать, {message.from_user.first_name}</b>\n\n"
            "<i>В этом боте вы можете узнать актуальное расписание нужной группы.</i>",
            reply_markup=keyboard.get_schedule_button(),
        )
