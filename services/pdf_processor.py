import os
import json
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
from config.database import get_db_connection

class PDFProcessor:
    def __init__(self):
        # Initialize sentence transformer for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 1000  # Characters per chunk
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def chunk_text(self, text):
        """Split text into manageable chunks"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1
            
            if current_length >= self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def generate_embeddings(self, chunks):
        """Generate embeddings for text chunks"""
        embeddings = self.model.encode(chunks)
        return embeddings
    
    def process_pdf(self, pdf_path, course_id):
        """Process PDF and store embeddings in database"""
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text:
                print("No text extracted from PDF")
                return False
            
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)
            
            # Get course and department info
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT department_id FROM courses WHERE id = %s', (course_id,))
            course_info = cursor.fetchone()
            
            if not course_info:
                cursor.close()
                conn.close()
                return False
            
            department_id = course_info['department_id']
            
            # Get material ID
            filename = os.path.basename(pdf_path)
            cursor.execute('SELECT id FROM materials WHERE file_path = %s', (filename,))
            material = cursor.fetchone()
            
            if not material:
                cursor.close()
                conn.close()
                return False
            
            material_id = material['id']
            
            # Store embeddings in database
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                embedding_json = json.dumps(embedding.tolist())
                cursor.execute(
                    '''INSERT INTO pdf_embeddings 
                       (material_id, course_id, department_id, chunk_text, chunk_index, embedding_vector) 
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (material_id, course_id, department_id, chunk, idx, embedding_json)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✓ Processed PDF: {filename} - {len(chunks)} chunks created")
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False
    
    def search_similar_chunks(self, query, department_id=None, top_k=5):
        """Search for similar text chunks based on query"""
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])[0]
            
            # Get all embeddings from database
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if department_id:
                cursor.execute(
                    'SELECT * FROM pdf_embeddings WHERE department_id = %s',
                    (department_id,)
                )
            else:
                cursor.execute('SELECT * FROM pdf_embeddings')
            
            embeddings_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if not embeddings_data:
                return []
            
            # Calculate similarities
            similarities = []
            for data in embeddings_data:
                stored_embedding = np.array(json.loads(data['embedding_vector']))
                similarity = np.dot(query_embedding, stored_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
                )
                similarities.append({
                    'chunk_text': data['chunk_text'],
                    'similarity': float(similarity),
                    'material_id': data['material_id'],
                    'course_id': data['course_id']
                })
            
            # Sort by similarity and return top k
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            print(f"Error searching similar chunks: {e}")
            return []
