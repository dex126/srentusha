from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_schedule_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Узнать расписание",
                    callback_data="get_schedule",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Сменить группу",
                    callback_data="change_group",
                ),
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Добавить курс",  # noqa: ERA001
            #         callback_data="append_course",  # noqa: ERA001
            #     ),
            # ],
        ],
    )
