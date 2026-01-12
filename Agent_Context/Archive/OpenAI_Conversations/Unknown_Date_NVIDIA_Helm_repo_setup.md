# NVIDIA Helm repo setup

**Date | Дата:** Unknown_Date 00:00:00

**ID:** 6931716b-8118-832f-814c-70dd45666c37

---

**👤 User | Пользователь:**

nvidia helm repo


**🤖 Assistant | Ассистент:**

Do you mean NVIDIA GPU Operator / more broadly NVIDIA’s “Helm repo”? Here’s how to add the official NVIDIA Helm repo (for GPU-Operator, NIM, etc.): 
✅ How to add the NVIDIA Helm repo

For GPU Operator:

bash
Копировать код
helm repo add nvidia https://nvidia.github.io/gpu-operator
helm repo update


Then you can install the chart for example with:

bash
Копировать код
helm install --wait --generate-name -n gpu-operator --create-namespace nvidia/gpu-operator
``` :contentReference[oaicite:2]{index=2}

- For other NVIDIA charts (e.g. NIM / NeMo / NIM-LLM / RAG / microservices), there are different Helm repos under NVIDIA’s NGC catalog, e.g.:

```bash
helm repo add nmp https://helm.ngc.nvidia.com/nvidia/nemo-microservices --username='$oauthtoken' --password=$NGC_API_KEY
helm repo update
``` :contentReference[oaicite:3]{index=3}

And for deploying a NIM for LLMs:  
```bash
helm fetch https://helm.ngc.nvidia.com/nim/charts/nim-llm-<version>.tgz --username='$oauthtoken' --password=$NGC_API_KEY
``` :contentReference[oaicite:4]{index=4}

### 🧑‍💻 Which repo to use when

 Use-case 

