class UnaryOperationHandler extends DefaultHandler {

	def symbols
   
	UnaryOperationHandler(boolean prune, boolean store, symb) {
		super(prune, store);
		symbols = symb;
	}

	String merge(expressions) {
		def code = node.code;
		if (code in symbols) {
			return symbols[code];
		} else if (expressions[0] == "!") {
			return expressions[1];
		} else {
			return "${expressions[0]}  ${expressions[1]}";
		}
	}

	boolean prune() {
		return node.code in symbols || node.code.startsWith("*");
	}
	
}
