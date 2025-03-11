# gemini_chatbot.py
import os
import json
import glob
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from google.api_core import retry
from .config import JSON_DIRECTORY, PDF_DIRECTORY, MARKDOWN_DIRECTORY

class MultisourceGeminiChatbot:
    def __init__(self, api_key=None):
        # Use API key from environment variable if not provided
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        os.environ["GOOGLE_API_KEY"] = self.api_key
        
        # Initialize chat histories and embeddings
        self.chat_histories = {}
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Create a unified knowledge base
        self.unified_qa = None
        self.document_sources = {}  # Track document sources for reference
        
        # Load all content sources into unified knowledge base
        self.initialize_knowledge_base()
    
    def initialize_knowledge_base(self):
        """Load all content sources and initialize a unified knowledge base."""
        try:
            # Collect documents from all sources
            all_documents = []
            
            # 1. Load PDFs
            pdf_documents = self._load_pdf_documents()
            all_documents.extend(pdf_documents)
            
            # 2. Load Web-scraped JSON content
            json_documents = self._load_json_documents()
            all_documents.extend(json_documents)
            
            # 3. Load Markdown content 
            # markdown_documents = self._load_markdown_documents()
            # all_documents.extend(markdown_documents)
            
            if not all_documents:
                print("No documents loaded in knowledge base")
                return
                
            # Create unified vector store
            print(f"Creating unified knowledge base with {len(all_documents)} documents")
            self._create_unified_qa(all_documents)
            
        except Exception as e:
            print(f"Error initializing knowledge base: {e}")
    
    def _load_pdf_documents(self):
        """Load all PDF documents in the PDF directory."""
        documents = []
        
        try:
            # Find all PDFs in the PDF directory
            pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith('.pdf')]
            
            for pdf_file in pdf_files:
                pdf_path = os.path.join(PDF_DIRECTORY, pdf_file)
                source_id = f"pdf:{pdf_file}"
                
                print(f"Loading PDF: {pdf_path}")
                try:
                    # Load and split the PDF
                    loader = PyPDFLoader(pdf_path)
                    pdf_docs = loader.load()
                    
                    # Track the source
                    for doc in pdf_docs:
                        doc.metadata['source_type'] = 'pdf'
                        doc.metadata['filename'] = pdf_file
                        doc.metadata['source_id'] = source_id
                    
                    documents.extend(pdf_docs)
                    self.document_sources[source_id] = {
                        'type': 'pdf',
                        'filename': pdf_file,
                        'path': pdf_path,
                        'count': len(pdf_docs)
                    }
                except Exception as e:
                    print(f"Error loading PDF {pdf_file}: {e}")
        except Exception as e:
            print(f"Error scanning PDF directory: {e}")
        
        return documents
    
    def _load_json_documents(self):
        """Load web-scraped content from JSON files."""
        documents = []
        
        try:
            # Find all JSON files in the JSON directory
            json_files = [f for f in os.listdir(JSON_DIRECTORY) if f.endswith('.json')]
            
            for json_file in json_files:
                json_path = os.path.join(JSON_DIRECTORY, json_file)
                source_id = f"json:{json_file}"
                
                print(f"Loading scraped content: {json_path}")
                try:
                    # Load JSON content
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert JSON content to documents
                    json_docs = []
                    
                    # Process title
                    if 'title' in data:
                        doc = Document(
                            page_content=f"Title: {data['title']}",
                            metadata={
                                'source_type': 'web_scraped',
                                'filename': json_file,
                                'content_type': 'title',
                                'url': data.get('url', 'unknown'),
                                'source_id': source_id
                            }
                        )
                        json_docs.append(doc)
                    
                    # Process content items
                    for item in data.get('content', []):
                        item_type = item.get('type', 'text')
                        text = item.get('text', '')
                        if text.strip():
                            doc = Document(
                                page_content=text,
                                metadata={
                                    'source_type': 'web_scraped',
                                    'filename': json_file,
                                    'content_type': item_type,
                                    'url': data.get('url', 'unknown'),
                                    'source_id': source_id
                                }
                            )
                            json_docs.append(doc)
                    
                    documents.extend(json_docs)
                    self.document_sources[source_id] = {
                        'type': 'web_scraped',
                        'filename': json_file,
                        'url': data.get('url', 'unknown'),
                        'title': data.get('title', 'Untitled'),
                        'count': len(json_docs)
                    }
                except Exception as e:
                    print(f"Error loading JSON {json_file}: {e}")
        except Exception as e:
            print(f"Error scanning JSON directory: {e}")
        
        return documents
    
    # def _load_markdown_documents(self):
    #     """Load content from Markdown files."""
    #     documents = []
        
    #     try:
    #         # Find all Markdown files in the Markdown directory
    #         md_files = [f for f in os.listdir(MARKDOWN_DIRECTORY) if f.endswith('.md')]
            
    #         for md_file in md_files:
    #             md_path = os.path.join(MARKDOWN_DIRECTORY, md_file)
    #             source_id = f"markdown:{md_file}"
                
    #             print(f"Loading Markdown: {md_path}")
    #             try:
    #                 # Load and process Markdown content
    #                 with open(md_path, 'r', encoding='utf-8') as f:
    #                     content = f.read()
                    
    #                 # Split content into sections based on headers
    #                 sections = []
    #                 current_section = ""
    #                 current_title = "Introduction"
                    
    #                 for line in content.split('\n'):
    #                     if line.startswith('#'):
    #                         # Save previous section if it exists
    #                         if current_section.strip():
    #                             sections.append((current_title, current_section))
    #                         # Start new section
    #                         current_title = line.lstrip('#').strip()
    #                         current_section = ""
    #                     else:
    #                         current_section += line + "\n"
                    
    #                 # Add the final section
    #                 if current_section.strip():
    #                     sections.append((current_title, current_section))
                    
    #                 # Create documents from sections
    #                 for title, content in sections:
    #                     doc = Document(
    #                         page_content=f"{title}:\n{content}",
    #                         metadata={
    #                             'source_type': 'markdown',
    #                             'filename': md_file,
    #                             'section': title,
    #                             'source_id': source_id
    #                         }
    #                     )
    #                     documents.append(doc)
                    
    #                 self.document_sources[source_id] = {
    #                     'type': 'markdown',
    #                     'filename': md_file,
    #                     'count': len(sections)
    #                 }
    #             except Exception as e:
    #                 print(f"Error loading Markdown {md_file}: {e}")
    #     except Exception as e:
    #         print(f"Error scanning Markdown directory: {e}")
        
    #     return documents
    
    def _create_unified_qa(self, documents, chunk_size=1000, chunk_overlap=150, k=4):
        """Create a unified QA chain from all documents."""
        try:
            if not documents:
                print("No documents provided for QA chain")
                return
            
            # Split the documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )
            docs = text_splitter.split_documents(documents)
            
            print(f"Created {len(docs)} chunks from {len(documents)} documents")
            
            # Create vector database
            db = DocArrayInMemorySearch.from_documents(docs, self.embeddings)
            
            # Create retriever
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
            
            # Create unified QA chain
            self.unified_qa = ConversationalRetrievalChain.from_llm(
                llm=ChatGoogleGenerativeAI(
                    model="models/gemini-1.5-pro",
                    temperature=0.2,
                    convert_system_message_to_human=True,
                    # safety_settings={
                    #     "HARASSMENT": "block_none",
                    #     "HATE_SPEECH": "block_none",
                    #     "SEXUAL": "block_none",
                    #     "DANGEROUS": "block_none",
                    # }
                ),
                chain_type="stuff",  # Use 'stuff' to combine all relevant documents
                retriever=retriever,
                return_source_documents=True,
                return_generated_question=True,
                verbose=False,
            )
            
            # Initialize global chat history
            self.chat_histories['unified'] = []
            
            print("Unified QA system created successfully")
            
        except Exception as e:
            print(f"Error creating unified QA chain: {e}")
            raise
    
    def refresh_knowledge_base(self):
        """Refresh the knowledge base with any new documents."""
        # Reset and reinitialize
        self.document_sources = {}
        self.initialize_knowledge_base()
        return self.get_stats()
    
    def get_stats(self):
        """Get statistics about the knowledge base."""
        stats = {
            'document_count': len(self.document_sources),
            'document_types': {
                'pdf': len([d for d in self.document_sources.values() if d['type'] == 'pdf']),
                'web_scraped': len([d for d in self.document_sources.values() if d['type'] == 'web_scraped']),
                'markdown': len([d for d in self.document_sources.values() if d['type'] == 'markdown']),
            },
            'documents': list(self.document_sources.values())
        }
        return stats
    
    def get_chat_response(self, message, session_id='unified'):
        """Get response from the chatbot using the unified knowledge base."""
        try:
            if not self.unified_qa:
                return {
                    "answer": "I don't have any knowledge base loaded yet. Please add some documents first.",
                    "sources": []
                }
            
            # Ensure chat history exists for this session
            if session_id not in self.chat_histories:
                self.chat_histories[session_id] = []
            
            chat_history = self.chat_histories[session_id]
            
            # Create a system prompt that encourages citation of sources
            system_prompt = """
            You are a helpful assistant that answers questions based on multiple knowledge sources including PDFs, 
            web-scraped content, and markdown documents. Your goal is to provide accurate, factual responses using
            only the information in these sources.

            Always include citations to your sources when providing information, mentioning the type of document
            and its title or URL where applicable. If you're not sure about something or if the information is not
            present in your knowledge base, admit that you don't know rather than making something up.
            
            If multiple sources contain relevant information, try to synthesize a complete answer that draws from all of them.
            """
            
            # Run the query
            result = self.unified_qa({
                "question": message,
                "chat_history": chat_history,
                "system_prompt": system_prompt
            })
            
            # Extract source information for attribution
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_type = doc.metadata.get('source_type', 'unknown')
                    
                    if source_type == 'pdf':
                        sources.append({
                            'type': 'pdf',
                            'filename': doc.metadata.get('filename', 'unknown'),
                            'page': doc.metadata.get('page', 0),
                            'content': doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                        })
                    elif source_type == 'web_scraped':
                        sources.append({
                            'type': 'web_scraped',
                            'url': doc.metadata.get('url', 'unknown'),
                            'content_type': doc.metadata.get('content_type', 'text'),
                            'content': doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                        })
                    elif source_type == 'markdown':
                        sources.append({
                            'type': 'markdown',
                            'filename': doc.metadata.get('filename', 'unknown'),
                            'section': doc.metadata.get('section', 'unknown'),
                            'content': doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                        })
            
            # Update chat history
            chat_history.append((message, result["answer"]))
            self.chat_histories[session_id] = chat_history
            
            return {
                "answer": result["answer"],
                "sources": sources,
                "generated_question": result.get("generated_question", "")
            }
            
        except Exception as e:
            print(f"Error getting chat response: {e}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": []
            }