import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

import os
from openai import OpenAI

_ =load_dotenv(find_dotenv())



def transcreve_audio(file_audio, prompt=None):
    if file_audio:
        transcription = openai.audio.transcriptions.create(  # Usando o client configurado
            model="whisper-1",
            language="pt",
            response_format="text",
            file=file_audio,
            prompt=prompt
        )
        return transcription
    return None


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


# import streamlit as st
# from dotenv import load_dotenv, find_dotenv
# import os
# from transformers import pipeline
# import os
# from transformers import pipeline

# # Carrega variáveis de ambiente (opcional, para chave HF)
# _ = load_dotenv(find_dotenv())

# def transcreve_audio(file_audio, prompt=None):
#     """Transcreve áudio usando o modelo do Hugging Face."""
#     if file_audio:
#         # Salva o arquivo temporariamente (o pipeline do HF precisa de um arquivo em disco)
#         temp_audio_path = "temp_audio.mp3"
#         with open(temp_audio_path, "wb") as f:
#             f.write(file_audio.getbuffer())
        
#         # Carrega o modelo de transcrição (pode demorar na primeira execução)
#         transcriber = pipeline(
#             "automatic-speech-recognition",
#             model="facebook/wav2vec2-large-xlsr-53-portuguese"
#         )
        
#         # Transcreve o áudio
#         transcription = transcriber(temp_audio_path)
        
#         # Remove o arquivo temporário
#         os.remove(temp_audio_path)
        
#         return transcription["text"]
#     return None

# def main():
#     st.header("App Transcript (Hugging Face)", divider=True)
#     st.subheader("Transcreva áudios e vídeos")
    
#     tabs = ["Video", "Audio"]
#     tab_video, tab_audio = st.tabs(tabs)
    
#     with tab_video:
#         st.markdown("Funcionalidade de vídeo ainda não implementada")
    
#     with tab_audio:
#         st.markdown("### Transcrição de Áudio")
#         prompt_audio = st.text_input("Digite um prompt de contexto (opcional):")
#         file_audio = st.file_uploader("Carregue seu arquivo de áudio (.mp3 ou .wav)", type=["mp3", "wav"])
        
#         if file_audio:
#             st.audio(file_audio, format='audio/wav')
#             if st.button("Transcrever Áudio"):
#                 with st.spinner("Transcrevendo..."):
#                     transcricao_audio = transcreve_audio(file_audio, prompt_audio)
                
#                 if transcricao_audio:
#                     st.success("Transcrição concluída!")
#                     st.text_area("Resultado:", transcricao_audio, height=200)
#                 else:
#                     st.error("Erro ao transcrever o áudio.")

# if __name__ == "__main__":
#     main()