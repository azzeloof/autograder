# Autograder Client

This package provides a Python client for an autograder server. It allows students to check their answers against functions hosted on a server, without being able to inspect the functions themselves.

## How it works

The client uses a dynamic interface to send the output from a student's to the autograder server. The server then evaluates the results and returns the result.

The `Autograder` class is the main entry point for the client. It takes the URL of the autograder server as an argument. When a student accesses an attribute of an `Autograder` instance, it returns an `Assignment` instance. When a student calls a method on an `Assignment` instance, the client sends a POST request to the autograder server with the assignment name, function name, and arguments. The server then evaluates the function (already provided on the server by an instructor) and returns the result.

## Installation

```bash
pip install .
```

## Usage

Here is an example of how to use the client:

```python
from autograder_client import Autograder

# Create an Autograder instance
a = Autograder(url="http://localhost:8000/evaluate") # url is optional

# Call a function on the "Week1" assignment
result = a.Week1.foo(68)

# Print the result
print(result)
```

In this example, the client sends a POST request to the autograder server with the following payload:

```json
{
    "assignment": "Week1",
    "function": "foo",
    "args": [68],
    "kwargs": {}
}
```

The server then evaluates the `foo` function from the `Week1` assignment with the argument `68` and returns the result.
