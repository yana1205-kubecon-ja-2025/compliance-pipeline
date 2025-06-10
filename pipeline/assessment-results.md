

## Component: Managed Kubernetes


#### Result of control sc-13: 



Rule `require-tls-on-ingress (Kyverno)`:
- Checks that all Ingress resources are configured to use TLS for secure communication by Kyverno

<details><summary>Details</summary>


  - Subject UUID: a70647a4-0888-489e-aa7c-d9f9582ad52a
    - Title: networking.k8s.io/v1/Ingress bad-application default
    - Result: failure :x:
    - Reason:
      ```
      validation error: Ingress must have TLS configured (hosts or secretName). rule require-tls[0] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/ rule require-tls[1] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/
      ```


  - Subject UUID: 269761e8-c768-41ca-8580-61ab5620b5b8
    - Title: networking.k8s.io/v1/Ingress good-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```

</details>


---

