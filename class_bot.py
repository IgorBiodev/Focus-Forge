import telebot
import database_manager as bc
import os
from dotenv import load_dotenv
import json

load_dotenv()

class FocusBot:
    def __init__(self):
        chave = os.getenv('TOKEN_TELEGRAM')
        if not chave:
            raise ValueError("ERRO: Chave do Telegram não encontrada no arquivo .env!")

        self.bot = telebot.TeleBot(chave)
        self.sessoes_ativas = {}

    def debug(self, mensagem):
        self.historico = json.dumps(self.sessoes_ativas, indent=4)
        self.bot.reply_to(mensagem, self.historico)
        

    def iniciar(self, mensagem):
        id_usuario = mensagem.chat.id
        texto_original = mensagem.text 
        tema = texto_original.replace('/iniciar','')
        
        if not tema:
            self.bot.reply_to(mensagem, "⚠️ Você precisa dizer o tema! Ex: /iniciar Python")
            return

        id_banco = bc.iniciar_sessao(id_usuario,tema)

        dados_sessao = {
            "id_banco": id_banco,
            "tema": tema
        }
    
        self.sessoes_ativas[id_usuario] = dados_sessao
        
        self.bot.reply_to(mensagem, f"🛡️ Sessão iniciada! Tema: {tema}\n(ID do Banco: {id_banco})")

    def parar(self, mensagem):
        id_usuario = mensagem.chat.id

        if id_usuario not in self.sessoes_ativas:
            self.bot.reply_to(mensagem, "❌ Nenhuma sessão ativa para parar.")
            return

        
        self.id_banco = self.sessoes_ativas[id_usuario]

    
        self.tempo = bc.encerrar_sessao(self.id_banco)

        del self.sessoes_ativas[id_usuario]

        self.bot.reply_to(mensagem, f"🛑 Foco Encerrado!\n⏱ Tempo Total: {self.tempo}")

    def deletar(self, mensagem):
        id_usuario = mensagem.chat.id

        try:
            bc.del_sessao(id_usuario)
            self.bot.reply_to(mensagem,'🗑️ Ultima sessão deletada com sucesso!')
        except Exception as e:
           self.bot.reply_to(mensagem, f'⚠️ Erro a deletar: {e}')


    def ligar(self):
        @self.bot.message_handler(commands=['debug'])
        def handle_debug(msg):
            self.debug(msg)
        @self.bot.message_handler(commands=['iniciar'])
        def handle_iniciar(msg):
            self.iniciar(msg)

        @self.bot.message_handler(commands=['parar'])
        def handle_parar(msg):
            self.parar(msg)

        @self.bot.message_handler(commands=['deletar'])
        def handle_deletar(msg):
            self.deletar(msg)

        print("🤖 FocusBot System ONLINE...")
        self.bot.polling()

if __name__ == "__main__":
    robo = FocusBot()
    robo.ligar()