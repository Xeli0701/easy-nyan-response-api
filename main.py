from fastapi import FastAPI
from janome.tokenizer import Tokenizer
import oseti
import urllib.parse

app = FastAPI()

@app.get("/nyan/{message}")
async def getNyanMessage(message):
    #「な」を「にゃ」に変換する
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


@app.get("/posneg/{message}")
async def getPosNegResponse(message):
    message = urllib.parse.unquote(message)
    analyzer = oseti.Analyzer()
    temp = analyzer.analyze(message)
    score = sum(temp) / len(temp)
    print(score)
    
    if (score >= 0.5): #「喜」とかのポジティブ
        return {"message": "すばらしいにゃ！"}
    elif (score > -0.5): #ふつう
        return {"message": "なるほどにゃ"}
    elif (score <= -0.5): #「死」とかのネガティブ
        return {"message": "そうなのかにゃ……"}
    else: #エラー
        return {"message": "にゃーん"}