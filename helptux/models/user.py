import bcrypt
from hashlib import sha512
from helptux import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return '<Role {0}>'.format(self.role)

    def __init__(self, role):
        self.role = role


users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role',
                            secondary=users_roles,
                            primaryjoin=(users_roles.c.user_id == id),
                            secondaryjoin=(users_roles.c.role_id == Role.id),
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.username = self.email
        self.password(password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def output_obj(self):
        return {
            'id': self.id,
            'username': self.username,
            'posts': [p.id for p in self.posts],
            'roles': [r.id for r in self.roles]
        }

    @property
    def password(self):
        raise AttributeError('Attribute unreadable')

    @password.setter
    def password(self, input_password):
        # Work around to 72-character limit for bcrypt (https://github.com/pyca/bcrypt/)
        hashed_input = sha512(input_password).digest()
        self.password_hash = bcrypt.hashpw(hashed_input, bcrypt.gensalt())

    def verify_password(self, input_password):
        hashed_input = sha512(input_password).digest()
        if bcrypt.hashpw(hashed_input, self.password_hash) == self.password_hash:
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated
