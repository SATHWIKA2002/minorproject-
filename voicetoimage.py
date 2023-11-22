# -*- coding: utf-8 -*-
"""voicetoimage.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jE4DXYDT6CQoaOvz0BIILwRdBhT5Oz8P
"""



#!pip install gradio==3.39.0
#!pip install openai==0.27.2
#!pip install ffmeg-python==0.2.0

import gradio as gr
import openai
import os
import warnings
warnings.filterwarnings("ignore")
openai.api_key = "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"
def chatgpt_api(input_text):
    messages = [
    {"role": "system", "content": "You are a helpful assistant."}]

    if input_text:
        messages.append(
            {"role": "user", "content": 'Summarize this text "{}" into a short and concise Dall-e2 prompt'.format(input_text)},
        )

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion.choices[0].message.content
    return reply
def dall_e_api(dalle_prompt):
    dalle_response = openai.Image.create(
            prompt = dalle_prompt,
            size="512x512"
        )
    image_url = dalle_response['data'][0]['url']
    return image_url
def whisper_transcribe(audio):
    os.rename(audio, audio + '.wav')
    audio_file = open(audio + '.wav', "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    dalle_prompt = chatgpt_api(transcript["text"])
    image_url = dall_e_api(dalle_prompt)
    return transcript["text"], image_url
output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Image(label="DALL-E Image")
speech_interface = gr.Interface(
    fn=whisper_transcribe,
    inputs=gr.Audio(source="microphone",type="filepath"),
    outputs=[output_1, output_2],
    title="Generate Images using Voice"
)
speech_interface.launch(debug=True)

