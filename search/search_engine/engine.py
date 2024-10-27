# search/search_engine/engine.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any
import pandas as pd
from django.core.cache import cache
from menuResto.models import Menu
import os
from django.conf import settings

class MenuSearchEngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MenuSearchEngine, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            # Set environment variable to disable symlinks warning
            os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
            
            # Initialize model and index
            self.model = None
            self.index = None
            self.menu_data = None
            
            # Create cache directory if it doesn't exist
            self.cache_dir = os.path.join(settings.BASE_DIR, 'search_cache')
            os.makedirs(self.cache_dir, exist_ok=True)
            
            self._initialize()
            self.initialized = True
    
    def _initialize(self):
        """Initialize or load index from cache"""
        # Try to load cached index and embeddings
        self.index = cache.get('search_index')
        self.menu_data = cache.get('menu_data')
        
        if self.index is None or self.menu_data is None:
            self._build_index()
        
        # Load model only when needed
        if self.model is None:
            self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    def _build_index(self):
        """Build search index from menu data"""
        # Get all menu items
        menus = Menu.objects.all().values('id', 'name', 'description', 'price')
        self.menu_data = pd.DataFrame(menus)
        
        # Initialize model if not already initialized
        if self.model is None:
            self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        # Combine fields for embedding
        texts = self.menu_data.apply(
            lambda x: f"{x['name']} {x['description']}", 
            axis=1
        ).tolist()
        
        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Normalize embeddings
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        
        # Cache the data
        cache.set('search_index', self.index, timeout=3600)  # Cache for 1 hour
        cache.set('menu_data', self.menu_data, timeout=3600)
    
    def search(self, query: str, k: int = 9) -> List[Dict[str, Any]]:
        """Search for menu items"""
        if self.model is None:
            self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
            
        # Generate query embedding
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search in index
        similarities, indices = self.index.search(query_embedding, k)
        
        # Get results
        results = []
        for idx, score in zip(indices[0], similarities[0]):
            menu_item = Menu.objects.get(id=self.menu_data.iloc[idx]['id'])
            results.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'description': menu_item.description,
                'price': menu_item.price,
                'image': menu_item.image,
                'score': float(score)
            })
        
        return results