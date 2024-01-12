import os
from huggingface_hub import InferenceClient
import gradio as gr

"""
Chat engine.
TODOs:
- Better prompts.
- Output reader / parser.
- Agents for evaluation and task planning / splitting.
    * Haystack for orchestration
- Tools for agents
    * Haystack for orchestration
- 
"""

selected_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

client = InferenceClient(selected_model)

def format_prompt(query, history, lookback):
    prompt = "Responses should be no more than 100 words long.\n"
    
    for previous_query, prevous_completion in history[-lookback:]:
        prompt += f"<s>[INST] {previous_query} [/INST] {prevous_completion}</s> "
    
    prompt += f"[INST] {query} [/INST]"
  
    return prompt
    
def query_submit(user_message, history):
    return "", history + [[user_message, None]]

def query_completion(
    query,
    history,
    lookback = 3,
    max_new_tokens = 256,
):

    generateKwargs = dict(
        max_new_tokens = max_new_tokens,
        seed = 1337,
    )

    formatted_query = format_prompt(query, history, lookback)
    
    stream = client.text_generation(
        formatted_query,
        **generateKwargs,
        stream = True,
        details = True,
        return_full_text = False
    )
    
    history[-1][1] = ""
    
    for response in stream:
        history[-1][1] += response.token.text
        yield history

def retry_query(
    history,
    lookback = 3,
    max_new_tokens = 256,
):
    if not history:
        pass
    
    else:
        query = history[-1][0]
        history[-1][1]  = None
        
        generateKwargs = dict(
            max_new_tokens = max_new_tokens,
            seed = 1337,
        )
        
        formatted_query = format_prompt(query, history, lookback)
        
        stream = client.text_generation(
            formatted_query,
            **generateKwargs,
            stream = True,
            details = True,
            return_full_text = False
        )
        
        history[-1][1] = ""
        
        for response in stream:
            history[-1][1] += response.token.text
            yield history