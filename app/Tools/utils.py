def parse_output(response):
    if(isinstance(response, dict)):
        if('answer' in response):
            response = response['answer']
        elif response['role']=='assistant':
            response = response['content']
    return response

