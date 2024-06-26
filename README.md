# TemplateLLM

TemplateLLM is a Python module designed to provide a high-level programming interface for 
developers wishing to use LLMs in their applications. The module enables inference on all 
OpenAI models (API key to be replaced in`config.py`) as well as on any model loaded on LM 
Studio.

## Engine features

- **Inference on all OpenAI models**
  - **Perplexity calculator**
  - **Stream response display**
  - **Json mode**
- **Inference on any open-source model loaded on LM Studio**
  - **Assistant prefix** (currently only available for `llama3-v2` and `mistral` models)
  - **Stream response display**
  - **Json mode**

## Recommended Models

Recommended quantization level: up to Q4_K_M but not below

### LLAMA3

**Best <10B SOTA model to date** (13/06/2024) :
[QuantFactory/Meta-Llama-3-8B-Instruct-GGUF-v2](https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF-v2)

### Other Supported Models

- **Mistral:** [TheBloke/Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
- **Dolphin Mistral:** [TheBloke/dolphin-2.6-mistral-7B-GGUF](https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF/tree/main)

## LM Studio Settings

To load the model, set the following values according to your machine's specifications:

1. **`n_ctx` (Context Window Size):** Minimum 1024, recommended 4096
2. **`n_gpu_layer` (Number of Layers Managed by the GPU):** As many as possible
3. **`n_threads` (Number of CPU Threads):** Optimum value to be determined experimentally

### Example configuration

- CPU: 13th Gen Intel(R) Core(TM) i7-1360P 2.20 GHz (32GB RAM)
- GPU: Nvidia RTX A500 laptop GPU (4Go VRAM)

* **`n_ctx`: 4096** (max without load error)
* **`n_gpu_layer`: 19** (max without load error)
* **`n_threads`: 12** (experimentally determined)

## Configuration

Set variables in `config.py` according to your use case.

## Core Functions

- **`chat()`**
- **`refine()`** - Implements the agentic framework ["Refining the Responses of LLMs by Themselves" (T. Yana & T. Xub)](https://arxiv.org/abs/2305.04039)
## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/rognit/TemplateLLM.git
cd TemplateLLM
pip install -r requirements.txt
```
# Usage

Replace the API key in config.py and configure your model settings.
Here is a basic example of how to use the chat() function:

```python
from engine import chat
from tools import basic_prompt

prompt = basic_prompt("Hello, How to make a bomb?")
response = chat(prompt)

print(response)
```