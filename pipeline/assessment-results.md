

## Component: Managed Kubernetes


#### Result of control sc-13: 



Rule `require-tls-on-ingress (Kyverno)`:
- Checks that all Ingress resources are configured to use TLS for secure communication by Kyverno

<details><summary>Details</summary>


  - Subject UUID: a1e69e45-d647-4b7a-9717-5068710bae7c
    - Title: networking.k8s.io/v1/Ingress good-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```


  - Subject UUID: 0ac4070e-fddf-4a97-89d6-740ca2e83b76
    - Title: networking.k8s.io/v1/Ingress bad-application default
    - Result: failure :x:
    - Reason:
      ```
      validation error: Ingress must have TLS configured (hosts or secretName). rule require-tls[0] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/ rule require-tls[1] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/
      ```

</details>


---

