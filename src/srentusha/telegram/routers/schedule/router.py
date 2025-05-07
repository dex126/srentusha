import contextlib
from datetime import datetime

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest

from srentusha.parser.service.service import CollegeParserService
from srentusha.telegram.routers.schedule import keyboard
from srentusha.user.service.service import UserService


class ScheduleRouter(Router):
    __parser_service: CollegeParserService
    __user_service: UserService

    def __init__(
        self,
        parser_service: CollegeParserService,
        user_service: UserService,
    ) -> None:
        super().__init__()
        self.__parser_service = parser_service
        self.__user_service = user_service
        self.callback_query.register(
            self.give_group_message,
            F.data.in_("get_schedule"),
        )
        self.callback_query.register(
            self.give_group_message,
            F.data.in_("refresh_schedule"),
        )

    async def give_group_message(
        self,
        query: types.CallbackQuery,
    ) -> None:
        await query.answer()
        user_info = await self.__user_service.insert_user(id_=query.message.chat.id)
        if not user_info.user_group:
            await query.message.edit_text(
                "<b>Сначала выберите группу!</b>",
                reply_markup=keyboard.get_group_button(),
            )
            return

        schedules = await self.__parser_service.get_parsed_schedule(
            group=user_info.user_group,
        )
        with contextlib.suppress(TelegramBadRequest):
            await query.message.edit_text(
                await self.parse_schedule_message(
                    schedules=schedules,
                    user_group=user_info.user_group,
                ),
                reply_markup=keyboard.get_schedule_keyboard(),
            )

    async def parse_schedule_message(self, schedules: dict, user_group: str) -> str:
        today_date = datetime.strptime(
            f"{datetime.now().date()}",
            "%Y-%m-%d",
        ).strftime("%d-%m-%Y")

        minimum_applied_hour = 8

        schedule_text = (
            f"<b>Расписание для {user_group}:"
            f"</b>\n<b>На <code>{today_date}</code></b>\n\n"
        )
        if schedules is None:
            return schedule_text + "<b>седня адыхаем) 🤪🤪🤪</b>"

        for classroom in schedules:
            nightmare = (str(classroom).split("?"))[0]

            schedule_time = await self.__parser_service.parse_timestamp(
                timestamp_start=schedules[classroom]["start"],
                timestamp_end=schedules[classroom]["end"],
            )

            if schedule_time[0].hour < minimum_applied_hour:
                time = (
                    f"{schedule_time[0].minute:d}:{schedule_time[0].second:02d}-"
                    f"{schedule_time[1].minute:d}:{schedule_time[1].second:02d}"
                )
            else:
                time = f"{schedule_time[0].time()[0:5]}-{schedule_time[1].time()[0:5]}"

            schedule_text += (
                f"{time} - "
                f"{schedules[classroom]['plan']['subject']['title']} - [{nightmare}]\n"
            )

        return schedule_text

    async def refresh_button(self, query: types.CallbackQuery) -> None:
        await self.give_group_message(query=query)
