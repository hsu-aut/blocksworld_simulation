def get_additional_rules() -> str:
    return """HANOI TOWERS RULES

The Hanoi Towers problem is a classic puzzle involving three stacks and a number of blocks of different sizes (widths, given by the x_size property of a block) which can be placed on other stacks. 
The puzzle starts with the blocks stacked in ascending order of size on one stack, the smallest at the top.
The objective is to move the entire stack to another stack, following these rules:

1. Only one block can be moved at a time.
2. A block can only be placed on top of a larger block or on an empty stack.
3. To place blocks, the actions of the basic blocksworld problem must be used (i.e. pick_up, put_down, stack, unstack).

The basic blocks world rules are the following:

"""


