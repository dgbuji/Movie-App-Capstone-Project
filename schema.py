from pydantic import BaseModel
from typing import Optional, List
# from Comment import comment
# from RatingBase import Rating


# from crud import comment
# from .schema.comment import Comment
# from .schema.rating import Rating
# from typing import Optional

class UserBase(BaseModel):
    username: str
    
    
class UserInDb(UserBase):
    full_name: str
    hashed_password: str
    user_id: str
    pass
      
class UserCreate(UserBase):
    full_name: str
    password: str
    pass 

class UserUpdate(UserBase):
    username: str
    full_name: str
    password: str
    is_active: bool = True
    
class UserDelete(UserBase):
    user_id: str  
    

class RatingBase(BaseModel):
    rating: float
    
class Rating(RatingBase):
    rating_id: str
    movie_id: str
    pass 

class RatingCreate(RatingBase):
    movie_id: str
    pass

# a comment should have a content field

class CommentBase(BaseModel):
    comment: str
    
class Comment(CommentBase):
    comment_id: str
    movie_id: str
    pass 

class CommentCreate(CommentBase):
    movie_id: str
    pass 

class CommentUpdate(Comment):
    updated_comment: str
    pass

    
class MovieBase(BaseModel):
    title: str
    description: str
    
class Movie(MovieBase):
    movie_id: str
    user_id: str
    comments: List[Comment]
    ratings: List [Rating]
    pass
    

class MovieCreate(MovieBase):
    user_id: str
    pass 

class MovieUpdate(MovieBase):
    user_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    comment: Optional[str] = None

class MovieDelete(MovieBase):
    user_id: str
    pass


