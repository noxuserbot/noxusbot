# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


from userbot.events import register
from userbot import CMD_HELP, bot, LOGS, CLEAN_WELCOME, BOTLOG_CHATID
from telethon.events import ChatAction
from userbot.cmdhelp import CmdHelp

@bot.on(ChatAction)
async def welcome_to_chat(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
        from userbot.modules.sql_helper.welcome_sql import update_previous_welcome
    except:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        """user_added=True,
        user_joined=True,
        user_left=False,
        user_kicked=False"""
        if (event.user_joined
                or event.user_added) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_welcome)
                except Exception as e:
                    LOGS.warn(str(e))
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name,
                                                     a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws and cws.reply:
                current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention,
                                                     title=title,
                                                     count=count,
                                                     first=first,
                                                     last=last,
                                                     fullname=fullname,
                                                     username=username,
                                                     userid=userid,
                                                     my_first=my_first,
                                                     my_last=my_last,
                                                     my_fullname=my_fullname,
                                                     my_username=my_username,
                                                     my_mention=my_mention),
                file=file_media)
            update_previous_welcome(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setwelcome(?: |$)(.*)")
async def save_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import add_welcome_setting
    except:
        await event.edit("`SQL d?????? modda ??al??????yor!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#KARSILAMA_NOTU\
            \nGRUP ID: {event.chat_id}\
            \nA??a????daki mesaj sohbet i??in yeni Kar????lama notu olarak kaydedildi, l??tfen silmeyin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Kar????lama notunu kaydetmek i??in BOTLOG_CHATID ayarlanmas?? gerekir.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Kar????lama mesaj?? bu sohbet i??in {} `"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('kaydedildi'))
    else:
        await event.edit(success.format('g??ncellendi'))


@register(outgoing=True, pattern="^.checkwelcome$")
async def show_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
    except:
        await event.edit("`SQL d?????? modda ??al??????yor!`")
        return
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada kay??tl?? kar????lama mesaj?? yok.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`??u anda bu kar????lama notu ile yeni kullan??c??lar?? a????rl??yorum.`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`??u anda bu kar????lama notu ile yeni kullan??c??lar?? a????rl??yorum.`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmwelcome$")
async def del_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import rm_welcome_setting
    except:
        await event.edit("`SQL d?????? modda ??al??????yor!`")
        return
    if rm_welcome_setting(event.chat_id) is True:
        await event.edit("`Kar????lama mesaj?? bu sohbet i??in silindi.`")
    else:
        await event.edit("`Burada kar????lama notu var m?? ?`")


CMD_HELP.update({
    "welcome":
    "\
.setwelcome <kar????lama mesaj??> veya .setwelcome ile bir mesaja cevap verin\
\nKullan??m: Mesaj?? sohbete kar????lama notu olarak kaydeder.\
\n\nKar????lama mesajlar??n?? bi??imlendirmek i??in kullan??labilir de??i??kenler :\
\n`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`\
\n\n.checkwelcome\
\nKullan??m: Sohbette kar????lama notu olup olmad??????n?? kontrol edin.\
\n\n.rmwelcome\
\nKullan??m: Ge??erli sohbet i??in kar????lama notunu siler.\
"
})

CmdHelp('welcome').add_command(
    'setwelcome', '<kar????lama mesaj??>', 'Mesaj?? sohbete kar????lama notu olarak kaydeder.'
).add_command(
    'checkwelcome', None, 'Sohbette kar????lama notu olup olmad??????n?? kontrol edin.'
).add_command(
    'rmwelcome', None, 'Ge??erli sohbet i??in kar????lama notunu siler.'
).add_info(
    'De??i??kenler: `{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`'
).add()