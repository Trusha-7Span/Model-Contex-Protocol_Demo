from flask import Flask, session, request, render_template
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'mcp-bollywood-secret-key'
app.permanent_session_lifetime = timedelta(minutes=10)

# Updated Bollywood movie database by genre
movie_database = {
    'romantic': ['Dilwale Dulhania Le Jayenge', 'Kabhi Khushi Kabhie Gham', 'Jab Tak Hai Jaan', 'Pride and Prejudice', 'Aashiqui 2'],
    'action': ['Dhoom', 'Bang Bang', 'War', 'Sultan', 'Sholay'],
    'comedy': ['3 Idiots', 'Andheri Raat Mein Diya', 'Hera Pheri', 'Chupke Chupke', 'Chhichhore'],
    'drama': ['Gully Boy', 'Taare Zameen Par', 'Lagaan', 'Zindagi Na Milegi Dobara', 'Barfi!'],
    'thriller': ['Kahaani', 'Talaash', 'Drishyam', 'Race 3', 'Kahaani 2'],
    'horror': ['Stree', 'Bhoot', 'Raat', 'The House Next Door', '1920'],
    'family': ['Dil Dhadakne Do', 'Kabhi Alvida Naa Kehna', 'Piku', 'Taare Zameen Par', 'Bajrangi Bhaijaan'],
}

@app.route('/', methods=['GET', 'POST'])
def index():
    session.permanent = True
    if 'user_name' not in session:
        session['user_name'] = 'Guest'
        session['preferred_genre'] = 'romantic'
        session['history'] = []

    # Handle genre selection and movie recommendation
    if request.method == 'POST':
        genre = request.form.get('genre')
        if genre:
            session['preferred_genre'] = genre
            recommended_movies = movie_database.get(genre, [])
            session['history'] = recommended_movies[:5]  # Keep only top 5 recommended movies

    # Fetch the current genre and recommendation history
    current_genre = session.get('preferred_genre')
    movie_recommendations = session.get('history', [])

    return render_template('index.html', 
                           name=session['user_name'], 
                           current_genre=current_genre, 
                           recommendations=movie_recommendations)

if __name__ == '__main__':
    app.run(debug=True)
