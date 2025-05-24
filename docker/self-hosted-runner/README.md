1. Build image
    ```
    docker build -t self-hosted-runner:latest . -f ./docker/self-hosted-runner/Dockerfile
    ```
1. Obtain short-live token of your self-hosted runner
  1. Go to your github respository -> Settings -> Actions -> Runners -> New self-hosted runner
  1. You can find token in code snipet `Configure`
1. If you use KinD, please modify server url and tls configuration of kubeconifg.yaml for being accessible inside a container
    ```
    sed '
      s/certificate-authority-data:.*/insecure-skip-tls-verify: true/
      s|server: https://127\.0\.0\.1:\(.*\)|server: https://host.docker.internal:\1|
      ' <PATH/TO/ORIGINAL_KUBECONFIG> > <PATH/TO/KUBECONFIG>
    ```
1. Run
    ```
    RUNNER_REPOSITORY_URL=https://github.com/your-org/your-app
    RUNNER_TOKEN=<runner token>
    docker run -d --rm --name runner \
      -e RUNNER_REPOSITORY_URL=$RUNNER_REPOSITORY_URL \
      -e RUNNER_TOKEN=$RUNNER_TOKEN \
      --mount type=bind,src=<ABSOLUTE_PATH/TO/KUBECONFIG>,dst=/home/runner/kubeconfig.yaml \
      self-hosted-runner:latest
    ```