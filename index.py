import asyncio
import time
from flask import Flask

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



# async def main():
#     start_time = time.time()
#     await asyncio.gather(image(), text(), audio())
#     end_time = time.time()
#     print(end_time-start_time)


# if __name__ == '__main__':
#     asyncio.run(main())
    

@app.route("/", methods=['POST'])
async def get_all():
    start_time = time.time()
    await asyncio.gather(image(), text(), audio())
    end_time = time.time()
    print(end_time-start_time)
    return "Hello"  

if __name__ == '__main__':
    app.run(debug=True)