class DefaultHandler implements Handler {

	static final String CMP = "\$CMP";
	static final String NUM = "\$NUM";

	boolean prune;
	boolean store;

	Neo4j2Vertex node;

	DefaultHandler(boolean prune, boolean store) {
		this.prune = prune;
		this.store = store;
	}

	String merge(expressions) {
		return node.code;
	}

	boolean prune() {
		return prune;
	}

	boolean store() {
		return store;
	}    

	void setNode(Neo4j2Vertex n) {
		node = n;
	}

}
