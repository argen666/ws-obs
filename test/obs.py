import builtins
import threading
from types import ModuleType
import pytchat
import asyncio
import json
import traceback
import time
from pytchat import ChatDataFinished
from pytchat.util import extract_video_id

# class DummyModule(ModuleType):
#     def __getattr__(self, key):
#         return None
#
#     __all__ = []  # support wildcard imports
#
#
# def tryimport(name, globals={}, locals={}, fromlist=[], level=-1):
#     try:
#         return realimport(name, globals, locals, fromlist, level)
#     except ImportError:
#         return DummyModule(name)
#
#
# realimport, builtins.__import__ = builtins.__import__, tryimport

#################################################################
import obspython as obs


def connect_cur_scene():
    source = obs.obs_frontend_get_current_scene()
    sh = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_connect(sh, "item_add", callback)
    obs.obs_source_release(source)


def callback(calldata):
    scene_item = obs.calldata_sceneitem(calldata, "item")
    # scene = obs.calldata_source(cd,"scene") # bad utf symbols
    scene = obs.obs_sceneitem_get_scene(scene_item)
    name = obs.obs_source_get_name
    source = obs.obs_sceneitem_get_source
    scene_source = obs.obs_scene_get_source
    scene_name = name(scene_source(scene))
    scene_item_name = name(source(scene_item))
    print(f"item {scene_item_name} has been added to scene {scene_name}")
    # obs.script_log(obs.LOG_WARNING, f"item {scene_item_name} has been added to scene {scene_name}")


def on_load(event):
    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        start_chat_stream(None, None)


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_load)


def script_unload():
    obs.timer_remove(timer_tick)


def script_defaults(settings):
    # obs.obs_data_set_default_int(settings, "interval", 1)
    return


def script_update(settings):
    global streamUrl
    if 'streamUrl' in globals() and streamUrl is not None and streamUrl != obs.obs_data_get_string(settings,
                                                                                                   "_stream_url"):
        stopWorkerThread()
    streamUrl = obs.obs_data_get_string(settings, "_stream_url")
    print("Stream URL saved: " + str(streamUrl))


def timer_tick():
    global worker
    global isWorkerStarted
    if isWorkerStarted:
        if not worker.is_alive():
            isWorkerStarted = False
            obs.script_log(obs.LOG_WARNING, "Worker is dead, restarting...")
            worker = threading.Thread(target=collect_chat_data, args=())
            worker.start()
            isWorkerStarted = True


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "_stream_url", "Stream URL:", obs.OBS_TEXT_DEFAULT)
    # obs.obs_properties_add_int(props, "interval", "Update Interval (seconds)", 1, 3600, 1)

    # p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    # sources = obs.obs_enum_sources()
    # if sources is not None:
    # 	for source in sources:
    # 		source_id = obs.obs_source_get_unversioned_id(source)
    # 		if source_id == "text_gdiplus" or source_id == "text_ft2_source":
    # 			name = obs.obs_source_get_name(source)
    # 			obs.obs_property_list_add_string(p, name, name)

    # 	obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "_start_button", "Start", start_chat_stream)
    obs.obs_properties_add_button(props, "_stop_button", "Stop", stop_chat_stream)
    obs.obs_properties_add_button(props, "_draw_scene_items_button", "Draw scene items!", draw_scene_items)
    return props


def collect_chat_data():
    global streamUrl
    global isWorkerStarted
    print(str(streamUrl))
    if streamUrl and isYoutubeVideoIdValid(streamUrl):
        print("Chat data started: " + str(streamUrl))
        livechat = pytchat.create(video_id=streamUrl, interruptable=False)
        isWorkerStarted = True
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=-5KAN9_CzSA", interruptable=False)
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=IgE-DV-9z7E", interruptable=False)
        # livechat = pytchat.create(video_id="https://www.youtube.com/watch?v=ThbXM1-Wfyw", interruptable=False)
        while livechat.is_alive():
            # time.sleep(5)
            if not isWorkerStarted:
                print('Received stop flag, terminating')
                livechat.terminate()
                return
            chatdata = livechat.get()
            for c in chatdata.sync_items():
                jsondata = json.loads(c.json())
                # print(c.json())
                obs.script_log(obs.LOG_WARNING, jsondata['author']['name'] + ": " + jsondata['message'])
                # time.sleep(1)
                draw_scene_items(None, None, jsondata['message'])
        try:
            livechat.raise_for_status()
        except ChatDataFinished:
            print("Chat data finished")
            livechat.terminate()
        except Exception as e:
            print("Chat data exception")
            livechat.terminate()
            # print(traceback.format_exc())
            print(type(e), str(e))
    else:
        obs.script_log(obs.LOG_WARNING,
                       "Stream URL is empty or not valid. Please check the Stream URL in the script settings")


