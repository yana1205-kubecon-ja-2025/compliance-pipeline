#!/bin/bash

{
  echo -e "NAME\tPORTS\tSSL_REDIRECT"
  kubectl get ingress -o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{if .spec.tls}}443{{else}}80{{end}}{{"\t"}}{{if index .metadata.annotations "nginx.ingress.kubernetes.io/force-ssl-redirect"}}{{index .metadata.annotations "nginx.ingress.kubernetes.io/force-ssl-redirect"}}{{else}}null{{end}}{{"\n"}}{{end}}' \
  | sed 's/,*$//'
} | column -s $'\t' -t