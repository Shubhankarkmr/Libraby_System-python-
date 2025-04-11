
from flask import Flask, render_template, request, redirect, url_for
from models import db, Student,Institute,Library,Books,Librarian,Teachers ,Director,Authors,Vehicle,Publisher
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# ====== Student CRUD ======
@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('student.html', students=students, student=None)

@app.route('/add_student', methods=['POST'])
def add_student():
    student = Student(
        reg_no=request.form['reg_no'],
        name=request.form['name'],
        phone_no=request.form['phone_no'],
        dob=request.form['dob'],
        age=request.form['age'],
        institute_id=request.form['institute_id']
    )
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/edit_student/<int:reg_no>')
def edit_student(reg_no):
    student = Student.query.get_or_404(reg_no)
    students = Student.query.all()
    return render_template('student.html', students=students, student=student)

@app.route('/update_student/<int:reg_no>', methods=['POST'])
def update_student(reg_no):
    student = Student.query.get_or_404(reg_no)
    student.name = request.form['name']
    student.phone_no = request.form['phone_no']
    student.dob = request.form['dob']
    student.age = request.form['age']
    student.institute_id = request.form['institute_id']
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/delete_student/<int:reg_no>')
def delete_student(reg_no):
    student = Student.query.get_or_404(reg_no)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))


# ====== Institute CRUD ======
@app.route('/institutes')
def institutes():
    institutes = Institute.query.all()
    return render_template('institute.html', institutes=institutes, institute=None)

@app.route('/add_institute', methods=['POST'])
def add_institute():
    i = Institute(id=request.form['id'] ,name=request.form['name'], address=request.form['address'], 
                  student_strength=request.form['student_strength'], date_of_inception=request.form['date_of_inception'])
    db.session.add(i)
    db.session.commit()
    return redirect(url_for('institutes'))

@app.route('/edit_institute/<int:id>')
def edit_institute(id):
    institute = Institute.query.get(id)
    institutes = Institute.query.all()
    return render_template('institute.html', institute=institute, institutes=institutes)

@app.route('/update_institute/<int:id>', methods=['POST'])
def update_institute(id):
    i = Institute.query.get(id)
    i.id=request.form['id']
    i.name = request.form['name']
    i.address = request.form['address']
    i.student_strength = request.form['student_strength']
    i.date_of_inception = request.form['date_of_inception']
    db.session.commit()
    return redirect(url_for('institutes'))

@app.route('/delete_institute/<int:id>')
def delete_institute(id):
    db.session.delete(Institute.query.get(id))
    db.session.commit()
    return redirect(url_for('institutes'))

# LIBRARY
@app.route('/libraries')
def libraries():
    libraries = Library.query.all()
    return render_template('library.html', libraries=libraries, library=None)

@app.route('/add_library', methods=['POST'])
def add_library():
    l = Library(name=request.form['name'], date_of_inception=request.form['date_of_inception'], 
                floor_no=request.form['floor_no'], 
                institute_id=request.form['institute_id'])
    db.session.add(l)
    db.session.commit()
    return redirect(url_for('libraries'))

@app.route('/edit_library/<int:id>')
def edit_library(id):
    library = Library.query.get(id)
    libraries = Library.query.all()
    return render_template('library.html', library=library, libraries=libraries)

@app.route('/update_library/<int:id>', methods=['POST'])
def update_library(id):
    l = Library.query.get(id)
    l.name = request.form['name']
    l.date_of_inception = request.form['date_of_inception']
    l.floor_no = request.form['floor_no']

    l.institute_id = request.form['institute_id']
    db.session.commit()
    return redirect(url_for('libraries'))

@app.route('/delete_library/<int:id>')
def delete_library(id):
    db.session.delete(Library.query.get(id))
    db.session.commit()
    return redirect(url_for('libraries'))

# BOOK
@app.route('/books')
def books():
    books = Books.query.all()
    authors = Authors.query.all()
    return render_template('book.html', books=books, book=None, all_authors=authors)

@app.route('/add_book', methods=['POST'])
def add_book():
    author_ids = request.form.getlist('authors')  # get multiple author IDs
    authors = Authors.query.filter(Authors.id.in_(author_ids)).all()

    b = Books(
        book_id=request.form['book_id'],
        title=request.form['title'],
        no_of_pages=request.form['no_of_pages'],
        publisher_name=request.form['publisher_name'],
        published_date=request.form['published_date'],
        edition=request.form['edition'],
        library_id=request.form['library_id'],
        authors=authors  # assign the list of author objects
    )
    db.session.add(b)
    db.session.commit()
    return redirect(url_for('books'))

