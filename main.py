import json
import os

import gradio as gr
from openai import OpenAI

import example
import asyncio
from utils.read import read_json
from tools.personality import read_personality
from tools.names import generate_names

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI"), )


async def character_generation(prompt, examples, name):

  # Add a prompt for the model to generate a new example
  prompt += "Create a new character profile that fits in this environment with the following personality " + str(
      read_personality) + " and this name " + name

  print(prompt)

  chat_completion = client.chat.completions.create(
      response_format={"type": "json_object"},
      messages=[{
          "role":
          "system",
          "content":
          "You are a creative team designing NPC characters based upon a given environment prompt and output in a json format",
      }, {
          "role": "user",
          "content": prompt
      }],
      model="gpt-3.5-turbo-0125",
  )
  chat = ""
  character = dict()
  if chat_completion.choices[0].message.content is not None:
    temp = json.loads(chat_completion.choices[0].message.content)
    character["name"] = temp["name"]
    character["age"] = temp["age"]
    character["gender"] = temp["gender"]
    character["personalities"] = temp["personalities"]
    character["appearance"] = temp["appearance"]
    character["background"] = temp["background"]
    chat = str(character)

  # generated_image = client.images.generate(
  #   model="dall-e-2",
  #   prompt=chat,
  #   n=1,
  #   size="1024x1024"
  # )

  print(type(chat_completion.choices[0].message.content))
  print(chat_completion)
  final = chat_completion.choices[0].message.content
  # return [chat_completion.choices[0].message.content, generated_image.data[0].url]
  return "" if final is None else final


async def instruction(file_obj, amount):
  amount = int(amount)
  data = read_json(file_obj)
  environment_context = (f"Era: {data['era']}, "
                         f"Time Period: {data['time_period']}, "
                         f"Detail: {data['detail']}\n\n")
  examples = example.examples

  prompt = environment_context + "\n\n".join([e["example"]
                                              for e in examples]) + "\n\n"

  tasks = set()

  names = generate_names(file_obj, amount)
  for x in range(amount):

    task = asyncio.create_task(character_generation(prompt, examples, names[x]))
    tasks.add(task)


  await asyncio.gather(*tasks)

  results = [task.result() for task in tasks]
  print(results)
  
  with open('output.json', 'a') as outfile:
    json.dump(results, outfile, indent=4)

  return results[0]


# Create Gradio Interface
demo = gr.Interface(fn=instruction,
                    inputs=[
                        "file",
                        gr.Slider(1,
                                  20,
                                  value=4,
                                  label="Count",
                                  info="Choose between 1 and 20")
                    ],
                    outputs=["json"],
                    title="JSON File Reader",
                    description="Upload a JSON file and see its contents.")

demo.launch(share=True)
