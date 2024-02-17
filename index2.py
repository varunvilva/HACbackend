from flask import Flask, jsonify
import asyncio

app = Flask(__name__)


async def image():
    print("image started")
    await asyncio.sleep(2)
    print("image completed")

async def text():
    print("text started")
    await asyncio.sleep(3)
    print("text completed")

async def audio():
    print("audio started")
    await asyncio.sleep(1)
    print("audio completed")

@app.route("/get")
async def get_data():
    await asyncio.gather(image(), text(), audio())

    return "hello"

if __name__ == "__main__":
    app.run(debug=True)