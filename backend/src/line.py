from fractions import Fraction

from counter import Counter
from state import State
from tree import WhileBlock

class Line:
    """A dataclass to store line information"""
    def __init__(self, line_no : int, prev_vars : dict[str, str]):
        self.line_no  : int = line_no
        self.output   : list[str] = []
        self.vars     : State = State(prev_vars)
        # counters are stored from least indented to most indented
        self.counters : list[Counter] = []
    
    def __str__(self):
        return str(self.line_no)
    
    def __eq__(self, other : "Line"):
        return self.line_no == other.line_no
    
    def long_str(self):
        return f"""line no {self.line_no}:
    output: {self.output}
    vars  :
        - prev: {self.vars.prev}
        - curr: {self.vars.curr}"""
    
    def add_counter(self, iteration : Fraction, while_ : WhileBlock):
        """Add a counter of an increased depth"""
        self.counters.append(Counter(iteration, while_))
