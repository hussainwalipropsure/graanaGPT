"""
This is the first place where user message will arrive.
identify intent

"""
from OpenAILM.gpt import GPTLLm
from OpenAILM.handle_functions import chat_completion_with_function_execution
from Tools.functions.function_definitions import functions

llm_ = GPTLLm()
llm = llm_.get_llm()

def init_message_handle(query, conversation:GPTLLm, chat_history=[]):

    conversation.add_message("user",query)
    # The model first prompts the user for the information it needs to use the weather function

    chat_response = chat_completion_with_function_execution(conversation=conversation,
        messages=conversation.conversation_history, functions=functions
    )
    try:
        assistant_message = chat_response["choices"][0]["message"]["content"]

    except Exception as e:
        print(e)
        print(chat_response)
        assistant_message="Welcome to Graana.com!"
  
    return assistant_message
