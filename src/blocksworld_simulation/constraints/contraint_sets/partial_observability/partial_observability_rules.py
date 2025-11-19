def get_partial_observability_rules() -> str:
    return """## PARTIAL OBSERVABILITY EXTENSION
The following additional constraints apply to this scenario:

### Limited Information Visibility
Only the top two blocks of each stack can be identified with the status tool. All other blocks in the stack are marked as "unknown".

### What You Know
- The exact identity of the top block 
- The exact identity of the second block from top (what the top block is stacked on)
- The total number of blocks in each stack
- All block properties (size, weight, type) for all blocks, even hidden ones
- The robot's current state and held block (if any)

### Dealing with Unknown Blocks
- The identities of blocks deeper than 2 positions in the stack are unknown and represented as "unknown".
- The top 2 visible blocks should be restacked through avaliable tools to reveal the "unknown" blocks below. 
"""