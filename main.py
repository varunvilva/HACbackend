import asyncio
import aiohttp
from contextlib import nullcontext
import textwrap
from flask import Flask, request
import requests
import google.generativeai as genai
import os, sys
from dotenv import load_dotenv
from IPython.display import display
from IPython.display import Markdown
import textwrap
import glob,io
from PIL import Image
import json

load_dotenv()

app = Flask(__name__)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

dick = {}
GOOGLE_API_KEY=os.getenv('API_KEY')
text_prompt = os.getenv("text_prompt")
genai.configure(api_key=GOOGLE_API_KEY)

# @app.route('/text', methods=['POST'])
async def get_text(query, bool=True):
    model = genai.GenerativeModel('gemini-pro')
    text_prompt = '''I am providing list of JSON attributes
                    product_name [String]
                    description [Text]
                    price [Float]
                    quantity [Float]
                    categories [list of String]
                    net_weight [Float]
                    barcode [String]
                    manufacturer_brand [String]
                    manufacturing_date [String] [DD-MM-YYYY]
                    expiration_date [String]  [DD-MM-YYYY]

                    Find the attributes in user entered prompt below, the attributes not found in the user entered prompt should be filled with null value.
                    The dates should be in the format [DD-MM-YYYY] id found in the user entered prompt
                    THE OUTPUT IS TO BE GIVEN IN JSON FORMAT
                    The user entered prompt is below :

                    '''
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, model.generate_content, str(text_prompt) + query)
    # print(response.text)
    if bool:
        dick["text"] = "{"+response.text.split("{")[1]
    else:
        dick["audio"] = "{"+response.text.split("{")[1]
    


# @app.route("/audio",methods=['POST'])
async def get_audio(audio):
    bhashini_input = {"modelId":"64117455b1463435d2fbaec4","task":"asr", "audioContent":audio, "source":"hi", "userId":None}
    bhashini_api = "https://meity-auth.ulcacontrib.org/ulca/apis/asr/v1/model/compute"
    # response =  requests.post(bhashini_api, json=bhashini_input)
    # if response.status_code == 200:
    #     print("Hi")
    #     print(response.json())
    #     return response
    # else:
    #     return "Hello"
    async with aiohttp.ClientSession() as session:
        async with session.post(bhashini_api, json=bhashini_input) as response:
            if response.status ==  200:
                # print("Hi")
                data = await response.json()
                await asyncio.gather(get_text(data['data']['source'], False))
            else:
                return "Hello"
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(text_prompt + query)
    # return response.text


# @app.route('/image',methods=['POST'])
async def get_image(image):
    image_prompt="""
    I am providing list of JSON attributes
    product_name [String]
    description [Text]
    price [Float]
    quantity [Float]
    categories [list of String]
    net_weight [Float]
    barcode [String]
    manufacturer_brand [String]
    manufacturing_date [String] [DD-MM-YYYY]
    expiration_date [String]  [DD-MM-YYYY]

    Find the attributes using the image given below, the attributes not found in the image should be filled with null value.
    Do not fill quantity of stock as it will not be mentioned in the image.
    Generate the categories and description based on product image
    The dates should be in the format [DD-MM-YYYY] id found in the image
    THE OUTPUT IS TO BE GIVEN IN JSON FORMAT
    The user entered image is below :
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    loop = asyncio.get_event_loop()
    img = await loop.run_in_executor(None, Image.open, io.BytesIO(image))
    response = await loop.run_in_executor(None, model.generate_content, [image_prompt, img])
    response.resolve()
    # print("three")
    # print(response.text)
    dick["image"]="{"+response.text.split("{")[1]
    # to_markdown(response.text)

    
    return response.text

@app.route("/get-result", methods=["POST"])
async def get_result():
    text = request.form.get('text')
    img = request.files.get('image')
    if img is not None:
        img = img.read()
    else:
        dick["image"]={
            "product_name": None,
            "description": None,
            "price": None,
            "quantity": None,
            "categories": None,
            "net_weight": None,
            "barcode": None,
            "manufacturer_brand": None,
            "manufacturing_date": None,
            "expiration_date": None
        }
    print(type(img))
    print(request.files.get("image"))
    audio = request.form.get('audio')

    
    # loop = asyncio.get_event_loop()
    # img = await loop.run_in_executor(None, Image.open, io.BytesIO(image.read()))
    # img = Image.open(img)
    if text!=None and img!=None and audio!=None:
        await asyncio.gather(get_audio(audio), get_text(text),get_image(img))#, get_audio(audio), get_text(text))
    elif text is None and img is not None and audio is not None:
        await asyncio.gather(get_audio(audio),get_image(img))
    elif text is not None and img is None and audio is not None:
        await asyncio.gather(get_audio(audio), get_text(text))
    elif text is not None and img is not None and audio is None:    
        await asyncio.gather(get_text(text),get_image(img))
    elif text is None and img is None and audio is not None:
        await asyncio.gather(get_audio(audio))
    elif text is None and img is not None and audio is None:
        await asyncio.gather(get_image(img))
    elif text is not None and img is None and audio is None:
        await asyncio.gather(get_text(text))
    elif text is None and img is None and audio is None:
        # await asyncio.gather(get_audio(audio), get_text(text),get_image(img))
        return {"message":"Enter some data"}
    else:
        # Handle the case where all three are None
        pass
    
    if text is None and text in dick.keys():
        dick["text"]={
            "product_name": None,
            "description": None,
            "price": None,
            "quantity": None,
            "categories": None,
            "net_weight": None,
            "barcode": None,
            "manufacturer_brand": None,
            "manufacturing_date": None,
            "expiration_date": None
        }
    if audio is None and audio in dick.keys():
        dick["audio"]={
            "product_name": None,
            "description": None,
            "price": None,
            "quantity": None,
            "categories": None,
            "net_weight": None,
            "barcode": None,
            "manufacturer_brand": None,
            "manufacturing_date": None,
            "expiration_date": None
        }

    #combine data
    print("image",dick["image"])
    # print(type(dick["image"]))
    print("text",dick["text"])
    # print(type(dick["text"]))
    print("audio",dick["audio"])
    # print(type(dick["audio"]))
    if img is not None and type(dick["image"])==type("str"):
        dick["image"] = json.loads(dick["image"].split("```")[0])
        
    if  text is not None and type(dick["text"])==type("str"):
        dick["text"] = json.loads(dick["text"].split("```")[0])
        
    if  audio is not None and type(dick["audio"])==type("str"):
        dick["audio"] = json.loads(dick["audio"].split("```")[0])
        
    
    final_json={}
    for key in dick["image"].keys():
        non_null_order = [dick["text"].get(key), dick["audio"].get(key), dick["image"].get(key)]
        non_null_order = [element for element in non_null_order if element is not None]
        final_json[key] = non_null_order[0] if non_null_order else None
    
    return final_json, 200




if __name__ == '__main__':
    app.run(debug=True, port=3000)