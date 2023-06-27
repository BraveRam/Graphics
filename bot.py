import telebot
from telebot.types import *
from telebot import custom_filters
import pymongo
from pymongo import MongoClient
from telebot import types

client = MongoClient("mongodb+srv://really651:K4vSnRMEsZhqsTqS@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["GraphicsBot"]
collection = db["graphicsbot"]

bot = telebot.TeleBot("6019916299:AAGdNbTE5Zzij4qv105Ll6vkn9IGJ6MqPhM")

ITEMS_PER_PAGE = 1

key = InlineKeyboardMarkup()
a1 = InlineKeyboardButton("My Daddy\'s Projects🏆", callback_data="projects")
a2 = InlineKeyboardButton("Information📃", callback_data="info")
a3 = InlineKeyboardButton("Help🔍", callback_data="help")
a4 = InlineKeyboardButton("Channel🔔", url="t.me/abelgraphics")
a5 = InlineKeyboardButton("Menu🗃", callback_data="menu")
a6 = InlineKeyboardButton("Language🌍", callback_data="lang")
key.add(a1)
key.add(a2, a3)
key.add(a4, a5)
key.add(a6)

def check_sub(message):
	if bot.get_chat_member("@mt_projectz", message.from_user.id).status != 'left':
		return True
	else:
		return False

def create_paged_keyboard(current_page, total_pages):
    image_caption_pairs = list(collection.find({}, {'_id': False, 'photo': True, "caption": True}))
    keyboard = InlineKeyboardMarkup()    
    buttons = []
    if current_page > 0:
        buttons.append(InlineKeyboardButton(text="◀ Back", callback_data=f"back;{current_page}"))    
    progress_text = f"{current_page + 1}/{total_pages}"
    buttons.append(InlineKeyboardButton(text=progress_text, callback_data="pagination_progress"))
    if current_page < total_pages - 1:
        buttons.append(InlineKeyboardButton(text="⏩Next", callback_data=f"next;{current_page}"))
    keyboard.row(*buttons)
    a1 = InlineKeyboardButton("¤HomePage", callback_data="backmenu")
    keyboard.row(a1)
    return keyboard

def get_total_pages(items, items_per_page):
    image_caption_pairs = list(collection.find({}, {'_id': False, 'photo': True, "caption": True}))
    return (len(items) + items_per_page - 1) 

def send_photo_by_id(chat_id, photo_id, caption, keyboard):
    image_caption_pairs = list(collection.find({}, {'_id': False, 'photo': True, "caption": True}))
    bot.send_photo(chat_id, photo_id, caption=caption, reply_markup=keyboard)

join = InlineKeyboardMarkup()
j = InlineKeyboardButton("🔶️Join The Channel🔷️", "t.me/abelgraphics")
join.add(j)

jtext = "⚠️Before using this bot, you need to Join Graphics Channel🔽\n<i>After Joining press /start button🔄</i>"

@bot.callback_query_handler(lambda query: query.data.startswith('mainmenu'))
def handle_cancel_callback(query):
	wm = f"ʜɪ ‹{query.message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:
		bot.send_message(query.message.chat.id, wm, reply_markup=key)

back = InlineKeyboardMarkup()
b = InlineKeyboardButton("⏪Back", callback_data="backmenu")
back.add(b)

@bot.callback_query_handler(lambda query: query.data.startswith('backmenu'))
def handle_cancel_callback(query):
	wm = f"ʜɪ ‹{query.message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
	am = "👋እንኳን ወደ Abel Graphics ቦት በደህና መጡ!\n\nከዚህ ቦት ሆነው ፕሮጀክቶቹን ማየት እና ማስታወቂያዎችን ማስተዋወቅ ይችላሉ::"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:
		user = collection.find_one({"user_id": query.message.chat.id})
		if user["lang"] == "am":
			bot.send_message(query.message.chat.id, am, reply_markup=key)
		else:
			bot.send_message(query.message.chat.id, wm, reply_markup=key)
	

@bot.callback_query_handler(lambda query: query.data.startswith("info"))
def handle_cancel_callback(query):
	info = "✨ᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ\nᴀɴy ɢʀᴀᴩʜɪᴄꜱ ᴡᴏʀᴋ ʟɪᴋᴇ...\n√ʟᴏɢᴏ\n√ʙᴀɴɴᴇʀ\n√ᴩᴏꜱᴛᴇʀ\n√ꜰʟyᴇʀ\n√ʙᴜꜱɪɴᴇꜱꜱ ᴄᴀʀᴅ.... ᴇᴛᴄ\nʙᴇꜱᴛ qᴜᴀʟɪᴛy \nʙy ᴛʜᴇ ʟᴏᴡᴇꜱᴛ ᴩʀɪᴄᴇ ᴩᴏꜱꜱɪʙʟᴇ\n#ᴏʀᴅᴇʀ_ɴᴏᴡ\n\n✆ ᴄᴏɴᴛᴀᴄᴛ ᴜꜱ:@dayofabel\n\n☛ ᴛᴏ ꜱᴇᴇ ᴍᴏʀᴇ:@abelgraphics"
	am = "✨ᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ\nᴀɴy ɢʀᴀᴩʜɪᴄꜱ ᴡᴏʀᴋ ʟɪᴋᴇ...\n√ʟᴏɢᴏ\n√ʙᴀɴɴᴇʀ\n√ᴩᴏꜱᴛᴇʀ\n√ꜰʟyᴇʀ\n√ʙᴜꜱɪɴᴇꜱꜱ ᴄᴀʀᴅ.... ᴇᴛᴄ\nʙᴇꜱᴛ qᴜᴀʟɪᴛy \nበቅናሽ ዋጋ።\n#አሁኑኑ ይዘዙ።\n\n✆ አናግሩን: @dayofabel\n\n☛ @abelgraphics"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:
		user = collection.find_one({"user_id": query.message.chat.id})
		if user["lang"] == "am":
			bot.send_message(query.message.chat.id, am, reply_markup=back)
		else:
			bot.send_message(query.message.chat.id, info, reply_markup=back)
	
@bot.callback_query_handler(lambda query: query.data.startswith("help"))
def handle_cancel_callback(query):
	info = "ᴅᴏ yᴏᴜ ɴᴇᴇᴅ ᴀɴy 🝰 ʜᴇʟᴩ:)\n\nɪꜰ yᴏᴜ ʜᴀᴠᴇ ᴀɴy qᴜᴇꜱᴛɪᴏɴꜱ ᴀʙᴏᴜᴛ ᴍᴇ,yᴏᴜ ᴄᴀɴ ᴄᴏɴᴛᴀᴄᴛ ᴍy ꜰᴀᴛʜᴇʀ: @dayofabel.✘ ɴᴏ ᴀᴅꜱ"
	am = "<b>ጥያቄ ካለዎት @dayofabel ማናገር ይችላሉ።</b>"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:
		user = collection.find_one({"user_id": query.message.chat.id})
		if user["lang"] == "am":
			bot.send_message(query.message.chat.id, am, reply_markup=back, parse_mode ="html")
		else:
			bot.send_message(query.message.chat.id, info, reply_markup=back, parse_mode ="html")	
	
@bot.callback_query_handler(lambda query: query.data.startswith("menu"))
def handle_cancel_callback(query):
	info = "<i>we will present a new menu soon</i>"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:
		user = collection.find_one({"user_id": query.message.chat.id})
		if user["lang"] == "am":
			bot.send_message(query.message.chat.id, "በቅርብ ቀን።", reply_markup=back)
		else:
			bot.send_message(query.message.chat.id, info, reply_markup=back, parse_mode ="html")
	
	
@bot.callback_query_handler(lambda query: query.data.startswith("lang"))
def handle_cancel_callback(query):
	langbtn = InlineKeyboardMarkup()
	am = InlineKeyboardButton("🇪🇹አማርኛ", callback_data="am")
	en = InlineKeyboardButton("🇺🇸English", callback_data="en")
	langbtn.add(am, en)
	info = "<i>Choose your language:)</i>"
	bot.delete_message(query.message.chat.id, query.message.message_id)
	if check_sub(query) == False:
		bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
	else:		
		bot.send_message(query.message.chat.id, info, reply_markup=langbtn, parse_mode ="html")

@bot.callback_query_handler(lambda query: query.data.startswith('projects'))
def handle_cancel_callback(query):
    image_caption_pairs = list(collection.find({}, {'_id': False, 'photo': True, "caption": True}))
    bot.delete_message(query.message.chat.id, query.message.message_id)
    if check_sub(query) == False:
    	return bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode ="html")
    else:
    	pass
    chat_id = query.message.chat.id
    total_pages = get_total_pages(image_caption_pairs, ITEMS_PER_PAGE)
    keyboard = create_paged_keyboard(0, total_pages)
    first_pair = image_caption_pairs[0]
    send_photo_by_id(chat_id, first_pair['photo'], first_pair['caption'], keyboard)

