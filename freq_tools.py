
def contagem(lista,n):
    ''' Faz a chamada '''
    contagem = []
    for a in lista:
        c = lista.count(a)
        contagem.append((a,(round((c/n)*100))))
    #print(contagem)
    #nem precisaria transformar em set
    contagem = list(set(contagem))

    contagemDict = {}
    for c in contagem:
        contagemDict[c[0]] = c[1]

    return contagemDict


def fazer_chamada(chat):
    ''' Função para seperar os trechos do chat por chamada '''
    chat = chat.split('\n')
    indices_inicio = [i for i,x in enumerate(chat) if x == '#inicioChamada' and chat[i-1][:4] == 'Você']
    indices_fim = [i for i, x in enumerate(chat) if x == '#fimChamada' and chat[i-1][:4] == 'Você']

    todos_indices = indices_inicio.copy()
    todos_indices.extend(indices_fim)

    indices = sorted(todos_indices)
    
    trechos = []
    #print(indices_fim, indices_inicio, indices)
    s = 0
    for i in range(len(indices_inicio)):
        try:
            # fazer o condicional de 'Você'
            indices_inicio.sort()
            inicio = indices_inicio[i]
            #print('oi')
            indices_fim.sort()

            if indices_fim[i] < inicio:
                fim = indices_fim[i+1]
            else:
                fim = indices_fim[i]
                            
            #print(inicio,fim)

            mensagens = chat[inicio+1:fim-1]
            s += 1

            mensagens = analisar_chat(mensagens)
            trechos.append(list(set(mensagens)))
        except:
            pass
    
    total_chamadas = len(trechos)

    todos_trechos = []
    for i in trechos:
        todos_trechos.extend(i)

    return todos_trechos, total_chamadas


def analisar_chat(chat):
    ''' Função para achar os nomes dos alunos no chat '''
    nomes = []

    for msg in chat:
        try:
            hora = int(msg[-5:-3])
            minuto = int(msg[-2:])
            
        except:
            hora = str(msg[-5:-3])
            minuto = str(msg[-2:])
        
        if type(hora) == int and type(minuto) == int:
            nomes.append(msg[0:-5])

    return nomes


def participacao(chat):
    ''' Função para calcular a participação de cada aluno na aula '''
    chat = chat.split('\n')
    nomes = analisar_chat(chat)
    filtro = [i for i in nomes if i != 'Você']
    d = contagem(filtro,len(filtro))
    
    return d
