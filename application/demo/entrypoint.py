from flask import Flask, render_template, abort, Blueprint, make_response, url_for

demo_entrypoint = Blueprint("demo_page", __name__, url_prefix='/demo')


@demo_entrypoint.route("")
def demo_main():
    return "Hello Root"


@demo_entrypoint.route("/test")
def demo_page():
    return "This is /demo/test"
