# py_corrector_docker

A Flask HTTP endpoint backed by `pycorrector.MacBertCorrector`.
Run the existing service with `docker compose up --build`.

## HTTP dependency verification

`requirements-http.txt` owns the Flask/Werkzeug pins and is included by the full
`requirements.txt`. Keep both updated to patched, mature releases.

```sh
python -m pip install -r requirements-http.txt
python -m unittest discover -s tests -v
```

The HTTP regression tests use the real Flask request/JSON layer and a simulated
correction model. They cover the Chinese JSON response shape, missing and malformed
input, method restrictions, and the Flask JSON-provider API. They do not download
model weights, validate correction quality, or claim production deployment.

The existing Docker image remains Python 3.9 for this bounded HTTP security fix;
modernizing the ML runtime requires a separate full-model compatibility check.
