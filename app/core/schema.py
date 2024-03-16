from pydantic import BaseModel, create_model, RootModel
from sqlalchemy import inspect
from core.models import *
import datetime

def sqlalchemy_schema(sqlalchemy_class):
    inspector = inspect(sqlalchemy_class)
    attributes = {}
    
    for column in inspector.c:
        attributes[column.name] = (column.type.python_type, None)
    
    return create_model(sqlalchemy_class.__name__, **attributes)

class TracksResponse(BaseModel):
    title: str
    album: str
    artist: str
    date: datetime.datetime
    hash: str
    albumhash: str
    artisthash: str

class TracksListResponse(RootModel[list[TracksResponse]]):
    root: list[TracksResponse]

    def dict(self, **kwargs):
        return self.root
    

    
class AlbumsListResponse(BaseModel):
    albumhash: str = None
    album: str = None
    albumartist: str = None
    imagehash: str = None
    year: int = 0
    tracktotals: int = 0
    disctotals: int = 0

class AlbumsResponse(sqlalchemy_schema(Albums)):
    pass



class ArtistsListResponse(sqlalchemy_schema(Artists)):
    pass

# class ArtistsResponse(sqlalchemy_schema(Artists)):
#     pass



# class TracksListResponse(BaseModel):
#     title: str = None
#     album: str = None
#     artist: str = None
#     date: datetime.datetime = None
#     hash: str = None
#     albumhash: str = None
#     artisthash: str = None

# class TracksResponse(sqlalchemy_schema(Tracks)):
#     pass