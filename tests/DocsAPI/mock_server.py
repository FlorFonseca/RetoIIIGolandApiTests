"""
Mock Server para API de Documentos
Archivo: mock_server.py
"""

from unittest.mock import Mock
from datetime import datetime


class MockDocsAPI:
    """Mock server que simula tu API de documentos"""
    
    def __init__(self):
        # Documentos existentes en el mock
        self.docs = {
            "123e4567-e89b-12d3-a456-426614174000": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "documento_ejemplo.pdf",
                "minio_path": "docs/123e4567-e89b-12d3-a456-426614174000.pdf",
                "uploaded_at": "2024-12-16T10:30:00"
            }
        }
        self.counter = 0
    
    def get(self, url, **kwargs):
        """Simula requests.get"""
        response = Mock()
        
        # GET /get_single_doc/{id}
        if "/get_single_doc/" in url:
            doc_id = url.split("/get_single_doc/")[1]
            
            # Validar formato UUID
            if not self._is_valid_uuid_format(doc_id):
                response.status_code = 400
                response.json.return_value = {"detail": "Invalid ID format"}
                return response
            
            # Buscar documento
            if doc_id in self.docs:
                response.status_code = 200
                response.json.return_value = self.docs[doc_id]
            else:
                response.status_code = 404
                response.json.return_value = {"detail": "Document not found"}
        
        # GET /get_docs
        elif "/get_docs" in url:
            response.status_code = 200
            response.json.return_value = {
                "results": list(self.docs.values()),
                "total": len(self.docs)
            }
        
        # GET /get/{id}/doc
        elif "/get/" in url and "/doc" in url:
            doc_id = url.split("/get/")[1].split("/")[0]
            
            if doc_id in self.docs:
                response.status_code = 200
                response.content = b"%PDF-1.4\n%Mock PDF content"
                response.headers = {'Content-Type': 'application/pdf'}
            else:
                response.status_code = 404
                response.json.return_value = {"detail": "Document not found"}
        
        else:
            response.status_code = 404
            response.json.return_value = {"detail": "Endpoint not found"}
        
        return response
    
    def post(self, url, **kwargs):
        """Simula requests.post"""
        response = Mock()
        
        if "/create_doc" in url:
            data = kwargs.get('data', {})
            files = kwargs.get('files', {})
            
            # Validar que tenga archivo
            if not files or 'content' not in files:
                response.status_code = 422
                response.json.return_value = {"detail": "Missing file"}
                return response
            
            # Validar que tenga filename
            if not data or 'filename' not in data:
                response.status_code = 422
                response.json.return_value = {"detail": "Missing filename"}
                return response
            
            # Validar tipo de archivo
            file_tuple = files['content']
            if len(file_tuple) >= 3:
                content_type = file_tuple[2]
                if content_type != "application/pdf":
                    response.status_code = 415
                    response.json.return_value = {"detail": "Invalid file type"}
                    return response
            
            # Crear documento exitosamente
            self.counter += 1
            new_id = f"new-doc-{self.counter:04d}-0000-0000-000000000000"
            filename = data['filename']
            
            new_doc = {
                "id": new_id,
                "filename": filename,
                "minio_path": f"docs/{new_id}.pdf",
                "uploaded_at": datetime.now().isoformat(),
                "result": True
            }
            
            self.docs[new_id] = new_doc
            response.status_code = 200
            response.json.return_value = new_doc
        else:
            response.status_code = 404
            response.json.return_value = {"detail": "Endpoint not found"}
        
        return response
    
    def delete(self, url, **kwargs):
        """Simula requests.delete"""
        response = Mock()
        
        if "/delete_doc/" in url:
            doc_id = url.split("/delete_doc/")[1]
            
            if doc_id in self.docs:
                deleted_doc = {**self.docs[doc_id], "result": True}
                del self.docs[doc_id]
                response.status_code = 200
                response.json.return_value = deleted_doc
            else:
                response.status_code = 404
                response.json.return_value = {
                    "id": doc_id,
                    "filename": None,
                    "minio_path": None,
                    "uploaded_at": None,
                    "result": "Error: Document not found"
                }
        else:
            response.status_code = 404
            response.json.return_value = {"detail": "Endpoint not found"}
        
        return response
    
    def _is_valid_uuid_format(self, doc_id):
        """Valida si el string tiene formato UUID"""
        parts = doc_id.split('-')
        if len(parts) != 5:
            return False
        try:
            # Intentar validar que sean hexadecimales
            for part in parts:
                int(part, 16)
            return True
        except ValueError:
            return False