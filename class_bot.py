import telebot
import database_manager as bc
import os
from dotenv import load_dotenv

load_dotenv()

class FocusBot:
    def __init__(self):
        chave = os.getenv('TOKEN_TELEGRAM')
        if not chave:
            raise ValueError("ERRO: Chave do Telegram não encontrada no arquivo .env!")

        self.bot = telebot.TeleBot(chave)
        self.sessoes_ativas = {}
    pass 

    def iniciar(self, mensagem):
       # COMO ERA NO SCRIPT
        id_usuario = mensagem.chat.id
        texto_original = mensagem.text 
        tema = texto_original.replace('/iniciar','')
        
        if not tema:
            self.bot.reply_to(mensagem, "⚠️ Você precisa dizer o tema! Ex: /iniciar Python")
            return

        id_banco = bc.iniciar_sessao(id_usuario,tema)
    
        self.sessoes_ativas[id_usuario] = id_banco
        
        self.bot.reply_to(mensagem, f"🛡️ Sessão iniciada! Tema: {tema}\n(ID do Banco: {id_banco})")
        pass

    def parar(self, mensagem):
        # DESAFIO 2:
        # Mesma coisa. Copie a lógica do 'parar' antigo e adapte.
        pass

    def deletar(self, mensagem):
        # DESAFIO 3:
        # Copie a lógica do 'deletar' antigo.
        pass

    def ligar(self):
        # Aqui conectamos os comandos
        # Eu vou te ajudar com um exemplo, você faz os outros.
        
        @self.bot.message_handler(commands=['iniciar'])
        def pre_iniciar(msg):
            self.iniciar(msg)
            
        # AGORA É COM VOCÊ:
        # Crie o registro para o comando '/parar' chamando self.parar
        # Crie o registro para o comando '/deletar' chamando self.deletar
        
        print("Bot Online...")
        self.bot.polling()

# Execução
if __name__ == "__main__":
    robo = FocusBot()
    robo.ligar()