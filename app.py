from flask import Flask, render_template, request, redirect
from models import db, StudentModel

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Disable track modifications to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database with the Flask app
db.init_app(app)

# Create the database tables manually
with app.app_context():
    db.create_all()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
    elif request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
                
        # Create a new student object
        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            
        )
        
        # Add the student to the database session
        db.session.add(student)
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the homepage
        return redirect('/')

@app.route('/')
def RetrieveList():
    # Retrieve all students from the database
    students = StudentModel.query.all()
    # Render the template with the list of students
    return render_template('datalist.html', students=students)

@app.route('/<int:id>')
def RetrieveStudent(id):
    # Retrieve a student by ID from the database
    student = StudentModel.query.get(id)
    if student:
        # Render the template with the student's details
        return render_template('data.html', student=student)
    else:
        return f"Student with id = {id} does not exist"

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    # Retrieve the student to be updated
    student = StudentModel.query.get(id)
    
    if request.method == 'POST':
        if student:
            # Delete the existing student
            db.session.delete(student)
            db.session.commit()
    
        # Extract form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        
        # Create a new student object with updated details
        updated_student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            
        )
        # Add the updated student to the database session
        db.session.add(updated_student)
        db.session.commit()
        return redirect('/')
    else:
        # Render the template for editing student details
        return render_template('update.html', student=student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    # Retrieve the student to be deleted
    student = StudentModel.query.get(id)
    if request.method == 'POST':
        if student:
            # Delete the student
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
        else:
            return f"Student with id = {id} does not exist"
    else:
        # Render the template for confirming deletion
        return render_template('delete.html')

if __name__ == "__main__":
    # Run the Flask application
    app.run(host='localhost', port=5000)
