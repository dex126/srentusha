import contextlib

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest

from srentusha.parser.service.service import CollegeParserService
from srentusha.telegram.routers.group import keyboard as keyboard_group
from srentusha.telegram.routers.start import keyboard as keyboard_menu
from srentusha.user.service.scheme import UserAddSchema
from srentusha.user.service.service import UserService


class ChangeGroupRouter(Router):
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
            F.data.in_("change_group"),
        )
        self.callback_query.register(
            self.catch_carousel_index,
            keyboard_group.CarouselIndexButtonCallbackInfo.filter(),
        )
        self.callback_query.register(
            self.catch_group_from_button,
            keyboard_group.GroupButtonCallbackInfo.filter(),
        )
        self.callback_query.register(
            self.back,
            F.data.in_("back"),
        )

    async def give_group_message(
        self,
        query: types.CallbackQuery,
        index: int = 1,
    ) -> None:
        await query.answer()
        await self.__user_service.insert_user(id_=query.message.chat.id)
        groups = await self.__parser_service.get_parsed_groups()

        with contextlib.suppress(TelegramBadRequest):
            await query.message.edit_text(
                "<b>Выберите нужную группу из списка ниже</b>",
                reply_markup=keyboard_group.build_groups_keyboard(
                    groups=groups,
                    index=index,
                ),
            )

    async def catch_carousel_index(
        self,
        query: types.CallbackQuery,
        callback_data: keyboard_group.CarouselIndexButtonCallbackInfo,
    ) -> None:
        await self.give_group_message(query=query, index=callback_data.index)

    async def catch_group_from_button(
        self,
        query: types.CallbackQuery,
        callback_data: keyboard_group.GroupButtonCallbackInfo,
    ) -> None:
        await self.__user_service.insert_group_to_user(
            user=UserAddSchema(
                user_id=query.message.chat.id,
                user_group=callback_data.group_title,
            ),
        )
        await query.message.edit_text(
            f"<b>Группа изменена на {callback_data.group_title}</b>",
            reply_markup=keyboard_group.get_back_button_with_schedule(),
        )

    async def back(self, query: types.CallbackQuery) -> None:
        await query.message.edit_text(
            text=f"<b>Добро пожаловать, {query.from_user.first_name}</b>\n\n"
            "<i>В этом боте вы можете узнать актуальное расписание нужной группы.</i>",
            reply_markup=keyboard_menu.get_schedule_button(),
        )
