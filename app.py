# app.py - Main Flask Application

from flask import Flask, render_template, request, session, redirect, url_for
from questions import quiz_data, get_categories, get_questions

app = Flask(__name__)
app.secret_key = 'mykey' # Needed for session management

# Route 1: Home page - Select category and start quiz
@app.route('/')
def index():
    # Clear session when visiting home page
    session.clear()
    categories = get_categories()
    return render_template('index.html', categories=categories)

# Route 2: Start quiz for selected category
@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    category = request.form.get('category')
    
    # Initialize session variables
    session['category'] = category
    session['questions'] = get_questions(category)
    session['current_question'] = 0
    session['score'] = 0
    session['user_answers'] = []  # Store user's answers
    
    return redirect(url_for('quiz'))

# Route 3: Display current question
@app.route('/quiz')
def quiz():
    # Check if quiz is initialized
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    current_q = session['current_question']
    questions = session['questions']
    
    # Check if quiz is finished
    if current_q >= len(questions):
        return redirect(url_for('result'))
    
    question_data = questions[current_q]
    total_questions = len(questions)
    
    return render_template('index.html', 
                         question=question_data,
                         question_number=current_q + 1,
                         total_questions=total_questions,
                         category=session['category'],
                         quiz_started=True)

# Route 4: Submit answer and move to next question
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    user_answer = request.form.get('answer')
    current_q = session['current_question']
    questions = session['questions']
    
    # Get correct answer
    correct_answer = questions[current_q]['answer']
    
    # Store user's answer with question details
    session['user_answers'].append({
        'question': questions[current_q]['question'],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': user_answer == correct_answer
    })
    
    # Update score if correct
    if user_answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
    
    # Move to next question
    session['current_question'] = current_q + 1
    
    return redirect(url_for('quiz'))

# Route 5: Show results
@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('index'))
    
    score = session['score']
    total = len(session['questions'])
    percentage = (score / total) * 100
    user_answers = session['user_answers']
    category = session['category']
    
    return render_template('result.html',
                         score=score,
                         total=total,
                         percentage=percentage,
                         user_answers=user_answers,
                         category=category)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)