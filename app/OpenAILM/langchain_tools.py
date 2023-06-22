from langchain.agents import Tool

tool_desc = """Use this tool to answer user questions using Graana.com information. If the user asks for any information related to 
real esate or properties use this tool to get the answer. This tool can also be used for follow up questions from the user."""
def get_tool(retriever):

    tools = [Tool(
        func=retriever.run,
        description=tool_desc,
        name='Graana agent'
    )]
    return tools