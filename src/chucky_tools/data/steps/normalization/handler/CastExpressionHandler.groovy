class CastExpressionHandler extends DefaultHandler {

	CastExpressionHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return "(${expressions[0]}) ( ${expressions[1]} )";
	}

}
