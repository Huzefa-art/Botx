import os
from dotenv import load_dotenv
from chat_model.config import *
from typing import Dict

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage


def chat_openai(model_name: str) -> ChatOpenAI:
    """
    Creates and returns an LLM object with appropriate error handling.

    Args: model_name (str): Name of the LLM model to create.
    Returns: ChatOpenAI: The created LLM object.
    """
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Missing API key")
    try:
        # create the LLM object
        chat_model = ChatOpenAI(
            model=model_name,
            openai_api_key=OPENAI_API_KEY,
        )
        return chat_model
    except Exception as error:
        if "Invalid API key" in str(error):
            raise ValueError("Invalid API key provided.") from error
        else:

            raise RuntimeError("Unexpected error:", error) from error



def chat_prompt_template(
        variables: Dict[str, str], 
        system_message_template: str) -> ChatPromptTemplate:
    
    """
    Creates a formatted chat prompt template.

    Args:
        variables (Dict[str, str]): Dictionary containing 'name', 'relation', and 'chat'.
        system_message_template (str): The template for the system message.
    Returns: ChatPromptTemplate: A formatted chat prompt template.
    """
    
    try:
        # System Message - Template Text & Variable Dictionary  
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        formatted_system_message = system_message_prompt.prompt.format(**variables)

        # print('\n\n\nFormatted Message\n' ,  formatted_system_message)
        # Create the ChatPromptTemplate
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=formatted_system_message
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        return chat_prompt
    
    except KeyError as error:
        raise print(f"Missing variable in 'variables' dictionary: {error}")
    except Exception as error:
        raise print(f"An error occurred: {error}")
     


def message_to_dict(message):
    if isinstance(message, HumanMessage):
        return {"input": message.content}
    elif isinstance(message, AIMessage):
        return {"output": message.content}
    else:
        return {"type": "Unknown", "content": str(message)}

