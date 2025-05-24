

## Component: Managed Kubernetes


#### Result of control sc-13: 



Rule `require-tls-on-ingress (Kyverno)`:
- Checks that all Ingress resources are configured to use TLS for secure communication by Kyverno

<details><summary>Details</summary>


  - Subject UUID: 7efaabe9-ac2d-417d-b267-4d5ad65ccf02
    - Title: networking.k8s.io/v1/Ingress bad-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```


  - Subject UUID: 4d58fe66-de7b-467a-92f0-06bb728d553d
    - Title: networking.k8s.io/v1/Ingress good-application default
    - Result: pass :white_check_mark:
    - Reason:
      ```
      validation rule 'require-tls' anyPattern[1] passed.
      ```

</details>


---

