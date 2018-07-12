import telebot
from telebot import types
import datetime

bot = telebot.TeleBot('token')
avisos = []
enquete = []
results = []
links = []
yea = False
@bot.message_handler(commands=['list', 'help'])
def funções(message):
    mens = long_string = ''' ---FUNÇÕES---
/list. ou /help. : lista todos os comandos disponíveis
/add_news. : adiciona um elemento ao quadro de avisos 
/clear_board. : apaga todo o conteúdo do quadro de avisos 
/erase_news. : remove uma notícia pelo índice no quadro de avisos 
/board. : mostra o quadro de avisos 
/enq_new. : cria uma enquete 
/enq_add. : adiciona uma opção à enquete 
/enq_show. : mostra o andamento da enquete 
/enq_vote. : adiciona um voto à opção na enquete 
/enq_end. : finaliza a enquete 
/links_add. : adiciona um link a lista de links 
/links. : mostra todos os links adicionados a lista de links 
/links_download. : apresenta o conteudo para download de um arquivo pelo indice da lista de links '''
    bot.send_message(message.chat.id,mens)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Iniciando projeto Skynet")


@bot.message_handler(commands=['add_news'])
def send_welcome(message):
    text = message.text.replace('/add_news', '')
    d = datetime.datetime.fromtimestamp(message.date).strftime('%d/%m/%Y, %Hh%Mmin')
    if text != '':
        avisos.append('[%s]: %s'%(d, text))

@bot.message_handler(commands=['clear_board'])
def limpar(message):
    del avisos[:]
    bot.send_message(message.chat.id, 'Quadro esvaziado')


@bot.message_handler(commands=['erase_news'])
def remover(message):
    n = message.text.replace('/erase_news', '')
    try:
        idx = int(n)
        if idx < len(avisos) and idx>=0:
            avisos.pop(idx)
            bot.send_message(message.chat.id, 'Aviso %d removido.' % idx)
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
            ans = ans + ('%d.%s\n' %(i, avisos[i]))
        bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enq_new'])
def create(message):
    msg = message.text.replace('/enq_new', '')
    if len(enquete) != 0:
        ans = 'Encerre a enquete atual para criar uma nova'
    elif msg == '':
        ans = 'Insira o nome da enquete apos o comando e tente novamente.'
    else:
        enquete.append(msg)
        ans = 'Enquete criada com sucesso!'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enq_add'])
def opcao(message):
    msg = message.text.replace('/enq_add', '')
    if msg != '':
        ans = entries(message, msg)
    else:
        ans = 'Insira uma opção valida.'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enq_show'])
def show(message):
    showEnquete(message)

@bot.message_handler(commands=['enq_vote'])
def vote(message):
    try:
        temp = message.text.split()[1]
        votar(message, temp)
    except Exception as e:
        bot.send_message(message.chat.id, 'Erro, tente novamente')

@bot.message_handler(commands=['enq_end'])
def ending(message):
    encerrar(message)

def entries(message, s):
    if len(enquete) == 0:
        ans = 'Sem enquete criada'
    else:
        enquete.append(s)
        ans = 'Adicionado com sucesso!'
        results.append(0)
    return ans

def votar(message, idx):
    ans = ''
    try:
        idx = int(idx)
        if idx < len(results):
            results[idx] += 1
            ans = ('Voto na opção %d adicionado com sucesso' % idx)
        else:
            ans = 'Opção invalida'
    except ValueError:
        ans = 'Opção invalida'
    bot.send_message(message.chat.id, ans)

def encerrar(message):
    if len(enquete) == 0:
        ans = 'Sem enquete ativa.'
    else:
        ans = '--- ' + enquete[0] + ' ---\n'
        ans += opcoes()
        ans += '-- RESULTADO FINAL -- \n'
        ans += resultado()
        del results[:]
        del enquete[:]
    bot.send_message(message.chat.id, ans)



def resultado():
    ans = ''
    for i in range(len(results)):
        ans += ('%s: %d votos\n' % (enquete[i + 1], results[i]))
    return ans

def opcoes():
    ans = ''
    for i in range(1, len(enquete)):
        ans += '%d. %s\n' %(i-1,enquete[i])
    return ans


def showEnquete(message):
    if len(enquete) == 0:
        ans = 'Sem enquetes no momento...'
    else:
        ans = '--- ' + enquete[0] + ' ---\n'
        ans += opcoes()
        ans += '\n---Resultado parcial---\n'
        ans += resultado()
    bot.send_message(message.chat.id, ans)

    
@bot.message_handler(commands=['links'])
def link(message):
    ans = '%d Links\n' % len(links)
    for i in range(len(links)):
        if isinstance(links[i], list):
            ans += '%d. %s\n' %(i,links[i][0])
        else:
            ans += '%d. %s\n' %(i,links[i])
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['links_add'])
def addition(message):
    global yea
    try:
        ans = 'Adicionado com sucesso!'
        msg = message.text.replace('/links_add', '')
        if msg == '':
            ans = 'Aguardando arquivo...'
            yea = True
        else:
            links.append(msg)
    except Exception as e:
        ans = 'Erro, tente novamente'
    bot.send_message(message.chat.id, ans)


@bot.message_handler(content_types= ['document'])
def arquivo(message):
    global yea
    if yea:
        links.append([str(message.document.file_name) + ' -Disponivel para download, use o comando com o devido indice para baixar.', message.document.file_id])
        bot.send_message(message.chat.id, 'Adicionado com sucesso!')
        yea = False

@bot.message_handler(commands=['links_download'])
def download(message):
    try:
        idx = message.text.split()[1]
        idx = int(idx)
        if isinstance(links[idx], list):
            bot.send_document(message.chat.id, links[idx][1])
        else:
            bot.send_message(message.chat.id, 'Algo de errado nao deu certo')
    except Exception as e:
        bot.send_message(message.chat.id, 'Algo de errado nao deu certo')
        
@bot.message_handler(commands=['links_clear'])
def limpar(message):
    del links[:]
        
        
        
bot.polling()
