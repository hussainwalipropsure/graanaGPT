import openai

import os
from Tools.store_manager.retriever import get_relevant_text 
from Tools.functions.get_properties import get_property_data
from Tools.functions.get_price_estimate import get_price_estimate
from OpenAILM.gpt import GPTLLm

openai.api_key= os.environ['OPENAI_API_KEY']
        
def chat_completion_with_function_execution(conversation:GPTLLm, messages,functions=[None]):
    """This function makes a chatcompletion api call with the option of adding functions"""
    try:
        response = conversation.chat_completion_request(messages, functions)
        
        full_message = response.json()["choices"][0]
        if full_message['finish_reason'] == "function_call":
            return call_function(conversation, messages, full_message)
        else:
            print(f"Function not required, responding to user")
            return response.json()
    except Exception as e:
        print("Unable to generate ChatCompletion request")
        print(f"Exception chat_completion_with_function_execution 28: : {e}")
        return response

def call_function(conversation:GPTLLm,messages, full_message):
    """ Executes function calls using model generated function arguments"""

    # add our function here
    if full_message['message']['function_call']['name']== 'get_relevant_text':    
        query = eval(full_message['message']['function_call']['arguments'])

        try:            
            results = get_relevant_text(query['query'])            
            messages.append(
                {"role": "function", "name": "get_relevant_text", "content": str(results)}
            )
        except Exception as e:
            print(f"Exception: {e}")
              # This following block tries to fix any issues in query generation with a subsequent call

        try:
            response = conversation.chat_completion_request(messages)            
            return response.json()
        except Exception as e:
            print(type(e))
            print(e)
            raise Exception("Function chat request failed")
    elif full_message['message']['function_call']['name']== 'get_property_data':    
        arguments = eval(full_message['message']['function_call']['arguments'])
        
        try:
            results = get_property_data(**arguments)
            messages.append({"role": "function", "name": "get_property_data", "content": str(results)})
            
        except Exception as e:
            print(f"call_function Exception 69 : {e}")
              # This following block tries to fix any issues in query generation with a subsequent call
        
        try:
            html = """ These are few properties found according to your requirements: 
            [html]<body><section class="contsainer" ><div class="slider-wrapper"><div class="slider" style="display:flex row; overflow-x:scroll; scroll-snap-type: x mandatory; scroll-behavior:smooth; box-shadow: 0 1.5rem 3rem -0.75rem hsla(0, 0%, 0%, 0.25); border-radius: 0.5rem;">"""
            i = 0
            for card in results:
                i+=1
                html +=f"""<div class="card" style="flex: 1 0 100%; scroll-snap-align: start; object-fit: cover; width: 100%; padding: 10px;"><img id="slider-{i}" src="{card['image']}" style="max-width: 17rem;"><p class="card-text" style="margin-top: 0.5rem;">Price: {card['price']}</p><a href="{card['link']}" target="_blank" class="btn btn-block btn-primary" style="text-decoration: none; background-color: #007bff; color: #fff; padding: 0.375rem 0.75rem; border-radius: 0.25rem;">{card['customTitle']}</a></div>"""
            
            html+="""</div></div></section></body>[/html]"""
            
            
            response = conversation.chat_completion_request(messages)
            
            response = response.json()
            response["choices"][0]["message"]["content"] = html
            return response
        except Exception as e:
            print(type(e))
            print(e)
            raise Exception("Function chat request failed")
    elif full_message['message']['function_call']['name']== 'get_price_estimate':    
        arguments = eval(full_message['message']['function_call']['arguments'])
        try:
            estimated_price = get_price_estimate(**arguments)
            messages.append({"role": "function", "name": "get_price_estimate", "content": str(estimated_price)})
        except Exception as e:
            print(f"call_function Exception 69 : {e}")
        
        try:
            response = conversation.chat_completion_request(messages)            
            response = response.json()
            return response
        except Exception as e:
            print(type(e))
            print(e)
            raise Exception("Function chat request failed")
    
    else:
        raise Exception("Function does not exist and cannot be called")