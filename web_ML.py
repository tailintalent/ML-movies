import numpy as np
from flask import Flask, url_for, request, redirect, render_template
from pymongo import MongoClient

#setting up database
client = MongoClient('localhost', 27017)
db = client.mlMovieDb
movie_to_rate = db.movie_to_rate  #user's rating will be save into this collection

#Initiating
app = Flask(__name__)
Movie_num_chosen = [1, 4, 6, 7, 15]
Movie_chosen = ['Godfather', 'Gone with the wind', 'Scent of a Woman', 'Fast & Furious', 'The Shawshank Redemption']
num_movie=len(Movie_chosen)
Y =np.zeros((len(Movie_chosen),1))

@app.route('/')
@app.route('/Movies/', methods=['GET','POST'])
def ML():
    rate=1
    if request.method == 'POST':
        rate=request.form['name']
        redirect(url_for('ML_updated',Rating=rate))
    return render_template('ML.html',Movie_chosen=Movie_chosen,num_movie=num_movie,Rating=rate)

@app.route('/')
@app.route('/Movies/updated/<int:Rating>')
def ML_updated(Rating):
    return render_template('ML_updated.html',Movie_chosen=Movie_chosen,num_movie=num_movie,Rating=Rating,movie_to_rate=movie_to_rate)


@app.route('/Movies/<int:movie_id>/', methods=['GET','POST'])
def ML_newMovie(movie_id):
    if request.method == 'POST':
        Rating = request.form['name']
        newRating={Movie_chosen[movie_id]:Rating}
        movie_to_rate.insert(newRating)
        return render_template('ML_updated.html',Movie_chosen=Movie_chosen,num_movie=num_movie,Rating=Rating,movie_to_rate=movie_to_rate)
    else:
        return render_template('ML_newMovie.html',Movie_chosen=Movie_chosen,movie_id=movie_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    client.close()
    print Y[0]
