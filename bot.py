import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envíame el link de un video de Twitter (X) y te lo descargaré.")

async def descargar_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "twitter.com" not in url and "x.com" not in url:
        await update.message.reply_text("Por favor, envía un enlace válido de Twitter o X.")
        return

    await update.message.reply_text("Descargando el video, por favor espera...")

    opciones = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            informacion = ydl.extract_info(url, download=True)
            nombre_archivo = ydl.prepare_filename(informacion)
        
        await update.message.reply_text("¡Descarga lista! Enviando video...")
        await update.message.reply_video(video=open(nombre_archivo, 'rb'))
        os.remove(nombre_archivo) # Borra el archivo local para no llenar tu disco
    except Exception as e:
        await update.message.reply_text(f"Hubo un error al descargar el video: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('9294668561:AAESN3ZFLASy_MLfZqi7cRzJwmFdz0NL0KY').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar_video))
    
    application.run_polling()