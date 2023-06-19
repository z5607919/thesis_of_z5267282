from tree_parser import parse

def test_no_indentation():
    def simple():
        i = 0
        print(i)

    root = parse(simple)
    assert root.to_dict() == {
        "BodyBlock" : {
            "start": 5,
            "end"  : 6,
            "body" : [
                {
                    "CodeBlock" : {
                        "start": 5,
                        "end"  : 6 
                    }
                }
            ]
        }
    }

def test_large():
    def large():
        i = 1
        twos, sevens = 0, 0
        while i < 100:
            if i % 2 == 0:
                print("two")
                twos += 1
            elif i % 7 == 0:
                print("seven")
                sevens += 1
            i += 1

        print(f"2s: {twos}, 7s: {sevens}")
    
    root = parse(large)
    assert root.to_dict() == {
        "BodyBlock" : {
            "start" : 26,
            "end"   : 37,
            "body" : [
                {
                    "CodeBlock" : {
                        "start" : 26,
                        "end"   : 27
                    }
                },
                {
                    "WhileBlock" : {
                        "start" : 28,
                        "end"   : 35,
                        "body" : [
                            {
                                "IfBlocK" : {
                                    "start" : 29,
                                    "end"   : 34,
                                    "body" : [
                                        {
                                            "CodeBlock" : {
                                                "start" : 30,
                                                "end"   : 31
                                            }
                                        }
                                    ],
                                    "elifs" : [
                                        {
                                            "ElifBlock" : {
                                                "start" : 32,
                                                "end"   : 34
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "CodeBlock" : {
                                    "start" : 35,
                                    "end"   : 35
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }    

def test_simple_if():
    def if_block():
        i = 0
        if i % 2 == 0:
            print("even")

    root = parse(if_block)
    print(root.pretty_print())
    assert root.to_dict() == {
        "BodyBlock" : {
            "start" : 93,
            "end"   : 95,
            "body"  : [
                {
                    "CodeBlock" : {
                        "start" : 93,
                        "end"   : 93
                    }
                },
                {
                    "IfBlock" : {
                        "start" : 94,
                        "end"   : 95,
                        "body" : [
                            {
                                "CodeBlock" : {
                                    "start" : 95,
                                    "end" : 95
                                }
                            }
                        ],
                        "elifs" : [],
                        "else"  : None
                    }
                }
            ]
        }
    }
