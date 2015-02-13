class PrimaryExpressionHandler extends DefaultHandler {
	
	PrimaryExpressionHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		def code = node.code;
		if (code.startsWith(/'/) || code.startsWith(/"/)) {
			return code;
		} else {
			return NUM;
		}
	}

}