@bot.callback_query_handler(lambda query: query.data.startswith("am") or query.data.startswith("en"))
def change_lang(query):
	bot.delete_message(query.message.chat.id, query.message.message_id)
	am = "👋እንኳን ወደ Abel Graphics ቦት በደህና መጡ!\n\nከዚህ ቦት ሆነው ፕሮጀክቶቹን ማየት እና ማስታወቂያዎችን ማስተዋወቅ ይችላሉ::"
	wm = f"ʜɪ ‹{query.message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
	if query.data == "en":
		collection.update_one({"user_id": query.message.chat.id}, {"$set": {"lang": "en"}})
		bot.send_message(query.message.chat.id, wm, reply_markup=key)
	if query.data == "am":
		collection.update_one({"user_id": query.message.chat.id}, {"$set": {"lang": "am"}})
		bot.send_message(query.message.chat.id, am, reply_markup=key)

@bot.callback_query_handler(lambda query: query.data.startswith("back") or query.data.startswith("next"))
def handle_pagination_callback(query):
    image_caption_pairs = list(collection.find({}, {'_id': False, 'photo': True, "caption": True}))
    if check_sub(query) == False:
        return bot.send_message(query.message.chat.id, jtext, reply_markup=join, parse_mode="html")
    else:
        pass

    current_page = int(query.data.split(";")[1])
    if query.data == "pagination_progress":
        return
    if query.data.startswith("back"):
        current_page -= 1
    else:
        current_page += 1

    total_pages = get_total_pages(image_caption_pairs, ITEMS_PER_PAGE)
    keyboard = create_paged_keyboard(current_page, total_pages)
    current_pair = image_caption_pairs[current_page]
    bot.edit_message_media(
        media=types.InputMediaPhoto(media=current_pair['photo'], caption=current_pair['caption']),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=keyboard
    )


