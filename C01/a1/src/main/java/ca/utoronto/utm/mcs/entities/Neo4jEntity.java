package ca.utoronto.utm.mcs.entities;

public interface Neo4jEntity<T> {

	public String nodeCreationString();
	
	public String nodeId();
    
    public String nodeName();
	
	public String label();
}
