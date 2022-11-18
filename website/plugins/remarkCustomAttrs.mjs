const parseAttribute = (expression) => {
    if (expression.type !== 'AssignmentExpression' || !expression.left || !expression.right) {
        return
    }

    const { left, right } = expression

    if (left.type !== 'Identifier' || right.type !== 'Literal' || !left.name || !right.value) {
        return
    }

    return { type: 'mdxJsxAttribute', name: left.name, value: right.value }
}

const parseAstTree = (markdownAST) => {
    markdownAST.children.map((node, index) => {
        if (node.type !== 'heading' || !node.children || node.children < 2) {
            return
        }

        const indexLast = node.children.length - 1
        const lastNode = node.children[indexLast]

        if (lastNode.type !== 'mdxTextExpression' || !lastNode.data || !lastNode.data.estree) {
            return
        }

        const { estree } = lastNode.data

        if (
            estree.type !== 'Program' ||
            !estree.body ||
            estree.body.length <= 0 ||
            !estree.body[0]
        ) {
            return
        }

        const estreeBodyFirstNode = estree.body[0]

        if (estreeBodyFirstNode.type !== 'ExpressionStatement' || !estreeBodyFirstNode.expression) {
            return
        }

        const statement = estreeBodyFirstNode.expression

        const attributeExpressions = [
            ...(statement.type === 'SequenceExpression' && statement.expressions
                ? statement.expressions
                : []),
            ...(statement.type === 'AssignmentExpression' ? [statement] : []),
        ]

        // This replaces the markdown heading with a JSX element
        markdownAST.children[index] = {
            type: 'mdxJsxFlowElement',
            name: `h${node.depth}`,
            attributes: attributeExpressions.map(parseAttribute),
            children: [node.children[0]],
        }
    })

    return markdownAST
}

const remarkCustomAttrs = () => parseAstTree

export default remarkCustomAttrs
