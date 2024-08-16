def movie_serializer(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie.get ("title"),
        "description": movie.get("description"),
        "ratings": movie.get("ratings", []),
        "user_id": movie.get("user_id"),  # Assuming this field is stored in the movie document
    }

# def movie_serializer(movie) -> dict:
#     ## to convert a MongoDB movie object to a Python Dictionary
    
#     return{
#         "id": str (movie.get ("_id")),
#         "title": movie.get ("title"),
#         "description": movie.get ("description"),
#         "user_id ": str (movie.get("user_id"))                 
#     }
    
def user_serializer(user) -> dict:
    
    return{
        "id": str (user.get ("_id")),
        "username": user.get ("username"),
        "full_name": user.get ("full_name"),
        "password": user.get ("password"),
    }
    
def user_serializer_password(user) -> dict:
    """Converts a MongoDB user object to a Python dictionary"""
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "hashed_password": user.get("hashed_password")
    }
    
def rating_serializer(rating) -> dict:
    """Converts a MongoDB rating object to a Python dictionary"""
    return {
        "id": str(rating.get("_id")),
        "movie_id": str(rating.get("movie_id")),
        "user_id": str(rating.get("user_id")),
        "rating": rating.get("rating")
    }
    
def comment_serializer(comment) -> dict:
    return {
        "comment_id": str(comment.get("_id")),
        "movie_id": str (comment.get("movie_id")),
        "comment": comment.get("comment"),
        "updated_comment": comment.get("updated_comment", None)
    }
    

