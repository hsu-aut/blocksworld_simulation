from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("RobotActions")

SIM_API = "http://localhost:5001"  # URL of the Blocksworld simulation API

@mcp.tool()
def pick_up(block:str) -> str:
    """
    Description:
        Picks up a block that is lying on the ground.

    Prerequisite: 
        The block must not be stacked on another block 
        There must not be any other block on top of it.

    Result:
        The robot will hold the block.

    Args: 
        block (str): The name of the block to pick up.
    """
    try:
        r = requests.post(f"{SIM_API}/pick_up", json={"block": block}, timeout=2)
        return r.json().get("result", f"Requested pick_up {block}")
    except Exception as e:
        return f"[ERROR]: {str(e)}"


@mcp.tool()
def put_down(block:str) -> str:
    """
    Description:
        Puts down a held block on the ground.

    Prerequisite:
        The robot must hold the block
        There must be a free space on the ground.

    Result:
        The block will be placed on the ground.
        Robot is free.

    Args:
        block (str): The name of the block to put down.
    """
    try:
        r = requests.post(f"{SIM_API}/put_down", json={"block": block}, timeout=2)
        return r.json().get("result", f"Requested put_down {block}")
    except Exception as e:
        return f"[ERROR]: {str(e)}"


@mcp.tool()
def stack(block1:str, block2:str) -> str:
    """
    Description:
        Stacks block1 on top of block2.

    Prerequisite    
        The robot must hold block1.
        Block2 must not have any block on top of it.

    Result:
        Block1 will be stacked on block2.

    Args:
        block1 (str): The name of the block to stack.
        block2 (str): The name of the block on which to stack.
    """
    try:
        r = requests.post(f"{SIM_API}/stack", json={"block1": block1, "block2": block2}, timeout=2)
        return r.json().get("result", f"Requested stack {block1} on {block2}")
    except Exception as e:
        return f"[ERROR]: {str(e)}" 


@mcp.tool()
def unstack(block1:str, block2:str) -> str: 
    """
    Description:
        Unstacks block1 from block2.

    Prerequisite:
        The robot must hold block1.
        Block2 must have block1 on top of it.         
    Result:
        Block1 will be unstacked from block2 and the robot will hold it.

    Args:
        block1 (str): The name of the block to unstack.
        block2 (str): The name of the block from which to unstack.
    """
    try:
        r = requests.post(f"{SIM_API}/unstack", json={"block1": block1, "block2": block2}, timeout=2)
        return r.json().get("result", f"Requested unstack {block1} from {block2}")
    except Exception as e:
        return f"[ERROR]: {str(e)}"
    
@mcp.tool()
def get_status() -> str: 
    """
    Description:
        Queries the current status of the system
     
    Result:
        Returns the current status of the robot including any held blocks and the positions of the blocks.

    Args:
        None
    """
    try:
        r = requests.post(f"{SIM_API}/get_status", json={}, timeout=2)
        return r.json().get("result", "Requested get_status")
    except Exception as e:
        return f"[ERROR]: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")