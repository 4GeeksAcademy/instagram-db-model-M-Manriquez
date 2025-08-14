from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relaciones
    posts = db.relationship('Post', back_populates='user',
                            cascade='all, delete-orphan')
    comments = db.relationship(
        'Comment', back_populates='author', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    # Claves Foraneas
    user_from_id = db.Column(
        db.Integer, db.ForeignKey('User.id'), primary_key=True)
    user_to_id = db.Column(
        db.Integer, db.ForeignKey('User.id'), primary_key=True)


class Post(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)

    # Clave Foranea
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Relaciones
    author = db.relationship('User', back_populates='posts')
    media = db.relationship('Media', back_populates='post',
                            cascade='all, delete-orphan')
    comments = db.relationship(
        'Comment', back_populates='post', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Media(db.Model):
    __tablename__ = 'Media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum, nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)

    # Clave Foranea
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)

    # Relaciones
    post = db.relationship('Post', back_populates='media')

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }


class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String, nullable=False)

    # Claves Foraneas
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Relaciones
    author = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "post_id": self.post_id,
            "author_id": self.author_id,
        }
