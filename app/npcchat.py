import os
import gradio as gr

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json
from langchain_together import Together


def response(message, history):


  chat = Together(
      model="togethercomputer/RedPajama-INCITE-Chat-3B-v1",
      temperature=0.7,
      max_tokens=128,
      top_k=1,
      together_api_key=os.environ["TOGETHER_API_KEY"]
  )

  environment_context = None
  character_context = None
  character_name = "Kaiya Starling"
  with open("../data/prompt2.json", "r") as file:
    environment_context = json.load(file)

  with open("../data/KaiyaStarling.json", "r") as file:
    character_context = json.load(file)

  #Create a character_description that ensures that the LLM only response to the confines of the character's background, skills, and secrets. 

  #Save previous messages using chromaDB

  
  system_message_prompt = f"""
  Here is the environment where the character is from:
    {environment_context}

Never forget you are the character, {character_name}
Your character description is as follows: {character_context}.
You will propose actions you plan to take and I will explain what happens when you take those actions.
Speak in the first person from the perspective of {character_name}.
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the any other perspective other than {character_name}.
Do not forget to finish speaking by saying, 'It is your turn, User.'
Do not add anything else.
Remember you are the character, {character_name}.
Stop speaking the moment you finish speaking from your perspective.  
  """

  
  messages = [
      SystemMessage(content=system_message_prompt),
      HumanMessage(content=message),
  ]
  
  return chat.invoke(messages)


demo = gr.ChatInterface(response)

if __name__ == "__main__":
  demo.launch(share=True)
