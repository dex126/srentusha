import secrets
from datetime import datetime, timedelta

import httpx
import pytz

from srentusha.settings import Settings


class CollegeParserService:
    def __init__(self) -> None:
        super().__init__()
        self.__client = httpx.AsyncClient()

    async def get_parsed_groups(self) -> dict[str, int]:
        extracted_groups = (
            await self.__client.get(
                "https://api.platform.nke.team:8443/groups/?offset=0&limit=500",
                headers={"Authorization": f"Bearer {Settings.COLLEGE_API_AUTH}"},
            )
        ).json()

        return {
            group["title"]: group["id"]
            for group in sorted(
                extracted_groups,
                key=lambda group: group["title"],
            )
        }

    async def get_parsed_schedule(self, group: str) -> dict[str, str]:
        timestamp_start = (datetime.today() - timedelta(days=1)).timestamp()  # noqa: DTZ002
        timestamp_end = datetime.today().timestamp()  # noqa: DTZ002

        groups = await self.get_parsed_groups()

        schedule_items = (
            await self.__client.get(
                f"https://api.platform.nke.team:8443/schedule/?start={timestamp_start}&end={timestamp_end}&groupId={groups[group]}",
                headers={"Authorization": f"Bearer {Settings.COLLEGE_API_AUTH}"},
            )
        ).json()

        if not schedule_items["items"]:
            return None

        return {
            f"{lesson['classroom']['title']}?{secrets.token_hex(3)}": lesson
            for lesson in sorted(
                schedule_items["items"],
                key=lambda lesson: lesson["start"],
            )
        }

    async def parse_timestamp(
        self,
        timestamp_start: int,
        timestamp_end: int,
    ) -> tuple[datetime, datetime]:
        tz = pytz.timezone("UTC")
        timestamp_start = datetime.fromtimestamp(timestamp_start, tz=tz)
        timestamp_end = datetime.fromtimestamp(timestamp_end, tz=tz)

        return timestamp_start, timestamp_end
