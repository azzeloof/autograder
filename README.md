# AutoGrader

[![Client CI](https://github.com/azzeloof/autograder/actions/workflows/client-ci.yml/badge.svg)](https://github.com/azzeloof/autograder/actions/workflows/client-ci.yml)

This project is a Python-based autograding system consisting of a client and a server. The system allows students to check their code's outputs against instructor-provided functions without having access to the underlying test code.

## Overview

The autograder system is composed of two main parts:

*   **Server:** A Django-based server that hosts the grading functions and provides an API for evaluating student code. Instructors can add and manage assignments and test functions through the Django admin interface.
*   **Client:** A Python client that allows students to send their answers to the server for evaluation. The client provides a simple and intuitive interface for interacting with the autograder.

## How It Works

1.  **Instructors** define assignments and test functions using the Django admin interface on the server. They can specify allowed libraries and the code for each test function.
2.  **Students** use the Python client to connect to the server and call the test functions with their code as arguments.
3.  The **server** receives the student's answer, evaluats it against a given function in a restricted environment, and returns the result to the client.
4.  The **client** handles the interface between the student and the server.

## For More Information

For detailed instructions on how to set up and use the client and server, please refer to the `README.md` files in their respective directories:

*   [Client README](./client-src/README.md)
*   [Server README](./server-src/README.md)
