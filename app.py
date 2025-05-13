from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

app = Flask(__name__)
api = Api(app, version='1.0', title='S444 Agent ai',
    description='S4ai ')

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

ns = api.namespace('chat', description='Chat operations')


chat_input = api.model('ChatInput', {
    'message': fields.String(required=True, description='The message to send to Gemini AI')
})

# Define the response model
chat_response = api.model('ChatResponse', {
    'response': fields.String(description='The response from Gemini AI')
})

@ns.route('')
class ChatResource(Resource):
    @ns.expect(chat_input)
    @ns.response(200, 'Success', chat_response)
    @ns.response(400, 'Bad Request')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        try:
            # Get the user's message from the request
            data = request.get_json()
            user_message = data.get('message')
            
            if not user_message:
                return {"error": "Message is required"}, 400

            # Send the message to Gemini API
            response = model.generate_content(user_message)
            bot_response = response.text

            # Return the response as JSON
            return {"response": bot_response}
        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)