from app.application.interfaces.ai_service import AIService
import os
from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(r"C:\Users\Public\repos\Estudos\Faculdade\projeto_aplicado_3\env")
CAMINHO_DB = os.getenv("CAMINHO_DB")
API_KEY = os.getenv("GEMINI_API_KEY")
PROMPT_TEMPLATE = """
    Responda a pergunta do usuário: {pergunta}

    com base no seguinte contexto: {contexto}

    Sempre que possível, cite fontes oficiais confiáveis (como MEC, CAPES, SBIE, ConBraSD, UNESCO ou legislações brasileiras sobre inclusão educacional).

    Se você não souber a resposta, diga "Desculpe, não sei a resposta para isso."
"""

class GeminiAIService(AIService):
    async def generate_response(self, user_question: str) -> str:
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=API_KEY
            )
            
            db = Chroma(persist_directory=CAMINHO_DB, embedding_function=embeddings)

            resultados = db.similarity_search_with_relevance_scores(user_question, k=3)
            if len(resultados) == 0 or resultados[0][1] < 0.7:
                resposta = "Desculpe, não sei a resposta para isso."
                print(resposta)
                return resposta
            
            textos_resultado = []
            for resultado in resultados:
                texto = resultado[0].page_content
                textos_resultado.append(texto)

            base_conhecimento = "\n\n----\n\n".join(textos_resultado)
            prompt_final = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt_final = prompt_final.invoke({"pergunta": user_question, "contexto": base_conhecimento})

            modelo = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=API_KEY,
                temperature=0.2
            )
            texto_resposta = await modelo.ainvoke(prompt_final)
            resposta = texto_resposta.content
            if any(palavra in user_question.lower() for palavra in ["diagnóstico", "tratamento", "avaliação"]):
                resposta += "\n\n⚠️ Aviso: Esta resposta é apenas informativa e não substitui orientação profissional qualificada."

            return resposta
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."
        
