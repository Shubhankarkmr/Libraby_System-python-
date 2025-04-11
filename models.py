from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association Table for M:N between Authors and Books
book_author = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'))
)

class Institute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    student_strength = db.Column(db.Integer)
    date_of_inception = db.Column(db.Date)

    libraries = db.relationship('Library', backref='institute', lazy=True)
    students = db.relationship('Student', backref='institute', lazy=True)

class Student(db.Model):
    reg_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_no = db.Column(db.BigInteger)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)

    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id'))
    vehicle_id = db.Column(db.String(15), db.ForeignKey('vehicle.registration_id'))
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_of_inception = db.Column(db.Date)
    floor_no = db.Column(db.Integer)

    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id'))
    librarian_id = db.Column(db.Integer, db.ForeignKey('librarian.employee_id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.employee_id'))

    students = db.relationship('Student', backref='library', lazy=True)
    books = db.relationship('Books', backref='library', lazy=True)
    teachers = db.relationship('Teachers', backref='library', lazy=True)

class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    no_of_pages = db.Column(db.Integer)
    publisher_name = db.Column(db.String(100), db.ForeignKey('publisher.name'))
    published_date = db.Column(db.Date)
    edition = db.Column(db.String(10))
    
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))

    authors = db.relationship('Authors', secondary=book_author, backref='books')

class Librarian(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Float)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))

    library = db.relationship('Library', backref='librarian', uselist=False)

class Teachers(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    phone_no = db.Column(db.BigInteger)
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))

class Director(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    phone_no = db.Column(db.BigInteger)
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)

    # one director to one library + institute pair (via Library)
    library = db.relationship('Library', backref='director', uselist=False)

class Authors(db.Model):  # Weak Entity
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    phone_no = db.Column(db.BigInteger)
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)

class Vehicle(db.Model):
    registration_id = db.Column(db.String(15), primary_key=True)
    color = db.Column(db.String(10))
    top_speed = db.Column(db.Integer)
    length = db.Column(db.String(5))
    hp = db.Column(db.String(10))

    students = db.relationship('Student', backref='vehicle', lazy=True)

class Publisher(db.Model):  # Publishes both Books and Authors
    name = db.Column(db.String(50), primary_key=True)
    address = db.Column(db.String(50))
    ceo_name = db.Column(db.String(50))
    establishment_date = db.Column(db.Date)
    contact_no = db.Column(db.BigInteger)

    books = db.relationship('Books', backref='publisher', lazy=True)
