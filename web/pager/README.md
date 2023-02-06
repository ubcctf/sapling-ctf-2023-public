# pager

## Notes

The `docker-compose` throws up a reverse proxy along with the service and uses volumes. It can be used for testing.

The `Dockerfile` is for kctf and assumes you have a load balancer rewriting the host header in front.

## Architecture

Backend nginx server with 2 vhosts:

* `frontend` which serves the public files.
* `processor` which does the processing and is inaccessible publicly.

The `frontend` vhost contains a PHP page in which users can send specific PHP to the `processor` vhost to have executed.

To restrict access to the `processor` vhost, an nginx reverse proxy is placed in front of the aforementioned nginx server that rewrites the `Host` header. `keepalive` is required for proxy to keep connection open and execute smuggled request

## Purpose

The webapp is designed to be an ancient apartment intercom that allows you to "ping" to check if people are online and "page" to send a message. I just tried to come up with something that goes around the exploit :^)

## Exploit

A request smuggling vulnerability in the backend server running nginx 1.17.6 allows a request to pass through the proxy as the data portion of a request but be interpreted by the backend server as 2 requests. As such it's `Host` header is not rewritten and it can access the `processor` vhost allowing for arbitrary PHP execution.

Example solution at [`solve/solution.py`](solve/solution.py).
