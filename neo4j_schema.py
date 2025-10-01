from neo4j import GraphDatabase
import os
from typing import Dict, Any

class SimpleSchemaExtractor:
    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.username = os.getenv('NEO4J_USERNAME', 'neo4j') 
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.schema_cache = None
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            print("✅ Neo4j schema connection established")
        except Exception as e:
            print(f"❌ Neo4j connection failed: {str(e)}")
            self.driver = None
    
    def get_schema_context(self) -> str:
        """Get complete schema as string context using node properties"""
        if self.schema_cache:
            return self.schema_cache
            
        if not self.driver:
            return "Neo4j schema not available - using basic personal information only."
        
        try:
            with self.driver.session() as session:
                schema_parts = ["=== MAYANK'S KNOWLEDGE GRAPH SCHEMA ===\n"]
                
                # Get all nodes with their name and description properties
                nodes_query = """
                MATCH (n)
                WHERE n.name IS NOT NULL
                RETURN n.name as name, n.description as description, 
                       properties(n) as properties, id(n) as node_id
                ORDER BY n.name
                LIMIT 50
                """
                
                nodes = list(session.run(nodes_query))
                
                # Group nodes by type if available, otherwise list all
                schema_parts.append("ENTITIES IN KNOWLEDGE GRAPH:")
                
                for node in nodes:
                    name = node['name']
                    description = node['description'] if node['description'] else "No description"
                    props = node['properties']
                    
                    # Get node type from properties or infer from name
                    node_type = props.get('type', self._infer_type_from_properties(props))
                    
                    schema_parts.append(f"\n• {name} ({node_type})")
                    schema_parts.append(f"  Description: {description}")
                    
                    # List other relevant properties
                    other_props = {k: v for k, v in props.items() 
                                 if k not in ['name', 'description', 'type'] and v}
                    if other_props:
                        prop_summary = ", ".join([f"{k}: {v}" for k, v in list(other_props.items())[:3]])
                        schema_parts.append(f"  Properties: {prop_summary}")
                
                # Get relationship patterns using node names
                schema_parts.append("\nRELATIONSHIP PATTERNS:")
                relationships_query = """
                MATCH (a)-[r]->(b) 
                WHERE a.name IS NOT NULL AND b.name IS NOT NULL
                RETURN a.name as from_name, type(r) as rel_type, b.name as to_name,
                       r.description as rel_description, count(*) as frequency
                ORDER BY frequency DESC 
                LIMIT 15
                """
                
                relationships = list(session.run(relationships_query))
                for rel in relationships:
                    rel_desc = f" ({rel['rel_description']})" if rel['rel_description'] else ""
                    schema_parts.append(f"• {rel['from_name']} -[{rel['rel_type']}]{rel_desc}-> {rel['to_name']}")
                
                # Get summary statistics
                stats_query = """
                MATCH (n) WHERE n.name IS NOT NULL
                WITH n.type as node_type, count(n) as count
                WHERE node_type IS NOT NULL
                RETURN node_type, count
                ORDER BY count DESC
                """
                
                stats = list(session.run(stats_query))
                if stats:
                    schema_parts.append("\nENTITY TYPE SUMMARY:")
                    for stat in stats:
                        schema_parts.append(f"• {stat['node_type']}: {stat['count']} entities")
                
                self.schema_cache = "\n".join(schema_parts)
                return self.schema_cache
                
        except Exception as e:
            error_context = f"Schema extraction error: {str(e)}. Using basic personal information only."
            print(f"❌ {error_context}")
            return error_context
    
    def _infer_type_from_properties(self, properties: Dict[str, Any]) -> str:
        """Infer entity type from properties when type field is not available"""
        if not properties:
            return "Unknown"
        
        # Check for explicit type property
        if 'type' in properties:
            return properties['type']
        
        # Infer from property patterns
        if 'level' in properties or 'proficiency' in properties:
            return "Skill"
        elif 'company' in properties or 'role' in properties:
            return "Experience"
        elif 'start_date' in properties and 'end_date' in properties:
            return "Project"
        elif 'email' in properties or 'phone' in properties:
            return "Person"
        elif 'industry' in properties or 'size' in properties:
            return "Company"
        elif 'degree' in properties or 'university' in properties:
            return "Education"
        else:
            return "Entity"
    
    def get_entity_by_name(self, entity_name: str) -> Dict[str, Any]:
        """Get specific entity details by name"""
        if not self.driver:
            return {}
        
        try:
            with self.driver.session() as session:
                query = """
                MATCH (n {name: $name})
                OPTIONAL MATCH (n)-[r]-(related)
                RETURN n.name as name, n.description as description,
                       properties(n) as properties,
                       collect(DISTINCT {
                           name: related.name, 
                           relationship: type(r),
                           description: related.description
                       }) as connections
                """
                
                result = session.run(query, name=entity_name)
                record = result.single()
                
                if record:
                    return {
                        'name': record['name'],
                        'description': record['description'],
                        'properties': record['properties'],
                        'connections': [conn for conn in record['connections'] if conn['name']]
                    }
                return {}
                
        except Exception as e:
            print(f"❌ Error getting entity {entity_name}: {str(e)}")
            return {}
    
    def close(self):
        if self.driver:
            self.driver.close()