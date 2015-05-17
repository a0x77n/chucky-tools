Gremlin.defineStep('normalize', [Vertex, Pipe], { symbols ->

	def node_data_store = [];
	def handler = [:];

	generic_handler = { node, store=true, prune=false, merge ->
		children = node.children().toList();
		if (!children.isEmpty()) {
			x = children.collect{ handler[it.type](it, !prune) };
			node_data = merge(x);
		} else {
			node_data = "$node.code";
		}
		if (store) node_data_store?.add(node_data);
		return node_data;
	};

	identifier_handler = { node, store=true->
		if (node.code in symbols) {
			node_data = symbols[node.code]
			if (store && node.code != 'NULL') node_data_store?.add(node_data);
		} else  {
			node_data = node.code
		}
		if (store && node.code != 'NULL') node_data_store?.add(node_data);
		return node_data;
	}

	primary_expression_handler = { node, store=true ->
		if (node.code.startsWith(/'/) || node.code.startsWith(/"/)) {
			node_data = "\$STR";
		} else {
			node_data = "\$NUM";
		}
		if (store && false) node_data_store?.add(node_data);
		return node_data;
	}

	binary_operation_handler = { node, store=true ->
		children = node.children().toList();
		operands = children.collect{ handler[it.type](it) };
		if (operands[0] == "\$NUM" && operands[1] == "\$NUM")
			node_data = "\$NUM";
		else 
			node_data = "( ${operands[0]} ${node.operator} ${operands[1]} )";
		if (store) node_data_store?.add(node_data);
		return node_data;
	}

	comparison_handler = { node, store=true ->
		merge = { children -> "${children[0]} \$CMP ${children[1]}" };
		return generic_handler(node, true, merge);
	}
	
	array_indexing_handler = { node, store=true ->
		merge = { children -> "${children[0]} [ ${children[1]} ]" };
		return generic_handler(node, true, merge);
	}

	call_expression_handler = { node, store=true ->
		callee = node.children().toList()[0];
		node_data = callee.code;
		if (store) node_data_store?.add(node_data);
		return node_data;
	}

	member_access_handler = { node, store=true ->
		if (node.code in symbols)
			node_data = "\$SYM";
		else {
			merge = { children -> "${children[0]} . ${children[1]}" };
			node_data = generic_handler(node, true, true, merge);
		}
		if (store) node_data_store?.add(node_data);
		return node_data;
	}

	ptr_member_access_handler = { node, store=true ->
		if (node.code in symbols)
			node_data = "\$SYM";
		else {
			merge = { children -> "${children[0]} -> ${children[1]}" };
			node_data = generic_handler(node, true, true, merge);
		}
		if (store) node_data_store?.add(node_data);
		return node_data;
	}

	cast_target_handler = { node, store=true ->
		return generic_handler(node, store, false, null);
	}

	cast_expression_handler = { node, store=true ->
		merge = { children -> "(${children[0]}) ${children[1]}" };
		return generic_handler(node, true, false, merge);
	}

	condition_handler = { node, store=true ->
		merge = { children -> "${children[0]}" };
		return generic_handler(node, false, false, merge);
	}

	conditional_expression_handler = { node, store=true ->
		merge = { children -> "${children[0]} ? ${children[1]} : ${children[2]}" };
		return generic_handler(node, true, false, merge);
	}

	unary_operator_handler = { node, store=true ->
		return generic_handler(node, store, false, null);
	}

	unary_operation_handler = { node, store=true ->
		merge = { children -> if (children[0] != "!") "${children[0]} ${children[1]}" else "${children[1]}" }
		return generic_handler(node, store, true, merge);
	}

	unary_expression_handler = { node, store=true ->
		merge = { children -> "${children[0]} ${children[1]}" }
		return generic_handler(node, store, true, merge);
	}

	assignment_expression_handler = { node, store=true ->
		merge = { children -> "${children[0]} = ${children[1]}" };
		return generic_handler(node, store, false, merge);
	}

	sizeof_expression_handler = { node, store=true ->
		merge = { children -> "${children[0]} ( ${children[1]} )" };
		return generic_handler(node, store, false, merge);
	}

	sizeof_handler = { node, store=true ->
		return generic_handler(node, store, false, null);
	}

	sizeof_operand_handler = { node, store=true ->
		merge = { children -> "${children[0]}" };
		return generic_handler(node, false, false, merge);
	}

	incdec_operation_handler = { node, store=true ->
		merge = { children -> "${children[0]} ${children[1]}" };
		return generic_handler(node, true, false, merge);
	}

	incdec_handler = { node, store=true ->
		return generic_handler(node, true, false, null);
	}

	handler['Condition'] = condition_handler;
		
	handler['AdditiveExpression'] = binary_operation_handler;
	handler['MultiplicativeExpression'] = binary_operation_handler;

	handler['InclusiveOrExpression'] = binary_operation_handler;
	handler['ExclusiveOrExpression'] = binary_operation_handler;
	handler['OrExpression'] = binary_operation_handler;
	handler['AndExpression'] = binary_operation_handler;
	handler['BitAndExpression'] = binary_operation_handler;
	handler['ShiftExpression'] = binary_operation_handler;
	handler['AssignmentExpr'] = binary_operation_handler;

	handler['EqualityExpression'] = comparison_handler;
	handler['RelationalExpression'] = comparison_handler;
	handler['ConditionalExpression'] = conditional_expression_handler;

	handler['Identifier'] = identifier_handler;
	handler['MemberAccess'] = member_access_handler;
	handler['PtrMemberAccess'] = ptr_member_access_handler;

	handler['ArrayIndexing'] = array_indexing_handler;

	handler['CallExpression'] = call_expression_handler;

	handler['CastExpression'] = cast_expression_handler;
	handler['CastTarget'] = cast_target_handler;

	handler['PrimaryExpression'] = primary_expression_handler;

	handler['IncDec'] = incdec_handler;
	handler['IncDecOp'] = incdec_operation_handler;

	handler['Sizeof'] = sizeof_handler;
	handler['SizeofExpr'] = sizeof_expression_handler;
	handler['SizeofOperand'] = sizeof_operand_handler;

	handler['UnaryExpression'] = unary_expression_handler;

	handler['UnaryOp'] = unary_operation_handler;
	handler['UnaryOperator'] = unary_operator_handler;

	_().sideEffect{ handler[it.type](it) }.transform{ node_data_store }.scatter()

});