@app.route('/edit_book/<int:id>')
def edit_book(id):
    book = Books.query.get(id)
    books = Books.query.all()
    authors = Authors.query.all()
    return render_template('book.html', book=book, books=books, all_authors=authors)

@app.route('/update_book/<int:id>', methods=['POST'])
def update_book(id):
    b = Books.query.get(id)
    b.title = request.form['title']
    b.no_of_pages = request.form['no_of_pages']
    b.publisher_name = request.form['publisher_name']
    b.published_date = request.form['published_date']
    b.edition = request.form['edition']
    b.library_id = request.form['library_id']

    # update authors list
    author_ids = request.form.getlist('authors')
    authors = Authors.query.filter(Authors.id.in_(author_ids)).all()
    b.authors = authors

    db.session.commit()
    return redirect(url_for('books'))

@app.route('/delete_book/<int:id>')
def delete_book(id):
    db.session.delete(Books.query.get(id))
    db.session.commit()
    return redirect(url_for('books'))

# LIBRARIAN
@app.route('/librarians')
def librarians():
    librarians = Librarian.query.all()
    return render_template('librarian.html', librarians=librarians, librarian=None)

@app.route('/add_librarian', methods=['POST'])
def add_librarian():
    lb = Librarian(employee_id=request.form['employee_id'], name=request.form['name'],
                   salary=request.form['salary'], dob=request.form['dob'], age=request.form['age'],
                   address=request.form['address'])
    db.session.add(lb)
    db.session.commit()
    return redirect(url_for('librarians'))

@app.route('/edit_librarian/<int:id>')
def edit_librarian(id):
    librarian = Librarian.query.get(id)
    librarians = Librarian.query.all()
    return render_template('librarian.html', librarian=librarian, librarians=librarians)

@app.route('/update_librarian/<int:id>', methods=['POST'])
def update_librarian(id):
    lb = Librarian.query.get(id)
    lb.name = request.form['name']
    lb.salary = request.form['salary']
    lb.dob = request.form['dob']
    lb.age = request.form['age']
    lb.address = request.form['address']
    db.session.commit()
    return redirect(url_for('librarians'))

@app.route('/delete_librarian/<int:id>')
def delete_librarian(id):
    db.session.delete(Librarian.query.get(id))
    db.session.commit()
    return redirect(url_for('librarians'))

#--------teacher CRUD-------------
@app.route('/teachers')
def teachers():
    teachers = Teachers.query.all()
    return render_template('teachers.html', teachers=teachers, teacher=None)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    teacher = Teachers(
        employee_id=request.form['employee_id'],
        name=request.form['name'],
        salary=request.form['salary'],  # Assuming spelling 'salery' is intentional based on your model
        phone_no=request.form['phone_no'],
        address=request.form['address'],
        dob=request.form['dob'],
        age=request.form['age']
    )
    db.session.add(teacher)
    db.session.commit()
    return redirect(url_for('teachers'))

@app.route('/edit_teacher/<int:id>')
def edit_teacher(id):
    teacher = Teachers.query.get_or_404(id)
    teachers = Teachers.query.all()
    return render_template('teachers.html', teachers=teachers, teacher=teacher)

@app.route('/update_teacher/<int:id>', methods=['POST'])
def update_teacher(id):
    teacher = Teachers.query.get_or_404(id)
    teacher.name = request.form['name']
    teacher.salary = request.form['salary']
    teacher.phone_no = request.form['phone_no']
    teacher.address = request.form['address']
    teacher.dob = request.form['dob']
    teacher.age = request.form['age']
    db.session.commit()
    return redirect(url_for('teachers'))

@app.route('/delete_teacher/<int:id>')
def delete_teacher(id):
    teacher = Teachers.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('teachers'))


#-------------------Director------------
@app.route('/directors')
def directors():
    directors = Director.query.all()
    return render_template('director.html', directors=directors, director=None)

@app.route('/add_director', methods=['POST'])
def add_director():
    director = Director(
        employee_id=request.form['employee_id'],
        name=request.form['name'],
        salary=request.form['salary'],
        phone_no=request.form['phone_no'],
        address=request.form['address'],
        dob=request.form['dob'],
        age=request.form['age']
    )
    db.session.add(director)
    db.session.commit()
    return redirect(url_for('directors'))

@app.route('/edit_director/<int:id>')
def edit_director(id):
    director = Director.query.get_or_404(id)
    directors = Director.query.all()
    return render_template('director.html', directors=directors, director=director)

