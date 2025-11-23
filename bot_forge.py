import telebot
import database_manager as bc
import os 
from dotenv import load_dotenv

load_dotenv()


chave = os.getenv('token_telegram')
if not chave:
    raise ValueError("ERRO: Chave do Telegram não encontrada no arquivo .env!")

bot = telebot.TeleBot(chave)

sessoes_ativas = {}

bc.criar_tabela()

@bot.message_handler(commands=['iniciar'])
def iniciar(mensagem):
    id_usuario = mensagem.chat.id
    texto_original = mensagem.text 


    tema = texto_original.replace('/iniciar','')

    
    if not tema:
        bot.reply_to(mensagem, "⚠️ Você precisa dizer o tema! Ex: /iniciar Python")
        return

 
    id_banco = bc.iniciar_sessao(id_usuario,tema)

  
    sessoes_ativas[id_usuario] = id_banco
    
    bot.reply_to(mensagem, f"🛡️ Sessão iniciada! Tema: {tema}\n(ID do Banco: {id_banco})")



@bot.message_handler(commands=['parar'])
def parar(mensagem):
    id_usuario = mensagem.chat.id

 
    if id_usuario not in sessoes_ativas:
        bot.reply_to(mensagem, "❌ Nenhuma sessão ativa para parar.")
        return

    
    id_banco = sessoes_ativas[id_usuario]

 
    tempo = bc.encerrar_sessao(id_banco)

    del sessoes_ativas[id_usuario]

    bot.reply_to(mensagem, f"🛑 Foco Encerrado!\n⏱ Tempo Total: {tempo}")


print("--- 🤖 BOT FOCUS FORGE INICIADO ---")
print("Aguardando ordens no Telegram...")


bot.polling()