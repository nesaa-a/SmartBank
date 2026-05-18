from app.models.system import File
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    model = File
