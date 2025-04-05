from aiogram import types


def get_schedule_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Обновить расписание",
                    callback_data="refresh_schedule",
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data="back",
                ),
            ],
        ],
    )


def get_group_button() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Сменить группу",
                    callback_data="change_group",
                ),
            ],
        ],
    )
