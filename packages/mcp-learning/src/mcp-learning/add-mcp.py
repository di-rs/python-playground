from fastmcp import FastMCP

mcp = FastMCP("My MCP Demo")


@mcp.tool(name="Addition Tool", description="Add two numbers together")
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    mcp.run()
