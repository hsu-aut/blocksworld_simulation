def get_additional_rules() -> str:
    return """#Block Size Rules

1. Only one block can be moved at a time.
2. A block can only be placed on top of a larger or equally sized block or on an empty stack.
3. To place blocks, the actions of the basic blocksworld problem must be used (i.e. pick_up, put_down, stack, unstack).

The basic blocks world rules have to be obeyed, they can be found in the following section.

"""


