from flask import Flask, render_template, request, session, redirect, url_for # this is importing required modules like render template html files render krega, request, and session is used to store info temporoary like how many questiions user have answered
from questions import quiz_data, get_categories, get_questions 

app = Flask(__name__)
app.secret_key = 'mykey' # This key needed it will make data encypted from hackers 

# Route 1 this is home page route means jb user domain/ pr hoga so ye page remder hoga 
@app.route('/')
def index(): # ye function run hoga when jb "/" route call hoga
    session.clear() # ye session jisme tempory data store hoga voh clear hoga before starting quiz agani
    categories = get_categories() 
    return render_template('index.html', categories=categories) # this will render html home page 

# Route 2: jab user category select karke quiz start karta hai
@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    category = request.form.get('category')
    # yahan form se category aa rahi hai jo user ne select ki hoti hai

    session['category'] = category
    # category ko session me is liye store kar rahe hain
    # taake next pages par bhi pata rahe quiz kis category ka hai

    session['questions'] = get_questions(category)
    # selected category ke saare questions ek list me aa jate hain
    # nd then we in session

    session['current_question'] = 0
    # current_question index track karega ke user kis question par hai

    session['score'] = 0
    # score 0 se start hota hai aur har correct answer par increase hoga

    session['user_answers'] = []
    # is list me hum har question ka user answer + correct answer store karenge
    # taake result page par detail show kar saken

    return redirect(url_for('quiz'))
    # setup complete hone ke baad user ko quiz page par bhej dete hain


# Route 3: yeh route har dafa current question show karta hai
@app.route('/quiz')
def quiz():
    if 'questions' not in session:
        # agar user direct /quiz URL hit kare bina quiz start kiye
        # to usko wapas home page bhej dete hain
        return redirect(url_for('index'))

    current_q = session['current_question']
    questions = session['questions']
    # session se current question number aur questions list nikal rahe hain

    if current_q >= len(questions):
        # jab current question number total questions se zyada ho jaye
        # iska matlab quiz complete ho chuka hai
        return redirect(url_for('result'))

    question_data = questions[current_q]
    # current question ka data (question + options + answer)

    total_questions = len(questions)
    # total number of questions quiz me

    return render_template(
        'index.html',
        question=question_data,
        question_number=current_q + 1,
        total_questions=total_questions,
        category=session['category'],
        quiz_started=True
    )
    # yahan same index.html reuse ho rahi hai
    # lekin ab quiz mode me question show ho raha hai


# Route 4: jab user answer submit karta hai
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session:
        # safety check
        return redirect(url_for('index'))

    user_answer = request.form.get('answer')
    # user ne jo option select kiya hai

    current_q = session['current_question']
    questions = session['questions']

    correct_answer = questions[current_q]['answer']
    # current question ka correct answer nikal rahe hain

    session['user_answers'].append({
        'question': questions[current_q]['question'],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': user_answer == correct_answer
    })
    # har question ka complete record save kar rahe hain
    # taake result page par analysis ho sake

    if user_answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
        # agar answer sahi ho to score increase kar dete hain

    session['current_question'] = current_q + 1
    # next question ke liye index increase

    return redirect(url_for('quiz'))
    # dubara quiz route par jaa ke next question load hoga


# Route 5: quiz complete hone ke baad result show karta hai
@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('index'))

    score = session['score']
    total = len(session['questions'])
    percentage = (score / total) * 100
    # final percentage calculate kar rahe hain

    user_answers = session['user_answers']
    category = session['category']

    return render_template(
        'result.html',
        score=score,
        total=total,
        percentage=percentage,
        user_answers=user_answers,
        category=category
    )
    # result.html par complete quiz summary show hoti hai


if __name__ == '__main__':
    app.run(debug=True)
    # debug mode development ke liye use hota hai
