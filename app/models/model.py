from app import db
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp



class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, nullable=True)
    full_name = db.Column(db.String, nullable=True)
    post = db.relationship('Posts', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name' : self.full_name
        }
    #
    # def check_pass(self,password):
    #     return safe_str_cmp(self.password)

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    create_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post {}>'.format(self.content)