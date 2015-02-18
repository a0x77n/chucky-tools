class ArgumentListHandler extends DefaultHandler {
	
	ArgumentListHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return expressions.join(", ");
	}

}
