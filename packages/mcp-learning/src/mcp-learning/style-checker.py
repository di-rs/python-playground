import os

from fastmcp import FastMCP

dirname = os.path.dirname(__file__)
style_guide_path = os.path.join(dirname, "..", "style-guide.md")

mcp = FastMCP(name="code-review-server", version="1.0.0")


@mcp.prompt(
    name="review-code",
    title="Code Review",
    description="Review code for best practices and potential issues",
)
def review_code(code: str) -> str:
    return f"""Please review this code to see if it follows our best practices.
        Use this Airbnb style guide as a reference and the rules
        in it to review the code. \n\n========\n\n
        ```{open(style_guide_path).read()}```\n\n
        ========\n\nCode to review:\n```{code}```
    """


if __name__ == "__main__":
    mcp.run()
