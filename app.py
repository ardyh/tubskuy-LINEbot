# mybot/app.py
import os
import datetime
from decouple import config
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)


    return 'OK'

try:
    templen = len(arr)
except:
    arr = [] 

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):   
    
    instr = event.message.text
    ins = instr.split(' ')

    if((ins[0] == 'push') & (len(ins) >= 3)):
        dltemp = ins[1].split('/')
    
        try:
            if(len(dltemp) == 3):
                dl = datetime.datetime(int(dltemp[0]), int(dltemp[1]), int(dltemp[2]))
            elif(len(dltemp) == 4):
                dl = datetime.datetime(int(dltemp[0]), int(dltemp[1]), int(dltemp[2]), int(dltemp[3]))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='wah salah deadline bang')
            )

        strtitle = ''

        for idx in range (2, len(ins)):
            if(idx == 2):
                strtitle += ins[idx]

            else:
                strtitle = strtitle + ' ' + ins[idx]

        try:
            arr.append({'deadline':dl, 'title':strtitle})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='done gan')
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='wah gabisa')
            )

    elif(instr == 'tubskuy show'):
        strout = ''
        nows = datetime.datetime.now()

        for idx, el in enumerate(arr):
            strout += str(idx+1) + '. ' + el['title'] + '\n'
            strout += '   ' + 'deadline: ' + str(el['deadline']) + '\n'
            strout += '   Sisa waktu: ' + str(el['deadline'] - nows) + '\n'
        
        try:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=strout)
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Alhamdulillah gabut gan')
            )

    elif((ins[0] == 'remove') & (len(ins) == 2)):
        try:
            temp = arr.pop(int(ins[1])-1)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='done gan')
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='salah ngapus gan')
            )

    """ else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='salah command')
        ) """


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)