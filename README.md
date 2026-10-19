# v4-hello-world

Minimal Hello World app used to test the Shakudo V4
Git Repository -> Microservice integration.

- `GET /`         -> Hello World page (marker: id="hello-heading")
- `GET /healthz`  -> {"status":"ok"}
- `GET /version`  -> JSON incl. git revision

Run: `./run.sh`   (listens on 0.0.0.0:8787)