@app.route('/update_director/<int:id>', methods=['POST'])
def update_director(id):
    director = Director.query.get_or_404(id)
    director.name = request.form['name']
    director.salary = request.form['salary']
    director.phone_no = request.form['phone_no']
    director.address = request.form['address']
    director.dob = request.form['dob']
    director.age = request.form['age']
    db.session.commit()
    return redirect(url_for('directors'))

@app.route('/delete_director/<int:id>')
def delete_director(id):
    director = Director.query.get_or_404(id)
    db.session.delete(director)
    db.session.commit()
    return redirect(url_for('directors'))


#-------------Authors------------
@app.route('/authors')
def authors():
    authors = Authors.query.all()
    return render_template('authors.html', authors=authors, author=None)

@app.route('/add_author', methods=['POST'])
def add_author():
    author = Authors(
        name=request.form['name'],
        salary=request.form['salary'],
        phone_no=request.form['phone_no'],
        address=request.form['address'],
        dob=request.form['dob'],
        age=request.form['age']
    )
    db.session.add(author)
    db.session.commit()
    return redirect(url_for('authors'))

@app.route('/edit_author/<int:id>')
def edit_author(id):
    author = Authors.query.get_or_404(id)
    authors = Authors.query.all()
    return render_template('authors.html', authors=authors, author=author)

@app.route('/update_author/<int:id>', methods=['POST'])
def update_author(id):
    author = Authors.query.get_or_404(id)
    author.name = request.form['name']
    author.salary = request.form['salary']
    author.phone_no = request.form['phone_no']
    author.address = request.form['address']
    author.dob = request.form['dob']
    author.age = request.form['age']
    db.session.commit()
    return redirect(url_for('authors'))

@app.route('/delete_author/<int:id>')
def delete_author(id):
    author = Authors.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('authors'))


#-----------------Vehicle-------------
@app.route('/vehicles')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('vehicle.html', vehicles=vehicles, vehicle=None)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    vehicle = Vehicle(
        registration_id=request.form['registration_id'],
        color=request.form['color'],
        top_speed=request.form['top_speed'],
        length=request.form['length'],
        hp=request.form['hp']
    )
    db.session.add(vehicle)
    db.session.commit()
    return redirect(url_for('vehicles'))

@app.route('/edit_vehicle/<string:registration_id>')
def edit_vehicle(registration_id):
    vehicle = Vehicle.query.get_or_404(registration_id)
    vehicles = Vehicle.query.all()
    return render_template('vehicle.html', vehicles=vehicles, vehicle=vehicle)

@app.route('/update_vehicle/<string:registration_id>', methods=['POST'])
def update_vehicle(registration_id):
    vehicle = Vehicle.query.get_or_404(registration_id)
    vehicle.color = request.form['color']
    vehicle.top_speed = request.form['top_speed']
    vehicle.length = request.form['length']
    vehicle.hp = request.form['hp']
    db.session.commit()
    return redirect(url_for('vehicles'))

@app.route('/delete_vehicle/<string:registration_id>')
def delete_vehicle(registration_id):
    vehicle = Vehicle.query.get_or_404(registration_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('vehicles'))


#-----------------Publisher---------
@app.route('/publishers')
def publishers():
    publishers = Publisher.query.all()
    return render_template('publisher.html', publishers=publishers, publisher=None)

@app.route('/add_publisher', methods=['POST'])
def add_publisher():
    publisher = Publisher(
        name=request.form['name'],
        address=request.form['address'],
        ceo_name=request.form['ceo_name'],
        establishment_date=request.form['establishment_date'],
        contact_no=request.form['contact_no']
    )
    db.session.add(publisher)
    db.session.commit()
    return redirect(url_for('publishers'))

@app.route('/edit_publisher/<string:name>')
def edit_publisher(name):
    publisher = Publisher.query.get_or_404(name)
    publishers = Publisher.query.all()
    return render_template('publisher.html', publishers=publishers, publisher=publisher)

@app.route('/update_publisher/<string:name>', methods=['POST'])
def update_publisher(name):
    publisher = Publisher.query.get_or_404(name)
    publisher.address = request.form['address']
    publisher.ceo_name = request.form['ceo_name']
    publisher.establishment_date = request.form['establishment_date']
    publisher.contact_no = request.form['contact_no']
    db.session.commit()
    return redirect(url_for('publishers'))

@app.route('/delete_publisher/<string:name>')
def delete_publisher(name):
    publisher = Publisher.query.get_or_404(name)
    db.session.delete(publisher)
    db.session.commit()
    return redirect(url_for('publishers'))


@app.route('/images')
def images():
    return render_template('image.html')

if __name__ == '__main__':
    app.run(debug=True)
