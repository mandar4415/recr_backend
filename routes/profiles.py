from flask import Blueprint, jsonify, request
from config.db import get_db
import pandas as pd

# Define Blueprint for Profiles API
profiles_bp = Blueprint("profiles", __name__)
db = get_db()

# Utility Functions for Profiles
def normalize_text(text):
    """Normalize text by converting to lowercase and stripping extra spaces."""
    if not isinstance(text, str):
        return text
    return text.strip().lower()

def filter_data(dataframe, filters):
    """
    Filter a DataFrame based on provided criteria.
    Args:
        dataframe (pd.DataFrame): DataFrame to filter.
        filters (dict): Filtering criteria (e.g., {"city": "New York", "skills": "Python"}).
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    filtered_df = dataframe
    for column, value in filters.items():
        if column in dataframe.columns and value:
            filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
    return filtered_df

# Route: Get All Profiles
@profiles_bp.route("/", methods=["GET"])
def get_all_profiles():
    """
    Fetch all profiles from the database.
    Returns:
        JSON: List of all profiles.
    """
    profiles = list(db.profiles.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify(profiles)

# Route: Filter Profiles
@profiles_bp.route("/filter", methods=["POST"])
def filter_profiles():
    """
    Filter profiles based on criteria provided in the request body.
    Example Input: { "city": "New York", "skills": "Python" }
    Returns:
        JSON: List of filtered profiles.
    """
    filters = request.json  # Expected JSON payload
    query = {}

    # Build MongoDB query dynamically based on filters
    if "city" in filters:
        query["city"] = filters["city"].lower()
    if "skills" in filters:
        query["skills"] = {"$regex": filters["skills"], "$options": "i"}

    # Query the database
    filtered_profiles = list(db.profiles.find(query, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify(filtered_profiles)
