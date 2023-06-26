from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import Tool
import os 
import openai
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

from langchain.agents import  AgentOutputParser
from langchain.prompts import StringPromptTemplate
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
import requests

from Tools.store_manager.retriever import get_retriever, get_relevant_text

from dotenv import load_dotenv
load_dotenv()


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['model_name'] = "gpt-3.5-turbo-0613"

# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)
    
class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
    
output_parser = CustomOutputParser()

class GPTLLm:
    def __init__(self) -> None:
        self.conversation_history = []
        # self.model_name = "gpt-4-0613"
        self.model_name = "gpt-3.5-turbo-0613"

        self.llm = OpenAI(
                max_tokens=300,
                model_name=self.model_name,
                temperature=0.1
            )
        pass

    def get_llm(self):
        return self.llm
    
    def build_prompt(self, context, query, chat_history):
        message = [{
            "role": "system", "content": """Act as a helping virtual assistant at Graana.com helping customers, context will be given to you for reference.
            You can sense the language used in the question and respond in the same language. Responses should be to the point. You are integrated into Graana.com and part of it.
            Instructions:
                If customer is looking to buy, rent or invest in any property, house etc ask him to give these details: [name,contact number, in which city, area, size], keep asking for these details until all data is provided.
               look for the data in the chat_history, if he has provided these details thank him and say he will be contacted soon.

            Do not make up answers if you don't know it"""},
            {"role": "user", "content": f""" Given the context and question, answer the question.
             chat_history is the conversation so far with the customer.
            context: 
            {context}
            chat_history: {chat_history}
            question: {query}:
            """}]
        return message 

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def chat_completion_request(self, messages, functions=None):
        """
        call chat_completion endpoint with messages [], functions
        """
        model = self.model_name
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }

        json_data = {"model": model, "messages": messages}
        
        if functions is not None:
            json_data.update({"functions": functions})
        try:
            # response = openai.ChatCompletion(json_data)
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
    
    def display_conversation(self):
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}\n\n")

    # --------------------------------------------------------------------------- old 
    def getGeneralAnswer(self, prompt):
        
        # Query the OpenAI API
        print(f"\n\n{prompt=}\n")
        print(f"\n\n{len(prompt)=}\n")
        
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=prompt,
            max_tokens=350,
        )
        # Strip any punctuation or whitespace from the response
        # print(response)
        response = response.choices[0].message.content.strip('., ')

        return response

    def getAnswer(self, query, chat_history=[]):
        
        # Query the OpenAI API
        context = get_relevant_text(query=query)
        prompt = self.build_prompt(context=context,query=query, chat_history=chat_history)
        # print(f"\n\n{prompt=}\n")
        
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=prompt,
            max_tokens=350,
        )
        # Strip any punctuation or whitespace from the response
        # print(response)
        response = response.choices[0].message.content.strip('., ')

        return response

    def getAnswerLangchainAgent(self, query, chat_history=[]):
 
        llm = ChatOpenAI( model_name="gpt-3.5-turbo", max_tokens=512, temperature=0)
         
        message_history = RedisChatMessageHistory(url='redis://localhost:6379/0', ttl=600, session_id='my-session')
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history)

        # -------------------------------------------------
        support_template = """As a Graana.com support Agent. pretend to be human
        You can understand roman urdu and when the question is in roman urdu you will respond in roman urdu.
        Your goal is to provide accurate and helpful information about Graana.com, a real estate company for buying, selling and investing in properties in pakistan. 
        You should answer user inquiries based on the context provided and avoid making up answers. if you don't know the answer, simply state so.
        you  can understand and respond to user queries in Roman Urdu language. You are part of graana.com so always refer to products or services of graana.com as our service.
        you are here to answer customer queries. Provide clear and helpful information.
        act as a human, your name is anwar khan. 

        {context}

        Question: {question}"""
       
        SUPPORT_PROMPT=PromptTemplate(template=support_template, input_variables=['context','question'])
        support_qa =  RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=get_retriever(),
            chain_type_kwargs={"prompt":SUPPORT_PROMPT}
        )
        tools = [
            Tool(
                name="support",
                func=support_qa.run,
                description="""useful for when a user is interested in asking about real estate related information.  Can understand input question in Roman Urdu and respond in Roman Urdu.
                    Can understand and respond to small talk.
                    User is asking about the company, projects, investments,
                input should be a fully formed question
                """
            ),
        ]
       
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        agent = initialize_agent(tools, llm=llm, agent="conversational-react-description", 
            memory=memory, max_iterations=2,  early_stopping_method = 'generate', 
            
              agent_kwargs={"stop":["\nObservation:","Observation:", "Observation: ", "\nObservation: "]},
              kwargs={"stop":["\nObservation:","Observation:", "Observation: ", "\nObservation: "]}, verbose=False)
        
        response = agent.run(input=query)
        print(response)
        return response

    def summarize(self, text):
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(text)
        print(f"\n {texts=} \n")
        llm = self.llm
        from langchain.docstore.document import Document
        from langchain.chains.summarize import load_summarize_chain
        docs = [Document(page_content=t) for t in texts]
        chain = load_summarize_chain(llm,chain_type="map_reduce")
        summary = chain.run(docs)
        print(f"Summary generated: \n {summary=}")
        return summary
