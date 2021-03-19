from behave import *
from requests import post
from json import loads


@when(u'I submit the JSON')
def step_impl(context):
    context.api_request = post(context.base_url, json=loads(context.text))


@then(u'the API returns the http status code {status_code:d}')
def step_impl(context, status_code):
    assert context.api_request.status_code == status_code
