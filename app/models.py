from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

# This class serves as BOTH a data validator and a database table
class League(SQLModel, table=True):
    id: int = Field(primary_key=True) # Use the ID from the API as the primary key
    name: str
    type: str
    logo: str
    country_name: str