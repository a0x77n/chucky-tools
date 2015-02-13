class RelationalOperationHandler extends DefaultHandler {

	RelationalOperationHandler(boolean prune, boolean store) {
		super(prune, store);
	}

	String merge(expressions) {
		return "( ${expressions[0]} ${CMP} ${expressions[1]} )";
	}

}
