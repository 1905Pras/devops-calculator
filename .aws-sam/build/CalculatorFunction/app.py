import json

def validate_operands(a, b):
    if type(a) is not int or type(b) is not int:
        raise ValueError("Operands must be integers.")

    if a <= 0 or b <= 0:
        raise ValueError("Operands must be positive integers.")

def add(a, b):
    validate_operands(a, b)
    return a + b

def subtract(a, b):
    validate_operands(a, b)
    return a - b

def multiply(a, b):
    validate_operands(a, b)
    return a * b

def calculate(operation, a, b):
    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
    }
    if not isinstance(operation, str) or operation not in operations:
        raise ValueError(
            "Operation must be add, subtract, or multiply."
        )
    return operations[operation](a, b)


def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            data = json.loads(body)
        elif isinstance(body, dict):
            data = body
        elif body is None:
            data = event
        else:
            raise ValueError("Invalid request body.")
        if not isinstance(data, dict):
            raise ValueError("Request must be a JSON object.")
        result = calculate(
            data.get("operation"),
            data.get("a"),
            data.get("b"),
        )
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"result": result}),
        }
    except (ValueError, TypeError) as exc:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(exc)}),
        }