@bot.message_handler(commands =["start"])
def start(message):
	am = "👋እንኳን ወደ Abel Graphics ቦት በደህና መጡ!\n\nከዚህ ቦት ሆነው ፕሮጀክቶቹን ማየት እና ማስታወቂያዎችን ማስተዋወቅ ይችላሉ"
	wm = f"ʜɪ ‹{message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
	if check_sub(message) == False:
		return bot.send_message(message.chat.id, jtext, reply_markup=join, parse_mode="html")
	else:
		pass
	user = collection.find_one({"user_id": message.from_user.id})
	if user:
		if user["lang"] == "am":
			bot.send_message(message.chat.id, am, reply_markup=key)
		else:
			bot.send_message(message.chat.id, wm, reply_markup=key)
	else:
		collection.insert_one({"user_id": message.from_user.id, "lang": "en"})
		bot.send_message(message.chat.id, wm, reply_markup=key)

admin = [1365625365, 5648060254]

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add("❌Cancel")

@bot.message_handler(func = lambda message: True, state="photo")
def get_photo(message):
	if message.text == "❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "MAIN MENU", reply_markup=ReplyKeyboardRemove())
		wm = f"ʜɪ ‹{message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
		bot.send_message(message.chat.id, wm, reply_markup=key)
	else:
		bot.send_message(message.chat.id, "Please Send Photo Or Cancel This Process:)")

@bot.message_handler(content_types=["photo"], state="photo")
def get_photos(message):
	for photo in message.photo:
		photo_id= photo.file_id
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		data["photo"] = photo_id
		bot.set_state(message.from_user.id, "caption", message.chat.id)
		bot.send_message(message.chat.id, "Cool, Now Send A Caption Of Photo:)", reply_markup=cancel)

@bot.message_handler(func = lambda message: True, state="caption")
def get_caption(message):
	if message.text == "❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "MAIN MENU", reply_markup=ReplyKeyboardRemove())
		wm = f"ʜɪ ‹{message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
		bot.send_message(message.chat.id, wm, reply_markup=key)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			photo_id = data["photo"]
			caption = message.text			
			user_data = {"user_id": photo_id, "text": caption}
			collection.update_one({}, {"$push": {"user_data": {"$each": [user_data], "$position": 0}}})
			bot.send_message(message.chat.id, "✅You Graphics has been added to the cart successfully✅")
			bot.send_message(message.chat.id, "MAIN MENU", reply_markup=ReplyKeyboardRemove())
			wm = f"ʜɪ ‹{message.from_user.first_name}›👋,\n\nᴀʙᴇʟ ɢʀᴀᴩʜɪᴄꜱ ʙᴏᴛ ɪ ᴀᴍ ᴄᴏᴏʟ ᴅᴇꜱɪɢɴᴇʀ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴅᴀᴅ\'ꜱ ᴩʀᴏᴊᴇᴄᴛꜱ\' ᴀꜰᴛᴇʀ ᴛʜɪꜱ ᴠɪꜱɪᴛ, ʜᴇ ᴀʟᴡᴀyꜱ ᴀꜱᴋ ᴍᴇ ᴛᴏ ᴩʀᴏᴍᴏᴛᴇ ꜰᴏʀ ᴀᴅᴠᴇʀᴛɪꜱɪɢɴ ʜᴇʀᴇ;)"
			bot.send_message(message.chat.id, wm, reply_markup=key)
		bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=["addphoto"])
def admin_add_photo(message):
	if message.chat.id in admin:
		bot.set_state(message.from_user.id, "photo", message.chat.id)
		bot.send_message(message.chat.id, "Great, Send Me The Photo To Be Added To Cart:)", reply_markup=cancel)
		

bot.add_custom_filter(custom_filters.StateFilter(bot))

print("Success")
bot.infinity_polling()
