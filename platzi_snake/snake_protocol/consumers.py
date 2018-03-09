import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("platzi_piton").add(message.reply_channel)


def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("el formato no parece json=%s", message['text'])
        return
    if data:
        reply_channel = message.reply_channel.name
        if data['direccion'] == "W": 
        	direccion(0,-1,reply_channel)
        if data['direccion'] == "S":
        	direccion(0,1,reply_channel)  	
        if data['direccion'] == "A":
        	direccion(-1,0,reply_channel)  	
        if data['direccion'] == "D":
        	direccion(1,0,reply_channel)  	
    return False

def ws_disconnect(message):
    Group("platzi_piton").discard(message.reply_channel)


def direccion(x,y,reply_channel):
    if reply_channel is not None:
		Channel(reply_channel).send({
				"text": json.dumps ({
				"EJE_X": x,
				"EJE_Y": y,
			})
		})

