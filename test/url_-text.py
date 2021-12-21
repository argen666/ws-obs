import obspython as obs
import urllib.request
import urllib.error
import pytchat
import time
import json
import urllib
import os
import datetime

url         = ""
interval    = 5
source_name = ""
jd="Nothung yet, wait for 1st message to come..."
msgcnt=0
bNeedRestart=0
NoMore=0

starttime=datetime.datetime.now()

# ------------------------------------------------------------
chat = pytchat.create(video_id="-5KAN9_CzSA")

def update_text():
#	global url
	global interval
	global source_name
	global chat
	global jd
	global bNeedRestart
	global msgcnt	
	
#	cwd = os.getcwd()
#	obs.script_log(obs.LOG_WARNING,cwd)
    
	if bNeedRestart:
		return
	source = obs.obs_get_source_by_name(source_name)
	if source is not None:
		if chat.is_alive():
			chatdata = chat.get()
			for c in chatdata.sync_items():
				jd=chatdata.json()
				jd1=json.loads(jd)
				jd2=jd1[0]['author']['imageUrl']
				try:f=urllib.request.urlopen(jd2)
				except urllib.error.URLError as e:
					obs.script_log(obs.LOG_WARNING,e.reason)
					return
				fil=f.read()
				f.close()
#				f2=open("/home/vr/work/Scripts/img/img.jpg", "wb")
				try:f2=open("C:/img.jpg", "wb")
				except:
					obs.script_log(obs.LOG_WARNING,"Can't open file for write userpic")
					return
				f2.write(fil)
				f2.close()

				settings = obs.obs_data_create()
#				obs.obs_data_set_string(settings, "text", f"{c.datetime} [{c.author.name}]- {c.message}")
				obs.obs_data_set_string(settings, "text", f"[{c.author.name}]- {c.message}")
				obs.obs_source_update(source, settings)
				obs.obs_data_release(settings)
				msgcnt+=1
#				obs.timer_remove(update_text)
				
		else:
			strout="Chat is dead. Please restart script manually. " + str(datetime.datetime.now())
			obs.script_log(obs.LOG_WARNING,strout)
			bNeedRestart=1
#			obs.timer_remove(update_text)
#			chat = pytchat.create(video_id="-5KAN9_CzSA")

		obs.obs_source_release(source)

def refresh_pressed(props, prop):
#	obs.script_log(obs.LOG_WARNING,"Pressed button")
	update_text()
def debuh_pressed(props, prop):
	global jd
	global msgcnt
	cwd = os.getcwd()
	obs.script_log(obs.LOG_WARNING,"Pressed Debugh. Total messages proceed: " + str(msgcnt))
	strout="Startung time: " + str(starttime) + ", cwd:" + str(cwd)
	obs.script_log(obs.LOG_WARNING, strout)	
	obs.script_log(obs.LOG_WARNING,jd)

def draw_pressed(props, prop):
	f0=open("C:/bigdildo.jpg", "rb")
	f1=open("C:/img.jpg", "wb")
	fil0=f0.read()
	f1.write(fil0)
	f1.close()
	f0.close()
# ------------------------------------------------------------

def script_description():
	return "Pops are parasites"

def script_update(settings):
#	global url
	global interval
	global source_name

#	url         = obs.obs_data_get_string(settings, "url")
	interval    = obs.obs_data_get_int(settings, "interval")
	source_name = obs.obs_data_get_string(settings, "source")

	obs.timer_remove(update_text)
	
	

#	if url != "" and source_name != "":
	obs.timer_add(update_text, interval * 1000)

def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "interval", 1)

#def script_tick(sec):
#	global bNeedRestart
#	global NoMore
#	if bNeedRestart:
#		if not NoMore:
#			chat = pytchat.create(video_id="-5KAN9_CzSA")
#			NoMore=1

def script_properties():
	props = obs.obs_properties_create()

#	obs.obs_properties_add_text(props, "url", "URL", obs.OBS_TEXT_DEFAULT)
	obs.obs_properties_add_int(props, "interval", "Update Interval (seconds)", 1, 3600, 1)

	p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)

	obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
	obs.obs_properties_add_button(props, "button2", "Debuh", debuh_pressed)
	obs.obs_properties_add_button(props, "button3", "Draw Dildoh!", draw_pressed)
	return props
