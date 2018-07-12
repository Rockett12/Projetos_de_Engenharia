links = []

@bot.message_handler(commands=['links'])
def link(message):
    ans = str(len(links)) + 'links\n'
    for i in range(len(links)):
        if isinstance(links[i], str):
            ans += str(i) + '- ' + links[i] + '\n'
        else:
            ans += str(i) + '- ' + links[i][0] + '\n'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['links_add'])
def addition(message):
    if message.Document != None:
        links.append([message.Document.file_name + ' - Disponivel para download, acione o comando com indice para baixar.', message.Document.file_id])
    else:
        msg = message.text.replace('/links_add', '')
        links.append(msg.text)

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
