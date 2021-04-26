import streamlit as st
from datetime import datetime
import pandas as pd
import base64
from freq_tools import *

st.header('Bem-vindo(a) ao analisador de chats do Meet!')
st.markdown('**Uma forma fácil e rápida de fazer a chamada da sua aula e de contabiblizar a participação de cada aluno.**')
st.markdown("Durante a aula escreva no chat o código *#inicioChamada*, aguarde seus alunos responderem, e então escreva o código *#fimChamada*, e pronto! Todos os alunos que escreverem no chat entre um código e outro terão sua presença contabilizada.")
st.markdown('Ah, e você pode fazer quantas chamadas quiser! Basta escrever os códigos novamente.')
st.markdown('De presente 🎁 nós calculamos também a participação de cada aluno no chat durante toda a aula!')

st.sidebar.title('Como fazemos a chamada')
st.sidebar.markdown('Em aulas com **mais de 1 chamada** nós fazemos a média da presença do aluno. *ex.: Em uma aula com 2 chamadas, um aluno que respondeu somente 1 terá 50% de presença.*')
st.sidebar.title('Como calculamos a participação')
st.sidebar.markdown('Para o **cálculo da participação** consideramos o número de mensagens que o aluno enviou e o número de mensagens total do chat (participação relativa).')
st.sidebar.title('E os códigos?')
st.sidebar.markdown('Por enquanto **não é possível mudar** os códigos de início e fim da chamada, mas logo **teremos essa atualização**!')
#st.sidebar.markdown('Você também pode definir **códigos de inicio e fim personalizados** antes da análise. E não se preocupe, se algum aluno escrever o código no chat, a mensagem é ignorada.')
st.sidebar.title('Entre em contato!')
st.sidebar.markdown('Encontrou um problema? Tem uma sugestão? Fale conosco pelo [Instagram](https://www.instagram.com/lab.tecaap/)!')

st.markdown('👈 Para mais informações consulte a barra lateral.')

st.subheader('Analisador')

chat = st.text_area('Cole aqui o chat do Meet')

if st.button('ANALISAR'):
    import time
    bar = st.progress(0)

    for p in range(100):
        time.sleep(0.002)
        bar.progress(p + 1)

    nomes, chamadas = fazer_chamada(chat)
    #st.write([nomes, chamadas])
    count = contagem(nomes, chamadas)
    #st.write(count)
    part = participacao(chat)
    #st.write(part)
    if chamadas > 1:
        st.success(f'Detectamos {chamadas} chamadas nesta aula! 🎉')
    elif chamadas == 1:
        st.success(f'Detectamos {chamadas} chamada nesta aula! 🎉')
    elif chamadas < 1:
        st.warning('☹️ Não detectamos nenhuma chamada nesta aula!\nPor favor confira os códigos usados e tente novamente!')


    df_part = pd.DataFrame({'Nome':list(part.keys()),
                            'Participação (%)': list(part.values())})
    
    df_part.sort_values(by=['Nome'], inplace=True, ignore_index=True)

    df_chamada = pd.DataFrame({'Nome':list(count.keys()),
                                'Frequência (%)': list(count.values())})

    df_chamada.sort_values(by=['Nome'], inplace=True, ignore_index=True)

    df_final = pd.merge(df_part, df_chamada, on='Nome')

    if chamadas > 0:
        st.table(df_final[['Nome','Frequência (%)','Participação (%)']])

        csv = df_final.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'👉 <a href="data:file/csv;base64,{b64}" download="chamada-{datetime.today().strftime("%d-%m-%Y")}.csv">Download da tabela</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.markdown("_Se o download não iniciar, clique com o botão direito e escolha 'Salvar como...'_")