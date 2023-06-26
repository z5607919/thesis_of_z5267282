from tree import CodeBlock

def test_code_block():
    c = CodeBlock(2)
    c.end = 3
    line_mapping = {}
    c.map_lines(line_mapping)

    assert line_mapping == {
        2 : c,
        3 : c
    }
