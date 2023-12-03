# hallucinations-eidf

```bash
$ pip install -U -r requirements.txt
$ kubectl create secret generic hl-secrets --from-literal=hf-token=...
$ python launch-cli.py sample.yml
```

To check the status of an ongoing job:

```bash
$ kubectl logs job/<job name>
```
