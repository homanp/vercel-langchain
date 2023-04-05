from flask import Flask, request, jsonify
import os
import sys
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import DirectoryLoader
import jieba as jb

UPLOAD_FOLDER = "embedding_files"
CUT_FOLDER = "embedding_cut_files"

app = Flask(__name__)
llm = OpenAI(temperature=0.9)

@app.route("/")
def home():
  text = "你好呀"
  return "<h2>Flask Vercel" + llm(text) + "</h2>"

@app.route("/users", methods=["GET"])
def get_all_users():
    return "123"

@app.route("/api/embedding_completions/<int:id>", methods=["GET"])
def get_embedding_completions():
    try:
        identifier = request.args.get('id')
        question = request.args.get('question')
        embedding = OpenAIEmbeddings()
        cut_dir = os.path.join(CUT_FOLDER, identifier)
        vectordb = Chroma(persist_directory=cut_dir, embedding_function=embedding)
        chain = ChatVectorDBChain.from_llm(OpenAI(temperature=0, model_name="gpt-3.5-turbo"), vectordb, return_source_documents=True)
        result = chain({"question": question})
        return result["answer"]
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'调用 Embedding : {str(e)}'})

@app.route('/upload_embedding_source', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        file_name = file.filename.lower()
        identifier = request.form.get('id')
        file_path = os.path.join(UPLOAD_FOLDER, identifier, file_name)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        file.save(file_path)
        #对中文文档进行分词处理
        with open(file_path,"r",encoding='utf-8') as f:  
            data = f.read()
        cut_data = " ".join([w for w in list(jb.cut(data))])
        #分词处理后的文档保存到data文件夹中的cut子文件夹中
        cut_file = os.path.join(CUT_FOLDER, identifier, file_name)
        cut_dir = os.path.join(CUT_FOLDER, identifier)
        with open(cut_file, 'w') as f:   
            f.write(cut_data)
            f.close()
        loader = DirectoryLoader(cut_dir,glob='**/*.txt')
        docs = loader.load()
        #文档切块
        text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
        doc_texts = text_splitter.split_documents(docs)
        #调用openai Embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        #向量化
        vectordb = Chroma.from_documents(doc_texts, embeddings, persist_directory=cut_dir)
        vectordb.persist()
        return jsonify({'status': 'success', 'message': '文件上传成功！'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'文件上传失败: {str(e)}'})
  
@app.route('/download_embedding_source', methods=['GET'])
def download_file():
    try:
        identifier = request.args.get('id')
        file_name = request.args.get('file_name')
        file_path = os.path.join(UPLOAD_FOLDER, identifier, file_name)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'文件下载失败: {str(e)}'})

if __name__ == '__main__':
  print('启动啦')
  app.run(host='0.0.0.0', debug=True, port=3000, threaded=True)

# ```
# curl -F 'file=@/path/to/yourfile.txt' -F 'identifier=abc' http://localhost:5000/upload
# ```
