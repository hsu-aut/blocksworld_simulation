def get_partial_observability_rules() -> str:
    return """## PARTIAL OBSERVABILITY EXTENSION
The following additional constraints apply to this scenario:

### Limited Information Visibility
**Only the top two blocks of each stack are fully identified.** All other blocks in the stack are marked as "unknown".

### What You Know
- The exact identity of the **top block** 
- The exact identity of the **second block from top** (what the top block is stacked on)
- The **total number of blocks** in each stack
- **All block properties** (size, weight, type) for all blocks, even hidden ones
- The robot's current state and held block (if any)

### What You Don't Know
- The identities of blocks deeper than 2 positions in the stack
- The exact arrangement of hidden blocks below the top two visible blocks
"""