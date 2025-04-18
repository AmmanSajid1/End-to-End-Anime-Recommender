import pandas as pd 
import numpy as np 
import joblib 
import requests
import time
from config.paths_config import * 

################### 1. GET ANIME FRAME ########################

def get_anime_frame(anime, path_df):

    df = pd.read_csv(path_df)

    if isinstance(anime,int):
        return df[df["anime_id"] == anime]
    
    if isinstance(anime, str):
        return df[df["eng_version"] == anime]
    

################### 2. GET_SYNOPSIS ###########################
def get_synopsis(anime, path_synopsis_df):

    synopsis_df = pd.read_csv(path_synopsis_df)

    if isinstance(anime, int):
        return synopsis_df[synopsis_df["MAL_ID"] == anime]["sypnopsis"].values[0]
    
    if isinstance(anime, str):
        return synopsis_df[synopsis_df["Name"] == anime]["sypnopsis"].values[0]
    

################# 3. CONTENT RECOMMENDATION ####################
def find_similar_animes(name, path_anime_weights, path_anime2anime_encoded, path_anime2anime_decoded, path_anime_df, n=10, return_dist=False, neg=False):

    anime_weights = joblib.load(path_anime_weights)
    anime2anime_encoded = joblib.load(path_anime2anime_encoded)
    anime2anime_decoded = joblib.load(path_anime2anime_decoded)

    # Get the anime_id for the given name
    index = get_anime_frame(name, path_anime_df).anime_id.values[0]
    encoded_index = anime2anime_encoded.get(index)

    if encoded_index is None:
        raise ValueError(f"Encoded index not found for anime ID: {index}")

    weights = anime_weights

    # Compute the similarity distances
    dists = np.dot(weights, weights[encoded_index])  # Ensure weights[encoded_index] is a 1D array
    sorted_dists = np.argsort(dists)

    n = n + 1

    # Select closest or farthest based on 'neg' flag
    if neg:
        closest = sorted_dists[:n]
    else:
        closest = sorted_dists[-n:]

    # Return distances and closest indices if requested
    if return_dist:
        return dists, closest

    # Build the similarity array
    SimilarityArr = []
    for close in closest:
        decoded_id = anime2anime_decoded.get(close)
       

       
        anime_frame = get_anime_frame(decoded_id, path_anime_df)

        anime_name = anime_frame.eng_version.values[0]
        genre = anime_frame.Genres.values[0]
        similarity = dists[close]
   

        SimilarityArr.append({
            "anime_id": decoded_id,
            "name": anime_name,
            "similarity": similarity,
            "genre": genre,
        })
       

    # Create a DataFrame with results and sort by similarity
    Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
    return Frame[Frame.anime_id != index].drop(['anime_id'], axis=1)


################### 4. FIND SIMILAR USERS ##############################################
def find_similar_users(item_input , path_user_weights , path_user2user_encoded , path_user2user_decoded, n=10 , return_dist=False,neg=False):
    try:
        user_weights = joblib.load(path_user_weights)
        user2user_encoded = joblib.load(path_user2user_encoded)
        user2user_decoded = joblib.load(path_user2user_decoded)

        index=item_input
        encoded_index = user2user_encoded.get(index)

        weights = user_weights

        dists = np.dot(weights,weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n=n+1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
            

        if return_dist:
            return dists,closest
        
        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            if isinstance(item_input,int):
                decoded_id = user2user_decoded.get(close)
                SimilarityArr.append({
                    "similar_users" : decoded_id,
                    "similarity" : similarity
                })
        similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity",ascending=False)
        similar_users = similar_users[similar_users.similar_users != item_input]
        return similar_users
    except Exception as e:
        print("Error Occured",e)


################### 5. GET USER PREFERENCES #########################################################
def get_user_preferences(user_id, path_rating_df, path_anime_df):

    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_anime_df)

    animes_watched_by_user = rating_df[rating_df["user_id"] == user_id]

    user_rating_percentile = np.percentile(animes_watched_by_user["rating"], 75)

    animes_watched_by_user = animes_watched_by_user[animes_watched_by_user["rating"] >= user_rating_percentile]

    top_animes_user = (
        animes_watched_by_user.sort_values(by="rating", ascending=False)["anime_id"].values
    )

    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version", "Genres"]]

    return anime_df_rows


####################### 6. GET USER BASED RECOMMENDATIONS #################################
def get_user_recommendations(similar_users, user_pref, path_anime_df, path_synopsis_df, path_rating_df, n=10):

    recommended_animes = []
    anime_list = []

    for user_id in similar_users["similar_users"]:
        pref_list = get_user_preferences(int(user_id), path_rating_df, path_anime_df)
        # Filter out animes already watched by user
        pref_list = pref_list[~pref_list["eng_version"].isin(user_pref["eng_version"].values)]
        
        if not pref_list.empty:
            anime_list.append(pref_list["eng_version"].values)

    if anime_list:
        anime_list = pd.DataFrame(anime_list)

        sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)

        for i, anime_name in enumerate(sorted_list.index):
            n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]

            if isinstance(anime_name, str):
                frame = get_anime_frame(anime_name, path_anime_df)
                anime_id = frame["anime_id"].values[0]
                genre = frame["Genres"].values[0]
                synopsis = get_synopsis(int(anime_id), path_synopsis_df)

                recommended_animes.append({
                    "n": n_user_pref,
                    "anime_name": anime_name,
                    "Genres": genre,
                    "Synopsis": synopsis
                })

    return pd.DataFrame(recommended_animes).head(n)



################################# 7. GET ANIME POSTERS ############################################
def get_anime_image(mal_id):
    try:
        time.sleep(0.5)  # sleep for 500ms between requests
        url = f"https://api.jikan.moe/v4/anime/{mal_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["data"]["images"]["jpg"]["image_url"]
    except Exception as e:
        print(f"Error fetching image for anime ID {mal_id}: {e}")
        return "https://via.placeholder.com/150x220?text=No+Image"



############################### 8. CHECK IF NEW USER #############################################
def is_new_user(user_id, rating_df):
    return user_id not in rating_df["user_id"].values

############################### 9. COLD START FUNCTION ###########################################
def cold_start_from_favorites(favorite_titles, n=10):
    recommendations = []
    seen = set()

    for title in favorite_titles:
        try:
            similar_animes = find_similar_animes(
                title,
                ANIME_WEIGHTS_PATH,
                ANIME2ANIME_ENCODED,
                ANIME2ANIME_DECODED,
                DF,
                n=n
            )

            for _, row in similar_animes.iterrows():
                anime_title = row["name"]
                if anime_title not in seen:
                    seen.add(anime_title)

                    anime_frame = get_anime_frame(anime_title, DF)
                    if anime_frame.empty:
                        print(f"No anime frame for title: {anime_title}")
                        continue

                    anime_id = anime_frame["anime_id"].values[0]
                    image_url = get_anime_image(anime_id)
                    recommendations.append({"title": anime_title, "image_url": image_url})

                if len(recommendations) >= n:
                    break
            if len(recommendations) >= n:
                break

        except Exception as e:
            print(f"Could not fetch similar animes for: {title} - {e}")

    return recommendations
