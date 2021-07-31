package ca.utoronto.utm.mcs.entities;

public interface Neo4jRelationship<T> {
    public String relationshipString();
    
    public String nodeId();
}
