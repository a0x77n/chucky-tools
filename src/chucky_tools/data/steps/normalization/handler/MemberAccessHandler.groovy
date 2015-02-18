class MemberAccessHandler extends DefaultHandler {

	def symbols;

	MemberAccessHandler(boolean prune, boolean store, symb) {
		super(prune, store);
		symbols = symb
	}
    
	String merge(expressions) {
		def code = node.code;
		if (code in symbols) {
			return symbols[code];
		} else {
			return "${expressions[0]} . ${expressions[1]}";
		}
	}

}
