class BinaryOperationHandler extends DefaultHandler {

	BinaryOperationHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return "${expressions[0]} ${node.operator} ${expressions[1]}";
	}

}
