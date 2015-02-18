Gremlin.defineStep('normalize', [Vertex, Pipe], { symbols ->

	def normalizer = new ASTNormalizer();
	def handler;
    
	handler = new DefaultHandler(true, false);
	normalizer.addHandler('IncDec', handler);
	normalizer.addHandler('CastTarget', handler);

	handler = new DefaultHandler(false, false);
	normalizer.addHandler('Condition', handler);

	handler = new IdentifierHandler(false, true, symbols, ['NULL']);
	normalizer.addHandler('Identifier', handler);

	handler = new PtrMemberAccessHandler(true, true, symbols);
	normalizer.addHandler('PtrMemberAccess', handler);

	handler = new MemberAccessHandler(true, true, symbols);
	normalizer.addHandler('MemberAccess', handler);
    
	handler = new CalleeHandler(true, true);
	normalizer.addHandler('Callee', handler);
    
	handler = new ArgumentHandler(true, false);
	normalizer.addHandler('Argument', handler);

	handler = new ArgumentListHandler(true, false);
	normalizer.addHandler('ArgumentList', handler);

	handler = new CallExpressionHandler(false, false);
	normalizer.addHandler('CallExpression', handler);
    

	handler = new BinaryOperationHandler(false, true);
	normalizer.addHandler('AndExpression', handler);
	normalizer.addHandler('BitAndExpression', handler);
	normalizer.addHandler('InclusiveOrExpression', handler);
	normalizer.addHandler('ExclusiveOrExpression', handler);
	normalizer.addHandler('OrExpression', handler);
	normalizer.addHandler('ShiftExpression', handler);
	normalizer.addHandler('AndExpression', handler);

	handler = new RelationalOperationHandler(false, true);
	normalizer.addHandler('RelationalExpression', handler);
	normalizer.addHandler('EqualityExpression', handler);
    
	handler = new ArithmeticOperationHandler(false, true);
	normalizer.addHandler('AdditiveExpression', handler);
	normalizer.addHandler('MultiplicativeExpression', handler);
    
	handler = new PrimaryExpressionHandler(false, false);
	normalizer.addHandler('PrimaryExpression', handler);
    
	handler = new CastExpressionHandler(false, true);
	normalizer.addHandler('CastExpression', handler);
    
	handler = new AssignmentExpressionHandler(false, true);
	normalizer.addHandler('AssignmentExpr', handler);
    
	handler = new ArrayIndexingHandler(false, true);
	normalizer.addHandler('ArrayIndexing', handler);
    
	handler = new ConditionalExpressionHandler(false, true);
	normalizer.addHandler('ConditionalExpression', handler);

	handler = new UnaryOperationHandler(false, true, symbols);
	normalizer.addHandler('UnaryOp', handler);

	handler = new UnaryOperatorHandler(false, false);
	normalizer.addHandler('UnaryOperator', handler);

	_().transform{ normalizer.normalizeTree(it) }.scatter()

});
