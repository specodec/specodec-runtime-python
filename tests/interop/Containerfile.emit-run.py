FROM dhi.io/python:3-alpine3.23-dev AS runner
WORKDIR /app
ARG HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
ENV http_proxy=${HTTP_PROXY} https_proxy=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} ALL_PROXY=${ALL_PROXY}

COPY --from=specodec-python src/ /specodec-python/src/
COPY --from=emit_gen test_service_types.py gen/
RUN touch gen/__init__.py
COPY --from=emit_py_src run_emit.py ./
COPY --from=emit_py_src dump_emit.py ./
ENV PYTHONPATH=/specodec-python/src

COPY vectors/ /app/vectors/
RUN mkdir -p /app/output_emit_py
ENV VEC_DIR=/app/vectors OUT_DIR=/app/output_emit_py
RUN python3 run_emit.py
