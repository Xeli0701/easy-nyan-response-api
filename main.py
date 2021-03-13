#uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8080

from fastapi import FastAPI
from janome.tokenizer import Tokenizer
import oseti
import urllib.parse

app = FastAPI()

@app.get("/nyan/{message}")
async def getNyanMessage(message):
    t = Tokenizer()
    message_tokens = []
    for token in t.tokenize(message):
        if("終助詞" in token.part_of_speech):
            pass
        else:
            message_tokens.append(token.surface)

    converted_message = "".join(message_tokens) + "にゃ"
    print(converted_message)
    return {"message": converted_message}


@app.get("/posneg/{message2}")
async def getPosNegResponse(message2):
    message = urllib.parse.unquote(message2)
    analyzer = oseti.Analyzer()
    temp = analyzer.analyze(message)
    score = sum(temp) / len(temp)
    print(score)
    
    if (score >= 0.5):
        return {"message": "すばらしいにゃ！"}
    elif (score > -0.5):
        return {"message": "なるほどにゃ"}
    elif (score <= -0.5):
        return {"message": "そうなのかにゃ……"}
    else:
        return {"message": "にゃーん"}