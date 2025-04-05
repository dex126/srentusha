from aiogram import F, Router, types


class InlineMenuRouter(Router):
    def __init__(self) -> None:
        super().__init__()
        self.inline_query.register(self.inline_menu_query, F.query.in_("nasos"))

    async def inline_menu_query(self, query: types.InlineQuery) -> None:
        results = []
        results.append(
            types.InlineQueryResultArticle(
                id="35235235235235235",
                title="Расписание",
                description="Жестко спарсить расписание",
                input_message_content=types.InputTextMessageContent(
                    message_text="trahnut nessssssskalka katov",
                ),
            ),
        )
        await query.answer(results=results)
