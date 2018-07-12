links = []
yea = False

@bot.message_handler(commands=['links'])
def link(message):
    ans = str(len(links)) + ' links\n'
    for i in range(len(links)):
        if isinstance(links[i], list):
            ans += str(i) + '- ' + links[i][0] + '\n'
        else:
            ans += str(i) + '- ' + links[i] + '\n'
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['links_add'])
def addition(message):
    try:
        ans = 'Adicionado com sucesso!'
        msg = message.text.replace('\links_add', '')
        if msg == '':
            ans = 'Aguardando arquivo...'
            yea = True
        else:
            links.append(msg)
    except Exception as e:
        ans = 'Erro, tente novamente'
    bot.send_message(message.chat.id, ans)


@bot.message_handler(content_types= 'document')
def arquivo(message):
    if yea:
        links.append([str(message.Document.file_name) + ' Disponivel para download, use o comando com o devido indice para baixar.', message.Document.file_id])
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
