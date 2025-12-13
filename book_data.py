from typing import Optional
from pydantic import BaseModel , Field

class BOOK(BaseModel):
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int
    year: int


#Creating different request model for data validation during book creation
# Each field  validation
class BookRequest(BaseModel):
    id:int
    title:str = Field(min_length=3 , max_length=100)
    author:str = Field(min_length=3 , max_length=50)
    category:str = Field(min_length=3 , max_length=30)
    description:str = Field(min_length=10 , max_length=500)
    rating:int  = Field(ge=1 , le=5)  # rating between 1 to 5
    year: int = Field(default=2024 , ge=1900 , le=2024)  # published year between 1900 to 2024


    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 0,
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "category": "Fiction",
                "description": "A philosophical book about a young shepherd's journey to find his personal legend.",
                "rating": 5,
                "year": 1988
            }
        }
    }