def start_chat_stream(props, prop):
    # worker = threading.Thread(target=collect_chat_data, args=())
    global worker
    if prop is not None:
        # start_btn_property = obs.obs_properties_get(props, "_start_button")
        prop_name = obs.obs_property_name(prop)
        # print(str(prop_name))
        if prop_name == "_start_button":
            if not worker.is_alive():
                worker = threading.Thread(target=collect_chat_data, args=())

    if not worker.is_alive():
        worker.start()
        obs.timer_add(timer_tick, 1000)
    else:
        print("Worker already started")

    # todo restart thread if ends
    # collect_chat_data()
    # while (True):
    #     try:
    #         loop = asyncio.get_event_loop()
    #         # task = loop.create_task(collect_chat_data())
    #         loop.run_until_complete(collect_chat_data())
    #         # loop.run_forever()
    #         print("123")
    #         print("123")
    #         print("123")
    #         print("123")
    #     except Exception as ex:
    #         print("Main exception")
    #         print(type(ex), str(ex))
    #         print(traceback.format_exc())


# if __name__ == '__main__':
#     while (True):
#         try:
#             loop = asyncio.get_event_loop()
#             # task = loop.create_task(main())
#             loop.run_until_complete(start())
#             # loop.run_forever()
#             print("123")
#             print("123")
#             print("123")
#             print("123")
#         except Exception as ex:
#             print("Main exception")
#             print(type(ex), str(ex))
#             print(traceback.format_exc())

def stop_chat_stream(props, prop):
    stopWorkerThread()


def isYoutubeVideoIdValid(id):
    try:
        vid = extract_video_id(streamUrl)
        # r = requests.get(f'https://img.youtube.com/vi/{id}/mqdefault.jpg')
        # return r.status_code == 200
        return True
    except Exception as ex:
        print(type(ex), str(ex))
        return False


def draw_scene_items(props, prop, messageText="Default"):
    # todo CRASHES???
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)

    # obs.obs_data_set_string(settings, "url", "<html> <head> <title>Example</title> </head> <body> <p>This is an example of a simple HTML page with one paragraph.</p> </body> </html>")
    # add group
    # group = obs.obs_source_create_private("group", "Youtube Chat", obs.obs_data_create())
    # obs.obs_scene_add(scene, group)

    # add text
    text_source = obs.obs_get_source_by_name("message")
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", messageText)
    if text_source is None:
        text_source = obs.obs_source_create("text_gdiplus", "message", settings, None)
        # obs.obs_scene_add(scene, text_source)
        # group = obs.obs_scene_insert_group(scene,"Youtube Chat",text_source,1)
        # text_item = obs.obs_scene_sceneitem_from_source(scene, text_source)
        # group = obs.obs_sceneitem_group_add_item(scene, text_item)

        obs.obs_scene_add(scene, text_source)
    else:
        obs.obs_source_update(text_source, settings)

    # group = obs.obs_scene_insert_group(scene, "Youtube Chat", None, 0)
    # scene_item = obs.obs_scene_find_source(scene, "message")
    # obs.obs_sceneitem_group_add_item(group, scene_item)

    # obs.obs_source_release(group)
    obs.obs_data_release(settings)
    obs.obs_scene_release(scene)
    # obs.source_list_release(obs.obs_frontend_get_scenes())


def get_scene_context(scene_name):
    scenes_list = obs.obs_frontend_get_scenes()
    return_scene = None
    for scene in scenes_list:
        name = obs.obs_source_get_name(scene)
        if name == scene_name:
            return_scene = obs.obs_scene_from_source(scene)

    return return_scene, scenes_list


def stopWorkerThread():
    global isWorkerStarted
    isWorkerStarted = False
    # print("Stop worker...")


isWorkerStarted = False
worker = threading.Thread(target=collect_chat_data, args=())
