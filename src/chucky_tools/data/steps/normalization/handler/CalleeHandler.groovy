class CalleeHandler extends DefaultHandler {

	CalleeHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return expressions[0];
	}
    
}
