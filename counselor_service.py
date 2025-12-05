from flask import Flask, request, jsonify
from flask_cors import CORS
from edsl import QuestionFreeText, AgentList, Agent
import os

app = Flask(__name__)
CORS(app)

# Expected Parrot API key must be set via environment variable
expected_parrot_key = os.getenv('EXPECTED_PARROT_API_KEY')
if not expected_parrot_key:
    raise ValueError("EXPECTED_PARROT_API_KEY environment variable is required")
os.environ['EXPECTED_PARROT_API_KEY'] = expected_parrot_key

# Internal API key for authentication
INTERNAL_API_KEY = os.getenv('INTERNAL_API_KEY')

def check_api_key():
    """Validate the API key from request headers"""
    if not INTERNAL_API_KEY:
        return None
    
    provided_key = request.headers.get('X-API-Key')
    if provided_key != INTERNAL_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/ask-counselors', methods=['POST'])
def ask_counselors():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.json
        question_text = data.get('question')
        
        if not question_text:
            return jsonify({"error": "No question provided"}), 400
        
        if len(question_text) > 50000:
            return jsonify({"error": "Question too long (max 50000 characters)"}), 400

        # Create your question
        q = QuestionFreeText(
            question_name="advice",
            question_text=question_text
        )

        # Create 3 guidance counselor agents with unique perspectives
        agents = AgentList([
            Agent(traits={
                "persona": f"You are guidance counselor #{i+1}. Counselor 1 focuses on academic planning and college preparation. Counselor 2 emphasizes career development and long-term goals. Counselor 3 prioritizes student wellbeing and personal growth."
            }) 
            for i in range(3)
        ])

        # Run the survey
        results = q.by(agents).run()

        # Extract results
        results_list = results.to_dicts()
        responses = []
        
        for i, result in enumerate(results_list):
            counselor_num = i + 1
            advice = result.get('answer.advice', result.get('advice', 'No response provided.'))
            persona = result.get('agent.persona', result.get('persona', f'Counselor #{counselor_num}'))
            responses.append({
                'counselor': counselor_num,
                'persona': persona,
                'advice': advice
            })

        # Format combined response
        combined_advice = "Here's advice from three guidance counselors:\n\n"
        for resp in responses:
            combined_advice += f"**Counselor #{resp['counselor']}:**\n{resp['advice']}\n\n"

        return jsonify({
            "advice": combined_advice,
            "individual_responses": responses
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred processing your request"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)