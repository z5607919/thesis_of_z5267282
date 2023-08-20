from collections import OrderedDict

from tree import WhileBlock

class Counter:
    """A dataclass to store counter information"""
    def __init__(self, iteration : int, total : int, while_ : WhileBlock):
        self.iteration = iteration
        self.total = total
        self.while_ = while_
        self.start = None
        self.end = None
    
    def __str__(self):
        return f"({self.iteration}/{self.total}) : {self.while_}"
    
    def __eq__(self, other : "Counter"):
        return self.iteration == other.iteration and self.total == other.total

    def __ne__(self, other : "Counter"):
        return not self == other
    
    def find_filtered_range(self, filtered : OrderedDict[int, bool]):
        keys = list(filtered)
        try:
            index = keys.index(self.while_.start)
        except ValueError:
            return

        # if the while is last in filtered graph, it is being evaluated
        # should be impossible for a while to be the last filtered line
        # a while can only ever be the second last item in the filtered list
        # where its body should be last
        if index == len(keys) - 1:
            return
        
        # we should still display statistics for a while if we're up to it
        if index == len(keys) - 2:
            self.start = index
            self.end = index
            return
        
        # while loop might have already been collapsed
        if not filtered[keys[index + 1]]:
            return

        self.start = index
        # note the lines should be in non-decreasing order
        for i, key in enumerate(keys[index:], start=index):
            if key > self.while_.end:
                break

            if key <= self.while_.end:
                self.end = i
        # after the loop terminates, i should be the largest index:
        # 1. key[i] <= while end
        # 2. consecutive from index

        # possible that self.start is None, but not self.end
        # this will be considered invalid later

    def has_valid_range(self):
        if self.start is None or self.end is None:
        # if self.start is None or self.end is None or self.start == self.end:
            return False
        return True
    
    def to_dict(self):
        return {
            "start"       : self.start,
            "end"         : self.end,
            "numerator"   : self.iteration,
            "denominator" : self.total
        }
