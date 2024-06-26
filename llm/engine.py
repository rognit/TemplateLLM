import json
import regex as re
from math import exp
from openai import OpenAI
from llm.config import *
from llm.tools import light_grey, redlog


def llama3v2_prompt_format(prompt, assistant_prefix):
    return f"{"".join(
        [f"<|start_header_id|>{speech['role']}<|end_header_id|>\n\n{speech['content']}<|eot_id|>" for speech in prompt]
    )}<|start_header_id|>assistant<|end_header_id|>\n\n{assistant_prefix}"


def mistral_prompt_format(prompt, assistant_prefix):
    return f"{"".join(
        [f"[INST]{speech['content']}[/INST]" if speech['role'] == 'user' else speech['content'] for speech in prompt]
    )}{assistant_prefix}"


def compute_perplexity(log_prob_list):
    cross_entropy = -sum(log_prob_list) / len(log_prob_list)
    return exp(cross_entropy) if cross_entropy < 690 else 1e+300


def extract_json(text):
    json_regex = r'\{(?:[^{}[\]]|(?R))*\}|\[(?:[^[\]{}]|(?R))*\]'
    matches = re.findall(json_regex, text)
    jsons = []
    for match in matches:
        try:
            jsons.append(json.loads(match))
        except json.JSONDecodeError:
            pass
    match len(jsons):
        case 0:
            redlog("No Json")
        case 1:
            return jsons[0]
        case _:
            redlog("Several Jsons")


def chat(messages,
         top_p=0.95,
         temperature=0,
         max_tokens=4096,
         perplexity=False,
         json_format=False,
         assistant_prefix='',
         model=MODEL,
         stream=VERBOSE):

    local_model = model in LOCAL_MODELS

    perplexity = False if local_model else perplexity
    assistant_prefix = '' if not local_model else assistant_prefix
    response_format = {'type': 'json_object'} if json_format else {'type': 'text'}

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed") if local_model \
        else OpenAI(api_key=OPENAI_API_KEY)

    if assistant_prefix:
        prompt = llama3v2_prompt_format(messages, assistant_prefix) if model == 'llama3' \
            else mistral_prompt_format(messages, assistant_prefix) if model == 'mistral' else None
        completion = client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            stream=stream,
            max_tokens=max_tokens,
            top_p=top_p,
        )

    else:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            logprobs=perplexity,
            max_tokens=max_tokens,
            response_format=response_format,
            top_p=top_p,
        )

    if stream:
        token_list, logprob_list = [], []
        for chunk in completion:
            choice = chunk.choices[0]
            if perplexity and choice.logprobs and choice.logprobs.content:
                logprob_list.append(choice.logprobs.content[0].logprob)
            token = choice.text if assistant_prefix else choice.delta.content
            if token:
                print(light_grey(token), end="", flush=True)
                token_list.append(token)
        print()
        output = ''.join(token_list)

    else:
        output = completion.choices[0].text if assistant_prefix else completion.choices[0].message.content
        logprob_list = [tok.logprob for tok in completion.choices[0].logprobs.content] if perplexity else []

    output = extract_json(output) if response_format['type'] == 'json_object' else output
    output = (output, compute_perplexity(logprob_list)) if perplexity else output

    return output
