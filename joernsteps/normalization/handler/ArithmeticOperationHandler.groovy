class ArithmeticOperationHandler extends DefaultHandler {

	ArithmeticOperationHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		if (expressions[0] == NUM && expressions[1] == NUM) {
			return NUM;
		} else {
			return "( ${expressions[0]} ${node.operator} ${expressions[1]} )";
		}
	}

}
