

## Component: Managed Kubernetes


#### Result of control sc-13: 



Rule `require-tls-on-ingress (Kyverno)`:
- Checks that all Ingress resources are configured to use TLS for secure communication by Kyverno

<details><summary>Details</summary>


  - Subject UUID: 8388b603-1205-4d1f-9410-578dacd3e244
    - Title: networking.k8s.io/v1/Ingress good-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```


  - Subject UUID: 46fb8d22-02dd-46fe-a70e-402a94a063a1
    - Title: networking.k8s.io/v1/Ingress bad-application default
    - Result: failure :x:
    - Reason:
      ```
      validation error: Ingress must have TLS configured (hosts or secretName). rule require-tls[0] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/ rule require-tls[1] failed at path /metadata/annotations/nginx.ingress.kubernetes.io/force-ssl-redirect/
      ```

</details>


---

