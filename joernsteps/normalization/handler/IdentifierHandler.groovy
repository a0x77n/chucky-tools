class IdentifierHandler extends DefaultHandler {

	def symbols;
	def except;
    
	IdentifierHandler(boolean prune, boolean store, symb, excp) {
		super(prune, store);
		symbols = symb;
		except = excp;
	}
    
	String merge(expressions) {
		def code = node.code;
		if (code in symbols) {
			return symbols[code];
		} else {
			return code;
		}
	}

	boolean store() {
		return store && !(node.code in except);
	}    
	

}
