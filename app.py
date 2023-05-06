from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex,GPTSimpleVectorIndex, PromptHelper, LLMPredictor, ServiceContext
from langchain import OpenAI
import gradio as gr
import sys
import os
os.chdir(r'/app')  # 文件路径
# os.environ["OPENAI_API_KEY"] = 'sk-xxxxxxxxxxxxxxx'
def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTSimpleVectorIndex.from_documents(documents,service_context=service_context)
    index.save_to_disk('index.json')
    return index
def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response
iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="请输入，您想从知识库中获取什么？"),
                     outputs="text",
                     title="AI 本地知识库ChatBot")
index = construct_index("docs")
iface.launch(share=True)
