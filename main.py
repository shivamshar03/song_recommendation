from flask import Flask, jsonify
import requests
from pymongo import MongoClient
import pickle
import pandas as pd
from lightfm.data import Dataset
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)


app = Flask(__name__)

def get_user_id():
    response = requests.get("/user_id")
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data"}

def get_recommendations(user_id, model_path="lightfm_model.pkl", users_csv="/content/users.csv", songs_csv="/content/songs.csv", n_recommendations=10):
    """
    Loads a trained LightFM model and provides song recommendations for a given user.

    Args:
        user_id (str): The ID of the user for whom to generate recommendations.
        model_path (str): The path to the saved LightFM model file.
        users_csv (str): The path to the users data CSV file.
        songs_csv (str): The path to the songs data CSV file.
        n_recommendations (int): The number of top recommendations to return.

    Returns:
        pandas.DataFrame: A DataFrame containing the top recommended songs with their names, artist names, and genre names.
    """
    # Load the saved LightFM model
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        return None

    # Load the users and songs dataframes
    try:
        users_df = pd.read_csv(users_csv)
        songs_df = pd.read_csv(songs_csv)
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return None

    # Recreate the dataset object and fit it with users and songs, including features
    dataset = Dataset()

    user_feature_columns = [col for col in users_df.columns if col != '_id']
    item_feature_columns = [col for col in songs_df.columns if col != '_id']

    dataset.fit(
        users_df['_id'],
        songs_df['_id'],
        user_features=user_feature_columns,
        item_features=item_feature_columns
    )

    # Build user and item features (must be done again to match the dataset object)
    user_features = dataset.build_user_features(
        ((row['_id'], [col for col in user_feature_columns if pd.notna(row[col])]) for index, row in users_df.iterrows())
    )

    item_features = dataset.build_item_features(
        ((row['_id'], [col for col in item_feature_columns if pd.notna(row[col])]) for index, row in songs_df.iterrows())
    )

    # Get the internal user ID for the selected user
    try:
        user_internal_id = dataset.mapping()[0][user_id]
    except KeyError:
        print(f"Error: User ID '{user_id}' not found in the dataset.")
        return None


    # Get the internal item IDs for all songs
    item_internal_ids = list(dataset.mapping()[2].values())

    # Predict scores for all songs for the selected user
    predicted_scores = model.predict(user_internal_id, item_internal_ids, user_features=user_features, item_features=item_features)

    # Get mapping of internal item IDs back to original song IDs
    item_id_map = {v: k for k, v in dataset.mapping()[2].items()}

    # Create a pandas Series of predicted scores with original song IDs as index
    predicted_scores_series = pd.Series(predicted_scores, index=[item_id_map[i] for i in item_internal_ids])

    # Sort the scores in descending order
    sorted_predictions = predicted_scores_series.sort_values(ascending=False)

    # Get the top N song IDs
    top_song_ids = sorted_predictions.head(n_recommendations).index.tolist()

    # Retrieve song information for the top N song IDs
    top_recommended_songs = songs_df[songs_df['_id'].isin(top_song_ids)].set_index('_id').loc[top_song_ids].reset_index()

    return top_recommended_songs[['_id','name', 'artistName', 'genreName']]


@app.route('/recommended_songs', methods=['GET'])
def process_and_send():
    user_id = get_user_id()
    client = MongoClient(MONGO_URI)  # replace with your URI if using Atlas

    # 2. Access database and collection
    db = client["Popil"]
    songs_collection = db["songs"]
    users_collection = db["users"]

    # 3. Fetch all documents
    songs_data = list(songs_collection.find())
    users_data = list(users_collection.find())

    # 5. Convert to DataFrame
    songs_df = pd.DataFrame(songs_data)
    users_df = pd.DataFrame(users_data)

    # 6. Export to CSV
    songs_df.to_csv("songs.csv", index=False)
    users_df.to_csv("users.csv", index=False)

    recommended_songs_df = get_recommendations(user_id)

    # Convert DataFrame to a list of dictionaries for JSON serialization
    recommended_songs_list = recommended_songs_df.to_dict(orient='records')

    return jsonify(recommended_songs_list)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)