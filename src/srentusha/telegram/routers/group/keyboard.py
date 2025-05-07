from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

inallowed_group_ids = [320, 282, 323, 297, 328]


class GroupButtonCallbackInfo(CallbackData, prefix="group_button_content"):
    group_title: str
    group_id: int


class CarouselIndexButtonCallbackInfo(CallbackData, prefix="carousel_index_button"):
    index: int


def get_carousel_buttons() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=CarouselIndexButtonCallbackInfo(
                        index=1,
                    ).pack(),
                ),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=CarouselIndexButtonCallbackInfo(
                        index=2,
                    ).pack(),
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


def build_groups_keyboard(
    groups: dict[str, int],
    index: int,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    group_list = list(groups)[:24] if index == 1 else list(groups)[23:]

    for group_title in group_list:
        if groups[group_title] not in inallowed_group_ids:
            builder.button(
                text=group_title,
                callback_data=GroupButtonCallbackInfo(
                    group_title=group_title,
                    group_id=groups[group_title],
                ),
            )

    builder.attach(InlineKeyboardBuilder.from_markup(get_carousel_buttons()))
    builder.adjust(2, repeat=True)

    return builder.as_markup()


def get_back_button() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data="back",
                ),
            ],
        ],
    )


def get_back_button_with_schedule() -> types.InlineKeyboardMarkup:
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
