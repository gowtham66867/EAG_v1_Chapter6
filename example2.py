# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import time
from models import AddInput, AddOutput, SqrtInput, SqrtOutput, StringsToIntsInput, StringsToIntsOutput, ExpSumInput, ExpSumOutput, WebSearchInput, WebSearchOutput, IntOutput, FloatOutput, ImageOutput, ListIntOutput, StringOutput


# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(input: AddInput) -> AddOutput:
    """Add two numbers"""
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=input.a + input.b)

@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(SqrtInput) -> SqrtOutput")
    return SqrtOutput(result=input.a ** 0.5)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> IntOutput:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> IntOutput:")
    return IntOutput(result=int(a - b))

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> IntOutput:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> IntOutput:")
    return IntOutput(result=int(a * b))

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> FloatOutput:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> FloatOutput:")
    return FloatOutput(result=float(a / b))

# power tool

# web search tool (mock)
@mcp.tool()
def web_search(input: WebSearchInput) -> WebSearchOutput:
    """Searches the web for a given query. Use this to find information you don't know."""
    print(f"CALLED: web_search(WebSearchInput) -> WebSearchOutput")
    # This is a mock tool. In a real scenario, this would call a search API.
    mock_db = {
        "number of moons of jupiter": "95",
        "number of moons of mars": "2",
        "capital of france": "Paris"
    }
    query = input.query.lower()
    result = "Information not found."
    # A more robust check for a mock tool
    if "jupiter" in query and "moons" in query:
        result = mock_db["number of moons of jupiter"]
    elif "mars" in query and "moons" in query:
        result = mock_db["number of moons of mars"]
    elif "france" in query and "capital" in query:
        result = mock_db["capital of france"]
    return WebSearchOutput(result=result)
@mcp.tool()
def power(a: int, b: int) -> IntOutput:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> IntOutput:")
    return IntOutput(result=int(a ** b))


# cube root tool
@mcp.tool()
def cbrt(a: int) -> FloatOutput:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> FloatOutput:")
    return FloatOutput(result=float(a ** (1/3)))

# factorial tool
@mcp.tool()
def factorial(a: int) -> IntOutput:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> IntOutput:")
    return IntOutput(result=int(math.factorial(a)))

# log tool
@mcp.tool()
def log(a: int) -> FloatOutput:
    """log of a number"""
    print("CALLED: log(a: int) -> FloatOutput:")
    return FloatOutput(result=float(math.log(a)))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> IntOutput:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> IntOutput:")
    return IntOutput(result=int(a % b))

# sin tool
@mcp.tool()
def sin(a: int) -> FloatOutput:
    """sin of a number"""
    print("CALLED: sin(a: int) -> FloatOutput:")
    return FloatOutput(result=float(math.sin(a)))

# cos tool
@mcp.tool()
def cos(a: int) -> FloatOutput:
    """cos of a number"""
    print("CALLED: cos(a: int) -> FloatOutput:")
    return FloatOutput(result=float(math.cos(a)))

# tan tool
@mcp.tool()
def tan(a: int) -> FloatOutput:
    """tan of a number"""
    print("CALLED: tan(a: int) -> FloatOutput:")
    return FloatOutput(result=float(math.tan(a)))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> IntOutput:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> IntOutput:")
    return IntOutput(result=int(a - b - b))

@mcp.tool()
def create_thumbnail(image_path: str) -> ImageOutput:
    """Create a thumbnail of an image"""
    print(f"CALLED: create_thumbnail(image_path: {image_path}) -> ImageOutput:")
    try:
        img = PILImage.open(image_path)
        img.thumbnail((128, 128))
        return ImageOutput(result=Image.from_pil(img))
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput")
    ascii_values = [ord(char) for char in input.string]
    return StringsToIntsOutput(ascii_values=ascii_values)

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput")
    result = sum(math.exp(i) for i in input.int_list)
    return ExpSumOutput(result=result)

@mcp.tool()
def fibonacci_numbers(n: int) -> ListIntOutput:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> ListIntOutput:")
    if n <= 0:
        return ListIntOutput(result=[])
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return ListIntOutput(result=fib_sequence[:n])




# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> StringOutput:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> StringOutput:")
    return StringOutput(result=f"Hello, {name}!")


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> StringOutput:
    print("CALLED: review_code(code: str) -> StringOutput:")
    return StringOutput(result=f"Please review this code:\n\n{code}")


@mcp.prompt()
def debug_error(error: str) -> StringOutput:
    # The multi-message format is not directly supported by our simple executor.
    # We will return a single string representing the interaction.
    return StringOutput(result=f"User: I'm seeing this error: {error}\nAssistant: I'll help debug that. What have you tried so far?")

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE SERVER AT AMAZING LOCATION")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
