# Blocksworld_Robot_Actions_Server.py
from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("RobotActions")

SIM_API = "http://localhost:5001"  # URL of the Blocksworld simulation API

@mcp.tool()
def pick_up(block:str) -> str:
    """
    Description:
        Picks up a block that is lying directly on the ground.

    Requirements: 
        The block to be picked up must be on the ground (= block is in the first position of the stack).
        There must not be any other block on top of it.
        Robot must be idle.

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
def unstack(block1:str, block2:str) -> str: 
    """
    Description:
        Unstacks block1 from block2.

    Requirements:
        The robot must be idle.
        block2 must have block1 on top of it.  
           
    Result:
        block1 will be unstacked from block2 and the robot will hold it.

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
def put_down(block:str) -> str:
    """
    Description:
        Puts down a held block directly on the ground on a free stack.

    Requirements:
        There must be a free space on the ground (= One stack has to be empty).
        The robot must hold the block.

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

    Requirements:    
        The robot must hold block1.
        Block2 must not have any block on top of it.

    Result:
        Block1 will be stacked on block2.
        Robot is free.

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
def get_status() -> str: 
    """
    Description:
        Queries the current status of the system
     
    Requirements:
        None

    Result:
        Returns the current status of the robot including any held blocks and the total number of available positions on the ground and the current order of the blocks.


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
