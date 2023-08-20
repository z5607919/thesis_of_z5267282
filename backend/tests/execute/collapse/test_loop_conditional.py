def program():
    i = 1
    twos, fives = 0, 0
    while i < 6:
        if i % 2 == 0:
            print("two")
            twos += 1
        elif i % 5 == 0:
            print("five")
            fives += 1
    
        j = 0
        while j < i:
            print("X", end="")
            j += 1
    
        i += 1
    
    print(f"2s: {twos}, 5s: {fives}")

from collections import OrderedDict
from typing import Type

from analyse import smart_trace
from collapse import collapse
from counter import Counter
from dataframe import DataFrame
from graph import generate_graphs
from helper import get_code_info, get_stripped_line
from line import Line
from evaluate import evaluate
from execute import trace_program
from tree import Block, BodyBlock
from tree_parser import parse

from generate import generate_dataframes

def test_on_while_line():
    root : BodyBlock = parse(program)
    line_mapping : dict[int, Type[Block]] = root.map_lines()
    all_lines : list[Line] = trace_program(program)
    filtered : list[Line] = smart_trace(line_mapping, all_lines)
    line_graphs : list[list[Line]] = generate_graphs(filtered, line_mapping)
    program_code : OrderedDict[int, str] = get_code_info(program)

    assert line_graphs[:2] == [
        [Line(3, {})],
        [Line(3, {}), Line(4, {})]
    ]

    _, graph = line_graphs[:2]
    code, lines, path = collapse(graph, program_code, root)
    _, curr = graph
    assert len(curr.counters) == 1
    counter, = curr.counters
    assert counter.start is None
    assert counter.end is None
    assert not counter.has_valid_range()
