

## Component: Managed Kubernetes


#### Result of control sc-13: 



Rule `require-tls-on-ingress (Kyverno)`:
- Checks that all Ingress resources are configured to use TLS for secure communication by Kyverno

<details><summary>Details</summary>


  - Subject UUID: 3e9a567f-1d1e-4a36-9907-bdf4d81f4ae8
    - Title: networking.k8s.io/v1/Ingress good-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```


  - Subject UUID: 19c1dfc6-c064-4f6e-83d7-c6f5cc66826e
    - Title: networking.k8s.io/v1/Ingress bad-application default
    - Result: failure :x:
    - Reason:
      ```
      validation error: Ingress must have TLS configured (hosts or secretName). rule require-tls[0] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/ rule require-tls[1] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/
      ```

</details>


---

