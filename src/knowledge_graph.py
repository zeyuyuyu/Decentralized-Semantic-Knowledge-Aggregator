import numpy as np
from scipy.spatial.distance import cosine

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_embeddings = {}

    def add_node(self, node_id, node_data):
        self.nodes[node_id] = node_data
        self.node_embeddings[node_id] = self.generate_node_embedding(node_data)

    def add_edge(self, node1_id, node2_id, edge_data):
        if node1_id not in self.edges:
            self.edges[node1_id] = {}
        self.edges[node1_id][node2_id] = edge_data

    def generate_node_embedding(self, node_data):
        # Implement your node embedding logic here
        # This could involve techniques like word2vec, BERT, or custom embeddings
        return np.random.rand(100)

    def search_similar_nodes(self, query_node_id, top_k=5):
        query_embedding = self.node_embeddings[query_node_id]
        similarity_scores = {}
        for node_id, embedding in self.node_embeddings.items():
            if node_id != query_node_id:
                similarity_score = 1 - cosine(query_embedding, embedding)
                similarity_scores[node_id] = similarity_score
        
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        return [node_id for node_id, _ in sorted_scores[:top_k]]
