from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
import networkx as nx
from typing import List, Dict, Optional

class KnowledgeGraph:
    def __init__(self):
        self.g = Graph()
        self.nx_graph = nx.DiGraph()
        self.kg_namespace = Namespace('http://dskg.org/ontology/')
        
    def add_concept(self, concept: str, properties: Dict[str, str]) -> None:
        """Add a concept node to the knowledge graph with properties"""
        concept_uri = URIRef(self.kg_namespace[concept])
        self.g.add((concept_uri, RDF.type, RDFS.Class))
        
        for prop, value in properties.items():
            prop_uri = URIRef(self.kg_namespace[prop])
            self.g.add((concept_uri, prop_uri, Literal(value)))
            
        # Add to NetworkX graph for analysis
        self.nx_graph.add_node(concept, **properties)

    def add_relation(self, source: str, relation: str, target: str) -> None:
        """Add a semantic relation between concepts"""
        source_uri = URIRef(self.kg_namespace[source])
        target_uri = URIRef(self.kg_namespace[target])
        relation_uri = URIRef(self.kg_namespace[relation])
        
        self.g.add((source_uri, relation_uri, target_uri))
        self.nx_graph.add_edge(source, target, relation=relation)

    def sparql_query(self, query: str) -> List[Dict]:
        """Execute SPARQL query on the knowledge graph"""
        results = []
        qres = self.g.query(query)
        
        for row in qres:
            result = {}
            for i, var in enumerate(qres.vars):
                result[var] = row[i]
            results.append(result)
            
        return results

    def find_paths(self, source: str, target: str) -> List[List[str]]:
        """Find all paths between two concepts"""
        try:
            paths = list(nx.all_simple_paths(self.nx_graph, source, target))
            return paths
        except nx.NetworkXNoPath:
            return []

    def get_central_concepts(self, limit: int = 10) -> List[str]:
        """Get most central concepts based on eigenvector centrality"""
        centrality = nx.eigenvector_centrality(self.nx_graph)
        sorted_concepts = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, score in sorted_concepts[:limit]]

    def export_graph(self, format: str = 'turtle') -> str:
        """Export the knowledge graph in specified RDF format"""
        return self.g.serialize(format=format)

    def import_graph(self, data: str, format: str = 'turtle') -> None:
        """Import knowledge graph data in specified RDF format"""
        self.g.parse(data=data, format=format)
        
        # Rebuild NetworkX graph
        self.nx_graph.clear()
        for s, p, o in self.g:
            self.nx_graph.add_edge(str(s), str(o), relation=str(p))