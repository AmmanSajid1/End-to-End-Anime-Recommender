from config.paths_config import * 
from utils.helpers import * 


def hybrid_recommendation(user_id,  user_weight=0.5, content_weight=0.5, n=10):
    ######### User Based Recommendation (Collabortaive Filtering) ################
    user_pref = get_user_preferences(user_id, RATING_DF, DF)
    if user_pref.empty:
        raise ValueError(f"User ID {user_id} not found or has insufficient data.")
    
    similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED, n=n)
    
    user_recommendations = get_user_recommendations(similar_users, user_pref, DF, SYNOPSIS_DF, RATING_DF, n=n)

    user_recommendations_list = user_recommendations["anime_name"].tolist()

    ######### Content based Recommendation #############################
    content_recommended_animes = []

    for anime in user_recommendations_list:
        similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, DF, n=n)

        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes["name"].tolist())
        
        else:
            print(f"No similar animes found for {anime}")


    ################ Combine Recommendations ##############################
    combined_scores = {}

    for anime in user_recommendations_list:
        combined_scores[anime] = combined_scores.get(anime, 0) + user_weight

    for anime in content_recommended_animes:
        combined_scores[anime] = combined_scores.get(anime, 0) + content_weight

    sorted_animes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    recommended_titles = list(dict.fromkeys([anime for anime, score in sorted_animes[:n*2]]))[:n]

    recommendations = []
    for title in recommended_titles:
        anime_frame = get_anime_frame(title, DF)
        if anime_frame.empty:
            print(f"No data found for: {title}")
            continue  # skip to next

        anime_id = anime_frame["anime_id"].values[0]
        image_url = get_anime_image(anime_id)
        recommendations.append({"title": title, "image_url": image_url})

    return recommendations


