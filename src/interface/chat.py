"""
Chat UI using Gradio Blocks.
Blocks preferred for "lower-level" layout control and state management.
TODOs:

"""

import gradio as gr
import interface.utils

with gr.Blocks() as chatUI:
    # gr.State()
    
    with gr.Row():
        modelSelect = gr.Dropdown(
            label = "Model selection:",
            scale = 0.5,
        )
    
    with gr.Row():
        chatOutput = gr.Chatbot(
            bubble_full_width = False,
            scale = 2
        )
        agentWhiteBoard = gr.Markdown(scale = 1)
        
    with gr.Row():
        queryInput = gr.Textbox(
            placeholder = "Please enter you question or request here...",
            show_label = False,
            scale = 4,
        )
        submitButton = gr.Button("Submit", scale = 1)
        
    with gr.Row():
        fileUpload = gr.File(
            height = 100,
        )
        retryButton = gr.Button("Retry")
        clearButton = gr.ClearButton([queryInput, chatOutput])
    
    with gr.Row():
        with gr.Accordion(label = "Expand for edit system prompt:"):
            systemPrompt = gr.Textbox(
                value = "System prompt here (null)",
                show_label = False,
                lines = 4,
                scale = 4,
        )
    

    """
    Event functions
    
    """
    queryInput.submit(
        fn = query_submit,
        inputs = [queryInput, chatOutput],
        outputs = [queryInput, chatOutput],
        queue = False,
    ).then(
        fn = query_completion,
        inputs = [queryInput, chatOutput],
        outputs = [chatOutput],
    )
    
    submitButton.click(
        fn = query_submit,
        inputs = [queryInput, chatOutput],
        outputs = [queryInput, chatOutput],
        queue = False,
    ).then(
        fn = query_completion,
        inputs = [queryInput, chatOutput],
        outputs = [chatOutput],
    )

    retryButton.click(
        fn = retry_query,
        inputs = [chatOutput],
        outputs = [chatOutput],
    )