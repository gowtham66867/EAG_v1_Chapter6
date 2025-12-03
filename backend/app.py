from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio

from decision_making import DecisionMaker
from memory import Memory

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/')
def home():
    """Home route with API information."""
    return jsonify({
        'message': 'Wellness Plan API',
        'endpoints': {
            '/api/generate-plan': {
                'method': 'POST',
                'description': 'Generate a wellness plan based on user profile',
                'example_payload': {
                    'goals': 'Improve fitness and sleep',
                    'sleep': '7',
                    'schedule': '9-5 office job',
                    'diet': 'Vegetarian'
                }
            }
        }
    })

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """API endpoint to generate a wellness plan."""
    user_profile_data = request.json
    
    # Format the user profile string as our agent expects it
    user_profile = (
        f"Goals: {user_profile_data.get('goals', '')}\n"
        f"Sleep Patterns: {user_profile_data.get('sleep', '')} hours per night\n"
        f"Work Schedule: {user_profile_data.get('schedule', '')}\n"
        f"Dietary Preferences: {user_profile_data.get('diet', '')}"
    )

    # Run our existing agent logic
    memory = Memory()
    decision_maker = DecisionMaker(memory)
    wellness_plan = asyncio.run(decision_maker.run(user_profile))

    if wellness_plan:
        return jsonify(wellness_plan.dict())
    else:
        return jsonify({'error': 'Failed to generate wellness plan'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
