import sys
import pandas as pd
from flask import Flask, render_template, request
from config.paths_config import *
from utils.helpers import *
from pipeline.prediction_pipeline import hybrid_recommendation
from src.custom_exception import AppException

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    error_message = None
    anime_titles = pd.read_csv(DF)["eng_version"].dropna().unique().tolist() 
    anime_titles = sorted(anime_titles)

    if request.method == 'POST':
        try:
            user_id_input = request.form.get("userID")
            favorites_input = request.form.getlist("favorites")  # get selected titles from dropdown
            rating_df = pd.read_csv(RATING_DF)

            if user_id_input:
                user_id = int(user_id_input)
                if is_new_user(user_id, rating_df):
                    error_message = f"No history for user {user_id}. Try selecting your favorite anime titles below."
                else:
                    recommendations = hybrid_recommendation(user_id)

            elif favorites_input:
                recommendations = cold_start_from_favorites(favorites_input)

            else:
                error_message = "Please enter a user ID or select favorite anime titles."

            print("Recommendations:", recommendations)
            print("Error:", error_message)

        except Exception as e:
            error_message = str(e)

    return render_template('index.html', recommendations=recommendations, error_message=error_message, anime_titles=anime_titles)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)