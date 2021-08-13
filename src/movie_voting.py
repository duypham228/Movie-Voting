from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Polls, Topics

movie_voting = Flask(__name__)

# load config from the config file we created earlier
movie_voting.config.from_object('config')

# initialize and create the database 
db.init_app(movie_voting)
db.create_all(app=movie_voting)
migrate = Migrate(movie_voting, db, render_as_batch=True)

@movie_voting.route('/')
def home():
    return render_template('index.html')

@movie_voting.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get user details from the form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # hash the password
        password = generate_password_hash(password)
        user = Users(email=email, username=username, password=password)

        db.session.add(user)
        db.session.commit()

        flash('Thanks for signing up please login')

        return redirect(url_for('home'))

    # it's a GET request, just render the template
    return render_template('signup.html')

@movie_voting.route('/login', methods=['POST'])
def login():
    # we don't need to check the request type as flask will raise a bad request     # error if a request aside from POST is made to this url 
    username = request.form['username']
    password = request.form['password']

    # search the database for the User     
    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password

        if check_password_hash(password_hash, password):
            # The hash matches the password in the database log the user in             
            session['user'] = username
            flash('Login was succesfull')
    else:
        # user wasn't found in the database         
        flash('Username or password is incorrect please try again', 'error')

    return redirect(url_for('home'))

@movie_voting.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash('We hope to see you again!')
    return redirect(url_for('home'))

@movie_voting.route('/api/polls', methods=['GET', 'POST'])
# retrieves/adds polls from/to the database 
def api_polls():
    if request.method == 'POST':
        # get the poll and save it in the database         
        poll = request.get_json()

        # simple validation to check if all values are properly secret         
        for key, value in poll.items():
            if not value:
                return jsonify({'error': 'value for {} is empty'.format(key)})

        title = poll['title']
        options_query = lambda option : Options.query.filter(Options.name.like(option))

        options = [Polls(option=Options(name=option))
            if options_query(option).count() == 0
            else Polls(option=options_query(option).first()) for option in poll['options']
        ]

        new_topic = Topics(title=title, options=options)

        db.session.add(new_topic)
        db.session.commit()

        return jsonify({'message': 'Poll was created succesfully'})

    else:
        # it's a GET request, return dict representations of the API         
        polls = Topics.query.join(Polls).all()
        all_polls = {'Polls':  [poll.to_json() for poll in polls]}

        return jsonify(all_polls)

@movie_voting.route('/api/polls/options')
def api_polls_options():

    all_options = [option.to_json() for option in Options.query.all()]

    return jsonify(all_options)


@movie_voting.route('/api/poll/vote', methods=['PATCH'])
def api_poll_vote():

    poll = request.get_json()

    poll_title, option = (poll['poll_title'], poll['option'])

    join_tables = Polls.query.join(Topics).join(Options)
    # filter options     
    option = join_tables.filter(Topics.title.like(poll_title)).filter(Options.name.like(option)).first()

    # increment vote_count by 1 if the option was found     
    if option:
        option.vote_count += 1
        db.session.commit()

        return jsonify({'message': 'Thank you for voting'})

    return jsonify({'message': 'option or poll was not found please try again'})

@movie_voting.route('/polls', methods=['GET'])
def polls():
    return render_template('polls.html')

# if __name__ == '__main__':
#     movie_voting.run()

