from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    prefix="/posts"
)


@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/")
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)

    new_post = models.Post(created_by = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    #post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    if post.Post.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        # response.status_code = status.HTTP_404_NOT_FOUND  
        # return {"message": f"Post with id {id} was not found"}    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()

    #post = find_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")

    if post.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post.delete(synchronize_session=False)
    db.commit()
    #conn.commit()
    #my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"message": f"The post with id {id} has been deleted"}

    

# @app.delete("/posts/{id}")
# def delete_post(id : int):
#     index = find_index(id)
#     if index == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                           detail=f"Post with id {id} does not exist")
#     my_posts.pop(index)
#     return {"message": "The post {id} was successfully deleted."}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_record = cursor.fetchone()
    # conn.commit()

    #index = find_index(id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    if post.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()