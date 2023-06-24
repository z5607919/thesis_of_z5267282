import inspect
from typing import Callable, Type

from cfg import OFFSET
from errors import ExpectedIfBlock
import helper
from stack import Stack
from tree import \
    Block, CodeBlock, BodyBlock, IfBlock, ElseBlock, ElifBlock, WhileBlock

def parse(program : Callable):
    lines, start = get_code_info(program)
    root, stack, prev_indent, line_no = init_state()

    for line_no, line_contents in enumerate(lines[OFFSET:], start=start):
        line         : str = helper.get_stripped_line(line_contents)
        indent_level : int = helper.num_leading_whitespace(line_contents)

        # first line
        if prev_indent is None:
            prev_indent = indent_level
            root, stack = parse_first_line(line, line_no, indent_level)
            continue

        top   : Type[BodyBlock] = stack.peek()
        block : Type[Block] = parse_line(line, line_no, indent_level)
        if indent_level == prev_indent:
            parse_same_level_block(block, line_no, top, stack)
        elif indent_level > prev_indent:
            parse_indented_block(block, line_no, top, stack)
        else:
            parse_unindented_block(block, line_no, indent_level, top, stack)
        prev_indent = indent_level

    # last line
    last : int = start + len(lines) - 1 - OFFSET
    top  : Type[BodyBlock] = stack.peek()
    if top.code_block is not None:
        top.code_block.end = last
        top.code_block = None
    while not stack.empty():
        top = stack.pop()
        top.end = last
    return root

def get_code_info(program : Callable):
    lines, start = inspect.getsourcelines(program)
    start += OFFSET
    return lines, start

def init_state():
    root        : BodyBlock = None
    stack       : Stack = None
    prev_indent : int = None
    line_no     : int = 0
    return root, stack, prev_indent, line_no

def parse_line(line : str, line_no : int, indent_level : int):
    if line.startswith("if"):
        return IfBlock(line_no, indent_level)
    if line.startswith("while"):
        return WhileBlock(line_no, indent_level)
    if line.startswith("elif"):
        return ElifBlock(line_no, indent_level)
    if line.startswith("else"):
        return ElseBlock(line_no, indent_level)
    return CodeBlock(line_no)

def parse_first_line(line : str, line_no : int, indent_level : int):
    """parse the first line in the program
    return the root of the tree and a stack with it"""
    first_block : Type[Block] = parse_line(line, line_no, indent_level)
    root = BodyBlock(line_no, indent_level)
    stack = Stack(root)
    if isinstance(first_block, (IfBlock, WhileBlock)):
        stack.push(first_block)
    elif isinstance(first_block, CodeBlock):
        root.code_block = first_block
    root.add_same_level_block(first_block)

    return root, stack

def parse_same_level_block(
    block : Type[Block], line_no : int, top : Type[BodyBlock], stack : Stack
):
    if isinstance(block, CodeBlock):
        return

    if isinstance(block, (IfBlock, WhileBlock)):
        top.end_code_block(line_no - 1)
        top.add_same_level_block(block)
        stack.push(block)

def parse_indented_block(
    block : Type[Block], line_no : int, top : Type[BodyBlock], stack : Stack
):
    if isinstance(block, CodeBlock):
        top.code_block = block 
    elif isinstance(block, (IfBlock, WhileBlock)):
        stack.push(block) 
    top.add_same_level_block(block)

def parse_unindented_block(
    block : Type[Block], line_no : int, indent_level : int,
    top : Type[BodyBlock], stack : Stack,
):
    prev : int = line_no - 1
    top.end_code_block(prev)
    # pop off stack until same level block
    # assumes consistent indentation levels have been followed
    # basically ends all indents inside the current level
    while top.indent_level != indent_level:
        top.end = prev
        top = stack.pop()

    is_elif : bool = isinstance(block, ElifBlock)
    if is_elif or isinstance(block, ElseBlock):
        # the top will either be the if, or an elif
        # if not, the top elif has ended
        if isinstance(top, ElifBlock):
            top.end_code_block(prev)
            top.end = prev
            top = stack.pop_peek()
        add_branch : Callable = \
            top.add_elif if is_elif else top.add_else
        add_branch(block)
        stack.push(block)
    else:
        # must end the current if branch if any
        is_el_block : bool = isinstance(top, (ElifBlock, ElseBlock))
        if isinstance(top, IfBlock) or is_el_block:
            top.end_code_block(prev)
            top.end = prev
            top = stack.pop_peek()
            # end the entire if block now
            if is_el_block:
                if not isinstance(top, IfBlock):
                    raise ExpectedIfBlock
                top.end = prev
                top = stack.pop_peek()
        elif isinstance(top, WhileBlock):
            # a while by this point should have had its code block ended
            top.end = prev
            top = stack.pop_peek()

        # now handle the stack
        if isinstance(block, CodeBlock):
            top.code_block = block 
        else:
            stack.push(block)
        top.add_same_level_block(block)
