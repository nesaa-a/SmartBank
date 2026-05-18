from app.models.system import Setting
from app.repositories.base import BaseRepository


class SettingRepository(BaseRepository[Setting]):
    model = Setting
