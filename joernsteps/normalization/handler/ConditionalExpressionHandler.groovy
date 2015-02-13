class ConditionalExpressionHandler extends DefaultHandler {

	ConditionalExpressionHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return "${expressions[0]} ? ${expressions[1]} : ${expressions[2]}";
	}
    
}
