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
import glob
import PIL.Image






load_dotenv()

app = Flask(__name__)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


GOOGLE_API_KEY=os.getenv('API_KEY')
text_prompt = os.getenv("text_prompt")
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/text', methods=['POST'])
def get_text():
    data = request.get_json()
    query = data['query']
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
    print(text_prompt)
    print(type(query))
    print(str(text_prompt) + query)
    response = model.generate_content(str(text_prompt) + query)
    return response.text

@app.route("/audio",methods=['POST'])
def get_audio():
    data = request.get_json()
    query = data['query']
    bhashini_input = {"modelId":"641c0be440abd176d64c3f92","task":"asr", "audioContent":query, "source":"en", "userId":"null"}
    bhashini_api = "https://meity-auth.ulcacontrib.org/ulca/apis/asr/v1/model/compute"
    response = requests.post(bhashini_api, json=bhashini_input)
    if response.status_code == 200:
        print("Hi")
        return response
    else:
        return "Hello"
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(text_prompt + query)
    # return response.text


@app.route('/image',methods=['POST'])
def get_image():
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
    image_files = glob.glob("*.jpg") + glob.glob("*.jpeg")
    latest_image = max(image_files, key=os.path.getmtime)
    img = PIL.Image.open(latest_image)
    response = model.generate_content([image_prompt,img],stream=True)
    response.resolve()
    return response.text





if __name__ == '__main__':
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    app.run(debug=True, port=3000)