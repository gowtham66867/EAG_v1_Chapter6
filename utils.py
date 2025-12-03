import ast

def parse_function_call_params(param_parts: list[str]) -> dict:
    """
    Parses key=value parts from the FUNCTION_CALL format.
    Supports nested keys like input.string=foo and list values like input.int_list=[1,2,3]
    Returns a nested dictionary.
    """
    result = {}

    for part in param_parts:
        if "=" not in part:
            raise ValueError(f"Invalid parameter format (expected key=value): {part}")

        key, value = part.split("=", 1)

        # Try to parse as Python literal (int, float, list, etc.)
        try:
            parsed_value = ast.literal_eval(value)
        except Exception:
            parsed_value = value.strip()

        # Support nested keys like input.string
        keys = key.split(".")
        current = result
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = parsed_value

    return result
