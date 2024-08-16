from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from fastapi import HTTPException, status
from database import movies_collection, users_collection, ratings_collection, comments_collection
from schema import MovieCreate, MovieUpdate, UserCreate, UserBase, UserInDb, UserUpdate, UserCreate, CommentCreate, RatingCreate, MovieDelete
from serializer import movie_serializer, user_serializer, comment_serializer, rating_serializer, user_serializer_password



class MovieCRUDservice:
    
    @staticmethod
    def movie_create(movie_data: MovieCreate, user: UserBase):
        movie_data_dict = movie_data.model_dump()
        movie_data_dict.get("user_id") == user["id"]
        movie_data = jsonable_encoder(movie_data_dict)
        movie_document_data = movies_collection.insert_one(movie_data)
        movie_id = movie_document_data.inserted_id
        movie_document = movies_collection.find_one({"_id": ObjectId(movie_id)})
        return movie_serializer(movie_document)
    
    @staticmethod
    def get_all_movies(skip: int = 0, limit: int = 5):
        movies = movies_collection.find().skip(skip).limit(limit)
        return [movie_serializer(movie) for movie in movies]
    
    @staticmethod
    def get_movies_by_id(movie_id: str):
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        # print(movie)  # Print the entire movie document
        if movie:
            movie["user_id"] = movie.get("user_id", None)
            return movie_serializer(movie)
        return None
    
    @staticmethod
    def update_movie(movie_id: str, movie_update_in: MovieUpdate, user: UserInDb):
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)}  )

        if not movie:
            return None
        
        if movie["user_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Not authorized to update this movie")

        movie_update_data = movie_update_in.model_dump(exclude_unset=True)
        movie_updated = movies_collection.find_one_and_update(
            {"_id": ObjectId(movie_id)}, {"$set": movie_update_data}, return_document=True
        )

        return movie_serializer(movie_updated)
    
    
    @staticmethod
    def delete_movie(movie_id: str, user: UserInDb):
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            return None
        if movie["user_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
        movie_deleted = movies_collection.find_one_and_delete({"_id": ObjectId(movie_id)})
        return True

    
    @staticmethod
    def add_comment_to_movie(movie_id: str, comment_id: str):
        movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$push": {"comments": comment_id}})
        
    
    @staticmethod
    def add_rating_to_movie(movie_id: str, rating_id: str):
        movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$push": {"ratings": rating_id}})

   
    @staticmethod
    def get_movie_id(movie_id: str):
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        return movie.get("title")
    
movie_crud_service = MovieCRUDservice


class UserCRUDservice:
    
    @staticmethod
    def user_create(user_data: UserCreate, hashed_password: str):
        # Verify if user exists
        if users_collection.find_one({"username": user_data.username}):
            raise HTTPException (detail = "user already exists", status_code= status.HTTP_400_BAD_REQUEST)
        # Continue if user does not exist
        user_data = jsonable_encoder(user_data)
        user_document_data = users_collection.insert_one(
            {
                "username": user_data.get('username'),
                "full_name": user_data.get('full_name'),
                "hashed_password": hashed_password,
            }
        )
        user_id = user_document_data.inserted_id
        user_document = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        return user_serializer(user_document)
    
    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 5):
        users = users_collection.find().skip(skip).limit(limit)
        return [user_serializer(user) for user in users]
    
    @staticmethod
    def get_user_by_username(username: str) -> UserInDb:
        user =users_collection.find_one({"username": username})
        if user:
            return user_serializer(user)
        return None
    
    @staticmethod
    def get_user_by_username_with_hash(username: str) -> UserInDb:
        user = users_collection.find_one({"username": username})
        if user:
            return user_serializer_password(user)
        return None
    
    @staticmethod
    def update_user(username: str, user_data: UserUpdate):
        user = users_collection.find_one({"username": username})

        if not user:
            return None

        user_update_data = user_data.model_dump(exclude_unset=True)
        user_updated = users_collection.find_one_and_update(
            {"username": user_data.username}, {"$set": user_update_data}, return_document=True
        )

        return user_serializer(user_updated)
    
    @staticmethod
    def delete_user(username: str):
        return users_collection.find_one_and_delete({"username": username})
   
    
user_crud_service = UserCRUDservice



class CommentCRUDservice:
    
    @staticmethod
    def create_comment(comment_data: CommentCreate, user: UserBase, movie_id: str):
        comment_data_dict = comment_data.model_dump()
        comment_data_dict['user_id'] = user["id"]
        comment_data_dict['movie_id'] = movie_id
        comment_data = jsonable_encoder(comment_data_dict)
        comment_document_data = comments_collection.insert_one(comment_data)
        comment_id = comment_document_data.inserted_id
        comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": {"comment_id": str(comment_id)}})
        movie_crud_service.add_comment_to_movie(movie_id, str(comment_id))
        comment_document = comments_collection.find_one({"_id": ObjectId(comment_id)})
        return comment_serializer(comment_document)



    @staticmethod
    def get_comments_by_movie(movie_id: str):
        comments = comments_collection.find({"movie_id": movie_id})
        return [comment_serializer(comment) for comment in comments]
    
comment_crud_service = CommentCRUDservice


class RatingCRUDservice:
    
    @staticmethod
    def create_rating(rating_data: RatingCreate, user: UserBase, movie_id: str):
        rating_data_dict = rating_data.model_dump()
        rating_data_dict['user_id'] = user["id"]
        rating_data_dict['movie_id'] = movie_id
        rating_data = jsonable_encoder(rating_data_dict)
        rating_document_data = ratings_collection.insert_one(rating_data)
        rating_id = rating_document_data.inserted_id
        ratings_collection.update_one({"_id": ObjectId(rating_id)}, {"$set": {"rating_id": str(rating_id)}})
        movie_crud_service.add_rating_to_movie(movie_id, str(rating_id))
        rating_document = ratings_collection.find_one({"_id": ObjectId(rating_id)})
        return rating_serializer(rating_document)
    
    
    @staticmethod
    def get_ratings_by_movie(movie_id: str):
        ratings = ratings_collection.find({"movie_id": movie_id})
        return [rating_serializer(rating) for rating in ratings]
    

rating_crud_service = RatingCRUDservice
