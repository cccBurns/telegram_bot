import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7062461662:AAFEPwoFMdrWcIMEQtWlgvuvkwvBlCaY20k"
USUARIO = "@burns_ccc_bot"

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola Wacho!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Necesitas ayuda gato?")

async def personalizado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Esto es un comando personalizado")

def respuesta(texto):
    texto = texto.lower()
    if "hola" in texto:
        return "Hola Wachin!"
    elif "chau" in texto:
        return "Chau gato!"
    elif "perro" in texto:
        return "Si me encantan los perros, con papas y al horno"
    elif "dólar blue" in texto or "dolar blue" in texto:
        return obtener_precio_dolar_blue()
    else:
        return "No entiendo que me queres decir, me estas descansado?"

def obtener_precio_dolar_blue():
    try:
        response = requests.get("https://api.bluelytics.com.ar/v2/latest")
        if response.status_code == 200:
            data = response.json()
            dolar_blue = data['blue']['value_sell']
            return f"Pero que Cheto que estas!, ya te lo digo...el precio del dólar blue es ${dolar_blue:.2f} ARS."
        else:
            return "No pude obtener el valor del dólar blue en este momento."
    except Exception as e:
        return f"Hubo un error al obtener el valor del dólar blue: {str(e)}"

async def mensajes_entrantes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tipo = update.message.chat.type
    texto = update.message.text

    if tipo == "group":
        if USUARIO in texto:
            texto_nuevo = texto.replace(USUARIO, "").strip()
            response = respuesta(texto_nuevo)
        else:
            return
    else:
        response = respuesta(texto)

    await update.message.reply_text(response)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    # Comandos
    app.add_handler(CommandHandler("start", inicio))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("personalizado", personalizado))

    # Respuestas
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mensajes_entrantes))

    # Actualización del bot
    app.run_polling(poll_interval=2)