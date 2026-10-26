import json
import pytest

from app import (
    add,
    subtract,
    multiply,
    calculate,
    lambda_handler,
)


def test_add():
    assert add(10, 5) == 15


def test_subtract():
    assert subtract(10, 5) == 5


def test_multiply():
    assert multiply(10, 5) == 50


def test_subtract_negative_result():
    assert subtract(2, 5) == -3


@pytest.mark.parametrize(
    "a,b",
    [(0, 5), (5, 0), (-1, 5), (5, -1)],
)
def test_reject_non_positive_operands(a, b):
    with pytest.raises(ValueError):
        add(a, b)


@pytest.mark.parametrize(
    "a,b",
    [(2.5, 3), ("2", 3), (True, 3)],
)
def test_reject_non_integer_operands(a, b):
    with pytest.raises(ValueError):
        add(a, b)


def test_invalid_operation():
    with pytest.raises(ValueError):
        calculate("divide", 10, 5)


def test_lambda_handler_success():
    response = lambda_handler(
        {
            "body": json.dumps({
                "operation": "multiply",
                "a": 6,
                "b": 7,
            })
        },
        None,
    )

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"result": 42}


def test_lambda_handler_invalid_input():
    response = lambda_handler(
        {
            "body": json.dumps({
                "operation": "add",
                "a": 0,
                "b": 5,
            })
        },
        None,
    )

    assert response["statusCode"] == 400
