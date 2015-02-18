class ArgumentHandler extends DefaultHandler {

	ArgumentHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return expressions[0];
	}

}
