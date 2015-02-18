class ASTNormalizer {

	def handlers;
	def defaultHandler;

	ASTNormalizer() {
		handlers = [:];
		defaultHandler = new DefaultHandler(false, true);
	};

	def addHandler(String type, Handler handler) {
		handlers[type] = handler;
	};

	def getHandler(String type) {
		if (type in handlers) {
			return handlers[type];
		}
		return defaultHandler;
	};
	
	def normalizeTree(root) {
		def expressions = [];
		normalize(root, true, expressions);
		return expressions;
	};

	def normalize(node, store = false, collection) {
		def subexpr = [];
		def expr;
		def handler = getHandler(node.type)
		handler.setNode(node);

		if (node.children()) {
			node.children().each() { child ->
				subexpr.add(normalize(
						child,
						store && !handler.prune(),
						collection));
			}
		}
		expr = handler.merge(subexpr);
		if (store && handler.store()) {
			collection.add("${expr}");
		}
		return expr;
	};

};
