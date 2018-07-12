enquete = []
results = []

@bot.message_handler(commands=['enquete_criar'])
def create(message):
    msg = message.txt.replace('/enquete_criar', '')
    if len(enquete) != 0:
        ans = 'Encerre a enquete atual para criar uma nova'
    elif msg == '':
        ans = 'Insira o nome da enquete apos o comando e tente novamente.'
    else:
        enquete.append(msg)
        ans = 'Enquete criada com sucesso!'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enquete_add_option'])
def opcao(message):
    msg = message.text.replace('/enquete_add_option', '')
    if msg != '':
        ans = entries(message, msg)
    else:
        ans = 'Insira uma opção valida.'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['enquete_show'])
def show(message):
    showEnquete(message)

@bot.message_handler(commands=['enquete_votar'])
def vote(message):
    try:
        temp = message.text.split()[1]
        votar(message, temp)
    except Exception as e:
        bot.send_message(message.chat.id, 'Erro, tente novamente')

@bot.message_handler(commands=['enquete_end'])
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
