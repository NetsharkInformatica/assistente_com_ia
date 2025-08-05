import speech_recognition as sr
import streamlit as st
from pydub import AudioSegment
import tempfile
import os

def transcreve_audio(file_audio, prompt=None):
    if not file_audio:
        return None

    tmp_file_path = None
    try:
        # Verifica se o arquivo tem conteúdo
        file_audio.seek(0, os.SEEK_END)
        file_size = file_audio.tell()
        file_audio.seek(0)
        
        if file_size == 0:
            return "Arquivo vazio"

        # Cria arquivo temporário
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp_file_path = tmp_file.name
        tmp_file.close()  # Fecha explicitamente o arquivo

        # Converte o áudio
        if file_audio.name.endswith('.mp3'):
            try:
                audio = AudioSegment.from_mp3(file_audio)
                audio.export(tmp_file_path, format="wav")
            except Exception as e:
                return f"Erro ao converter MP3: {str(e)}"
        else:
            with open(tmp_file_path, 'wb') as f:
                f.write(file_audio.read())

        # Processa o áudio
        r = sr.Recognizer()
        with sr.AudioFile(tmp_file_path) as source:
            audio_data = r.record(source)
        
        text = r.recognize_google(audio_data, language='pt-BR')
        return text

    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Erro no serviço: {e}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
    finally:
        # Garante que o arquivo será excluído
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except PermissionError:
                # Se ainda estiver bloqueado, tenta novamente após um delay
                import time
                time.sleep(0.1)
                os.unlink(tmp_file_path)

# Interface do Streamlit
st.title("Transcrição de Áudio")
st.write("Faça upload de um arquivo de áudio (MP3 ou WAV) para transcrever")

arquivo_audio = st.file_uploader("Carregar arquivo de áudio", type=['wav', 'mp3'])

if arquivo_audio is not None:
    st.audio(arquivo_audio)
    
    if st.button("Transcrever Áudio"):
        with st.spinner("Transcrevendo..."):
            resultado = transcreve_audio(arquivo_audio)
        
        if resultado:
            if resultado.startswith(("Erro", "Não foi")):
                st.error(resultado)
            else:
                st.success("Transcrição concluída!")
                st.text_area("Texto transcrito", resultado, height=150)
def main():
    #função principal
    st.header("App Transcript",divider=True)
    st.subheader("Transcreva auios e videos")
    tabs=["Video","Audio"]
    tab_video, tab_audio=st.tabs(tabs)
    with tab_video:
        st.markdown("Teste em video")
    with tab_audio:
        st.markdown("Teste em audio")
        prompt_audio = st.text_input("digite o seu prompt")
        file_audio=st.file_uploader("escolha o seu audio .mp3",type=["mp3","mp4"])
        if file_audio:
            transcricao_audio= transcreve_audio(file_audio,prompt_audio)
            if transcricao_audio:
                st.write(transcricao_audio)
            else:
                st.error("erro ao transcrever o audio")
            
if __name__ == "__main__":
    main() 