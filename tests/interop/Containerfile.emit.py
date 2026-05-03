FROM dhi.io/python:3-alpine3.23-dev AS runner
WORKDIR /app
ARG HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
ENV http_proxy=${HTTP_PROXY} https_proxy=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} ALL_PROXY=${ALL_PROXY}

COPY --from=specodec-python src/ /specodec-python/src/
COPY --from=emit_gen test_service_types.py gen/
RUN touch gen/__init__.py
ENV PYTHONPATH=/specodec-python/src
RUN python3 -c "from gen.test_service_types import *; print('OK py')"
