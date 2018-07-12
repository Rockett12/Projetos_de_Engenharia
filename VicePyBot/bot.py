import telebot
from telebot import types
import datetime

bot = telebot.TeleBot('Token')
avisos = []
enquete = []
results = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Iniciando projeto Skynet")


@bot.message_handler(commands=['add'])
def send_welcome(message):
    text = message.text.replace('/add', '')
    d = datetime.datetime.fromtimestamp(message.date).strftime('%d/%m/%Y, %Hh%Mmin')
    if text != '':
        avisos.append('[' + d + ']: ' + text)

@bot.message_handler(commands=['list'])
def funções(message):
    bot.send_message(message.chat.id, ' ---FUNÇÕES--- \n /add. : adicionar um elemento ao quadro de avisos \n /limpar. : apaga todo o conteúdo do quadro de avisos \n /remover. : remove uma notícia pelo índice no quadro de avisos \n /board. : mostra o quadro de avisos \n /enquete create. : cria uma enquete \n /enquete add_option. : adiciona uma opção(cadidado) a enquete \n /enquete show. : mostra o andamento da enquete \n /enquete vote. : adiciona um voto ao candidato escolhido \n /enquete end. : finaliza a enquete')

@bot.message_handler(commands=['limpar'])
def limpar(message):
    del avisos[:]
    bot.send_message(message.chat.id, 'Quadro esvaziado')


@bot.message_handler(commands=['remover'])
def remover(message):
    check = True;
    n = message.text.replace('/remover', '')
    try:
        idx = int(n)
        if idx >= len(avisos) or idx<0:
            check = False
        if check:
            avisos.pop(idx)
            bot.send_message(message.chat.id, 'Aviso ' + str(idx) + ' removido.')
        else:
            bot.send_message(message.chat.id, 'Entrada invalida, tente entrar com o numero do aviso correto')
    except ValueError:
        bot.send_message(message.chat.id, 'Entrada invalida, tente entrar com o numero do aviso correto')

@bot.message_handler(commands=['board'])
def news_board(message):
    ans = '--- QUADRO DE NOTICIAS ---\n'
    if len(avisos) == 0:
        bot.send_message(message.chat.id, "Nada novo sob o sol de \'" + message.chat.title + "\'")
    else:
        for i in range(len(avisos)):
            ans = ans + str(i) + '.' + avisos[i] + '\n'
        bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enquete'])
def enq(message):
    select = message.text.split()
    try:
        tipo = select[1]
    except Exception as e:
        bot.send_message(message.chat.id, 'ERROOOU')
        return
    if tipo == 'create':
        try:
            zerotwo = select[2]
            enquete.append(zerotwo)
        except Exception as e:
            bot.send_message(message.chat.id, 'ERROOOU')
    elif tipo == 'add_option':
        try:
            zerotwo = select[2]
            entries(message, zerotwo)
        except Exception as e:
            bot.send_message(message.chat.id, 'ERROOOU')
    elif tipo == 'show':
        showEnquete(message)
    elif tipo == 'vote':
        try:
            zerotwo = select[2]
            votar(message, zerotwo)
        except Exception as e:
            bot.send_message(message.chat.id, 'ERROOOU')
    elif select[1] == 'end':
        encerrar(message)
    else:
        bot.send_message(message.chat.id, 'Comando nao reconhecido, insira um comando valido.')

def entries(message, s):
    if len(enquete) == 0:
        ans = 'Sem enquete criada'
    else:
        enquete.append(s)
        ans = 'Adicionado com sucesso!'
        results.append(0)
    bot.send_message(message.chat.id, ans)

def votar(message, idx):
    ans = ''
    try:
        idx = int(idx)
        if idx < len(results):
            results[idx] += 1
            ans = 'Voto na opção ' + str(idx) + ' adicionado com sucesso'
        else:
            ans = 'Opção invalida'
    except ValueError:
        ans = 'Opção invalida'
    bot.send_message(message.chat.id, ans)

def encerrar(message):
    if len(enquete) == 0:
        ans = 'Sem enquete ativa.'
    else:
        ans = '--- Opções --- \n'
        ans += opcoes()
        ans += '-- RESULTADO FINAL -- \n'
        ans += resultado()
        del results[:]
        del enquete[:]
    bot.send_message(message.chat.id, ans)



def resultado():
    ans = ''
    for i in range(len(results)):
        ans += enquete[i + 1] + '. ' + str(results[i]) + ' votos\n'
    return ans

def opcoes():
    ans = ''
    for i in range(1, len(enquete)):
        ans += str(i) + '.' + enquete[i] + '\n'
    return ans


def showEnquete(message):
    if len(enquete) == 0:
        ans = 'Sem enquetes no momento...'
    else:
        ans = '--- ' + enquete[0] + ' ---\n'
        ans = opcoes()
        ans += '\n---Resultado parcial---\n'
        ans += resultado()
    bot.send_message(message.chat.id, ans)
bot.polling()
