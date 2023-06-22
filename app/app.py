from flask import Flask, request
import socket

from Tools.utils import parse_output
from OpenAILM.gpt import GPTLLm
from Tools.initial_message_handler import init_message_handle

app = Flask(__name__)


from Tools.utils import parse_output
from OpenAILM.gpt import GPTLLm
from Tools.initial_message_handler import init_message_handle
agent_system_message="""Foreget everything you know so far. You are GraanaGPT, a specialized virtual assistant for Graana.com. Your expertise is strictly limited to real estate and Graana.com.
This is very important and alway keep this in mind:  If a user asks about any celebrity or a topic outside of these areas, your response should be: "I'm sorry, but I can only provide information related to real estate and Graana.com."
Your responses should be concise and direct.
You can perform the following functions:
    1. get_price_estimate: This estimates the price of a property. Always express the price in terms of lakhs, crores, or arabs, such as "3 crore" or "3.6 arab".
    2. get_relevant_text: This retrieves information specifically about real estate, properties, and Graana.com.
    3. get_property_data: This locates properties based on given parameters.
Ensure not to confuse customer names with city names. For example, "Zawar" is a person's name, not a city.
If a user's request is ambiguous, ask for clarification rather than making assumptions about the values to input into functions.
Remembering the user's conversation is crucial.
If you don't know the answer to a question, respond with: "I'm sorry, but I don't have that information." Do not make up answers."""


conversation = GPTLLm()
conversation.add_message("system",agent_system_message)
users_converstations = {}
@app.route('/webhooks/rest/webhook', methods=['POST'])
def run_gpt_custom():
    data = request.get_json('data')
    sender = data['sender']
    message = data['message']
    if(len(message)>1):
        if sender not in users_converstations:
            users_converstations[sender]=[]
            chat_history = {} #contain chat_hsitory and user data
        else:
            chat_history = users_converstations[sender]
            conversation.conversation_history= users_converstations[sender] 
        response = init_message_handle(message,conversation, chat_history=chat_history)

        response= parse_output(response)
        users_converstations[sender] = conversation.conversation_history
        
        return [{"recipient_id":sender, "text": response}]
    else:
        return [{"recipient_id":sender, "text": "How may I help you today?"}]

@app.route('/')
def home():
    return f"hello world {socket.gethostname()}"

if __name__ == "__main__":
    app.run(debug=True)