from pyrogram import Client
from pyrogram import filters
import os
import threading
import mdisk
import split

bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "") 

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

TG_SPLIT_SIZE = 2097151000

@app.on_message(filters.command(["start"]))
async def echo(client, message):
    await app.send_message(message.chat.id, 'Send me the mdisk link like this >> /mdisk link')

'''async def progress(current, total):
    await app.send_message(message.chat.id,f"{current * 100 / total:.1f}%")'''

async def down(v,a,message,link):
    await app.send_message(message.chat.id, 'downloading')
    file = mdisk.mdow(link,v,a,message)
    size = split.get_path_size(file)
    if(size > 2097151000):
        await app.send_message(message.chat.id, 'spliting')
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        os.remove(file)
        await app.send_message(message.chat.id, 'uploading')
        i = 1
        for ele in flist:
            await app.send_document(message.chat.id,document=ele,caption=f"part {i}")#, progress=progress)
            i = i + 1
            os.remove(ele)
    else:
        await app.send_message(message.chat.id, 'uploading')
        await app.send_document(message.chat.id,document=file)#, progress=progress)
        os.remove(file)


@app.on_message(filters.command(["mdisk"]))
async def echo(client, message):
    try:
        link = message.text.split("mdisk ")[1]
        if "mdisk" in link:
            out = mdisk.req(link)
            await app.send_message(message.chat.id, out)
            await app.send_message(message.chat.id, 'send VideoID,AudioID like this >> 0,1')
            with open(f"{message.chat.id}.txt","w") as ci:
                ci.write(link)
    except:
        await app.send_message(message.chat.id, 'send only mdisk link with command followed by link')

@app.on_message()
async def echo(client, message):
    if os.path.exists(f"{message.chat.id}.txt"):
        with open(f"{message.chat.id}.txt","r") as li:
            link = li.read()
        link = link.split("\n")[0] 
        os.remove(f"{message.chat.id}.txt")
        ids = message.text.split(",")
        d = threading.Thread(target=lambda:down(ids[0],ids[1],message,link),daemon=True)
        d.start()
        #await down(ids[0],ids[1],message,link)
    else:
        await app.send_message(message.chat.id, "first send me link with /mdisk")

app.run()    
