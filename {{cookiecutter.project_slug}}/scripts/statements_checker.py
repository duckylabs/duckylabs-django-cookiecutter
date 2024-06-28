from __future__ import absolute_import, print_function, unicode_literals

import argparse
import ast
import platform
import sys
import traceback


class DisallowedStatementVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.disallowed_statement_visited = False
        self.disallowed_statements = (
            "print",
            "breakpoint",
            "ugettext",
            "ungettext",
            "ugettext_lazy",
            "ungettext_lazy",
        )

    def found_disallowed_statement(self, lineno, col_offset, statement_name):
        self.disallowed_statement_visited = True
        print(
            "{}:{}:{} found {} call".format(
                self.filename, lineno, col_offset, statement_name
            )
        )

    def visit_DisallowedStatement(self, node):
        self.found_disallowed_statement(node.lineno, node.col_offset, False)
        self.generic_visit(node)

    def visit_Call(self, node):
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in self.disallowed_statements
        ):
            self.found_disallowed_statement(node.lineno, node.col_offset, node.func.id)
        self.generic_visit(node)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, "rb") as f:
                visitor = DisallowedStatementVisitor(filename)
                visitor.visit(ast.parse(f.read(), filename=filename))
                if visitor.disallowed_statement_visited:
                    retval = 1
        except SyntaxError:
            print(
                "{}: failed parsing with {} {}:".format(
                    filename,
                    platform.python_implementation(),
                    sys.version.partition(" ")[0],
                )
            )
            print(
                "\n{}".format("    " + traceback.format_exc().replace("\n", "\n    "))
            )
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
