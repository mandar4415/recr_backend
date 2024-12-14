from flask import Blueprint, jsonify, request
from services.ai_ml_insights import rank_candidates_with_insights

# Define the Blueprint for Insights API
insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/rank_with_insights", methods=["POST"])
def get_ranked_candidates_with_insights():
    """
    API endpoint to rank candidates and generate AI-driven insights.
    Example Input: { "job_title": "Web Developer", "skills": "Python, JavaScript" }
    Returns:
        JSON response containing:
        - candidates: List of top-ranked candidates.
        - insights: Analytical insights (skill distribution, salary comparison, etc.).
    """
    try:
        # Parse input payload
        payload = request.json
        if not payload:
            return jsonify({"error": "Invalid input. Please provide a valid JSON payload."}), 400

        job_title = payload.get("job_title", "").strip()
        skills = payload.get("skills", "").strip()

        # Validate required fields
        if not job_title or not skills:
            return jsonify({"error": "Both 'job_title' and 'skills' are required."}), 400

        # Call the service function to get ranked candidates and insights
        ranked_candidates, insights = rank_candidates_with_insights(job_title, skills)

        # Return the response
        return jsonify({"candidates": ranked_candidates, "insights": insights}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
