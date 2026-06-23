import urllib3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8702394861:AAF4VrwF00tP7w9PM7YwMDVamoQK8sZiYKI"

group_settings = {}
user_warnings = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🤖 *بوت إدارة المجموعات*

📌 *الأوامر:*
/help - المساعدة
/rules - القوانين
/id - معرفاتك
/stats - إحصائيات
/setup - لوحة التحكم

🔹 *للأدمن:*
/ban @user - حظر
/unban @user - فك حظر
/warn @user - تحذير
/mute @user - كتم
/unmute @user - فك كتم
/kick @user - طرد
/welcome_on - تفعيل الترحيب
/welcome_off - إيقاف الترحيب
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📖 /start - القائمة الرئيسية\n/rules - القوانين\n/id - معرفاتك")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 1️⃣ احترام الآخرين\n2️⃣ ممنوع السب\n3️⃣ ممنوع الروابط")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 معرفك: `{update.message.from_user.id}`", parse_mode='Markdown')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    member_count = await context.bot.get_chat_member_count(chat.id)
    await update.message.reply_text(f"📊 عدد الأعضاء: {member_count}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /ban @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        members = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in members:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if user_id:
            await context.bot.ban_chat_member(chat.id, user_id)
            await update.message.reply_text(f"✅ تم حظر @{username}!")
        else:
            await update.message.reply_text("❌ لم أجد هذا العضو")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /unban @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        banned = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in banned:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if user_id:
            await context.bot.unban_chat_member(chat.id, user_id)
            await update.message.reply_text(f"✅ تم فك حظر @{username}")
        else:
            await update.message.reply_text("❌ لم أجد هذا العضو")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /warn @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        members = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in members:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if not user_id:
            await update.message.reply_text("❌ لم أجد هذا العضو")
            return
        if user_id not in user_warnings:
            user_warnings[user_id] = 0
        user_warnings[user_id] += 1
        warnings = user_warnings[user_id]
        if warnings >= 3:
            await context.bot.ban_chat_member(chat.id, user_id)
            await update.message.reply_text(f"🚫 تم حظر @{username} بعد 3 تحذيرات!")
            del user_warnings[user_id]
        else:
            await update.message.reply_text(f"⚠️ تحذير {warnings}/3 للعضو @{username}\nعند الوصول لـ 3 تحذيرات سيتم الحظر!")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /mute @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        members = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in members:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if user_id:
            await context.bot.restrict_chat_member(chat.id, user_id, permissions=ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"🔇 تم كتم @{username}")
        else:
            await update.message.reply_text("❌ لم أجد هذا العضو")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /unmute @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        members = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in members:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if user_id:
            await context.bot.restrict_chat_member(chat.id, user_id, permissions=ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"🔊 تم فك كتم @{username}")
        else:
            await update.message.reply_text("❌ لم أجد هذا العضو")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ استخدم: /kick @username")
        return
    username = context.args[0].replace('@', '')
    chat = update.effective_chat
    try:
        members = await context.bot.get_chat_administrators(chat.id)
        user_id = None
        for member in members:
            if member.user.username and member.user.username.lower() == username.lower():
                user_id = member.user.id
                break
        if user_id:
            await context.bot.ban_chat_member(chat.id, user_id)
            await context.bot.unban_chat_member(chat.id, user_id)
            await update.message.reply_text(f"👢 تم طرد @{username}")
        else:
            await update.message.reply_text("❌ لم أجد هذا العضو")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

async def welcome_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_settings[update.effective_chat.id] = {'welcome': True}
    await update.message.reply_text("✅ تم تفعيل الترحيب")

async def welcome_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_settings[update.effective_chat.id] = {'welcome': False}
    await update.message.reply_text("❌ تم إيقاف الترحيب")

async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id != context.bot.id:
                await update.message.reply_text(f"🎉 أهلاً {member.first_name}!")

async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if update.message.text.startswith('/'):
        return
    text = update.message.text.lower()
    bad = ['سب', 'شتم', 'قذف']
    for word in bad:
        if word in text:
            try:
                await update.message.delete()
            except:
                pass
            await update.message.reply_text("⚠️ ممنوع السب!")
            return
    if 'http://' in text or 'https://' in text:
        try:
            await update.message.delete()
        except:
            pass
        await update.message.reply_text("🚫 ممنوع الروابط!")

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔊 تفعيل الترحيب", callback_data='welcome_on')],
        [InlineKeyboardButton("🔇 إيقاف الترحيب", callback_data='welcome_off')],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data='stats')]
    ]
    await update.message.reply_text("⚙️ لوحة التحكم:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'welcome_on':
        group_settings[query.message.chat_id] = {'welcome': True}
        await query.edit_message_text("✅ تم تفعيل الترحيب!")
    elif query.data == 'welcome_off':
        group_settings[query.message.chat_id] = {'welcome': False}
        await query.edit_message_text("❌ تم إيقاف الترحيب!")
    elif query.data == 'stats':
        try:
            chat = query.message.chat
            member_count = await context.bot.get_chat_member_count(chat.id)
            await query.edit_message_text(f"📊 عدد الأعضاء: {member_count}")
        except:
            await query.edit_message_text("❌ حدث خطأ")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("id", get_id))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("ban", ban_user))
app.add_handler(CommandHandler("unban", unban_user))
app.add_handler(CommandHandler("warn", warn_user))
app.add_handler(CommandHandler("mute", mute_user))
app.add_handler(CommandHandler("unmute", unmute_user))
app.add_handler(CommandHandler("kick", kick_user))
app.add_handler(CommandHandler("welcome_on", welcome_on))
app.add_handler(CommandHandler("welcome_off", welcome_off))
app.add_handler(CommandHandler("setup", setup))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

print("✅ البوت يعمل...")
app.run_polling()
