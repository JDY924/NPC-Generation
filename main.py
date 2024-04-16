from app.generation import instruction
import gradio as gr


# Create Gradio Interface
demo = gr.Interface(fn=instruction,
                    inputs=[
                        "file",
                        gr.Slider(1,
                                  20,
                                  value=1,
                                  label="Count",
                                  info="Choose between 1 and 20")
                    ],
                    outputs=["json"],
                    title="JSON File Reader",
                    description="Upload a JSON file and see its contents.")

demo.launch(share=True)
