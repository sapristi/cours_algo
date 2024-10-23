from django.shortcuts import render
from django.http import HttpResponse
from recorder.models import Record


def record(request, *args, **kwargs):
    scheme = request.scheme
    method = request.method
    path = request.path
    parameters = request.GET
    body = request.body
    headers = request.headers
    record = Record(
        scheme=scheme,
        method=method,
        path=path,
        parameters=dict(parameters),
        body=body,
        headers=dict(headers)
    )

    if Record.objects.count() > 100:
        Record.objects.first().delete()
    record.save()
    print(f"Saved new record: {record}")
    return HttpResponse(status=200, content=f"request recorded ({record})".encode())
