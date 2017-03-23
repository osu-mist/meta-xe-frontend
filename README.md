Meta XE Frontend
====

This app provides a frontend to the [Meta XE API][meta-xe-api].

[meta-xe-api]: https://github.com/osu-mist/meta-xe-api

Installation
----

    % git clone https://github.com/osu-mist/meta-xe-frontend.git
    % cd meta-xe-frontend
    % virtualenv .
    % bin/pip install -e .

### Dependencies

See [setup.py](setup.py#L11).

Configuration
----

    SECRET_KEY

        This key protects the app's session cookies.
        You should set it to a suitably random string.

            python -c 'print repr(open("/dev/random").read(32))'


    TOKEN_ENDPOINT

        The URL of the OAuth2 token endpoint.
        Example: https://api.oregonstate.edu/oauth2/token

    API_ENDPOINT

        The URL of the Meta XE API endpoint.
        Example: https://api.oregonstate.edu/v1/xeapps

    CLIENT_ID

        Your client ID for the OSU developer APIs.

    CLIENT_SECRET

        Your client secret for the OSU developer APIs.

Running
----

    % METAXE_CONFIG=../config.py bin/python -m metaxe

This runs the meta xe app in debug mode.
For deploying in production, use gunicorn or another WSGI server.

Docker
----

Build a docker image with

    # docker build --tag=metaxe .

Run the image with

    # docker run --publish 5000:8000 --volume $PWD/config.py:/src/config.py:ro metaxe

where 5000 is the port you want to listen on
and $PWD/config.py is the (absolute) path to your config file.
