from langchain_community.document_loaders import PyPDFLoader
from rag_with_mongo import Embedding


def main():
    input_file_path = input("Enter File path :")
    file_path = rf"{input_file_path}"
    loader = PyPDFLoader(file_path)
    data = loader.load()
    embedding = Embedding()
    embedding.get_embeddings(data)


if __name__ == "__main__":
    main()
