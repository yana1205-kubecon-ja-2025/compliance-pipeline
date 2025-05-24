FROM ghcr.io/actions/actions-runner:2.324.0

USER root

# Install kubectl (arch-independent)
ENV KUBECTL_VERSION=v1.30.1
RUN ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') && \
    curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl
RUN apt update && apt install -y python3-pip

COPY docker/self-hosted-runner/entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh
RUN mkdir /etc/compliance-pipeline
COPY pyproject.toml /etc/compliance-pipeline/pyproject.toml
COPY compliance_pipeline /etc/compliance-pipeline/compliance_pipeline
RUN cd /etc/compliance-pipeline && \
    pip3 install -e .
USER runner

ENTRYPOINT ["/etc/entrypoint.sh"]