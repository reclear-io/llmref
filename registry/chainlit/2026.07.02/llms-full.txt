# Ask User
Source: https://docs.chainlit.io/advanced-features/ask-user



The ask APIs prompt the user for input. Depending on the API, the user input can be a string, a file, pick an action or fill a form.

Until the user provides an input, both the UI and your code will be blocked.

<Frame>
  <img />
</Frame>

## Available Ask APIs

<CardGroup>
  <Card title="Text Input" icon="text" href="/api-reference/ask/ask-for-input">
    Ask the user for a string input.
  </Card>

  <Card title="File" icon="file" href="/api-reference/ask/ask-for-file">
    Ask the user to upload a file.
  </Card>

  <Card title="Action" icon="bolt" href="/api-reference/ask/ask-for-action">
    Ask the user to pick an action.
  </Card>

  <Card title="Element" icon="square-check" href="/api-reference/ask/ask-for-element">
    Ask the user to complete a custom form.
  </Card>
</CardGroup>

## Interactive Consent-Gated Forms

The `AskElementMessage` API enables agents to send interactive, consent-gated UI components to users. This feature is particularly useful for:

* **Compliance workflows** where explicit user consent is required
* **Data review** scenarios where users need to review and modify AI-generated data
* **Form completion** with pre-filled values for user confirmation
* **Audit trails** for sensitive operations

The flow works as follows:

1. **Agent** calls a consent-gated tool (e.g., expense logging API)
2. Backend sends a **CustomElement** to the frontend with editable fields and timeout
3. **User** modifies or confirms the pre-filled values and submits
4. Backend receives the **updated props** and proceeds with the tool call using user-approved data

This pattern blocks further chat interactions until user input is received, preventing ambiguous or unauthorized actions.

<Frame>
  <img />
</Frame>


# Chat Profiles
Source: https://docs.chainlit.io/advanced-features/chat-profiles



Chat Profiles are useful if you want to let your users choose from a list of predefined configured assistants. For example, you can define a chat profile for a support chat, a sales chat, or a chat for a specific product.

<Card title="Chat Profiles API" icon="comments" href="/api-reference/chat-profiles">
  Learn how to define chat profiles.
</Card>

<Frame>
  <img />
</Frame>


# Chat Settings
Source: https://docs.chainlit.io/advanced-features/chat-settings



Chat settings are useful to let each user configure their chat experience given a set of options.

## How it works

Check the chat settings [API reference](/api-reference/chat-settings) to learn how to configure it.

## Preview

If chat settings are set, a new button will appear in the chat bar.

<img alt="OpenChatSettings" />

Clicking on this button will open the settings panel. All settings are editable by the user. Once settings are updated, an event is sent to the Chainlit server so the application can react to the update.

<Frame>
  <img />
</Frame>

## Example

Check out this example from the cookbook that uses this feature: [https://github.com/Chainlit/cookbook/tree/main/image-gen](https://github.com/Chainlit/cookbook/tree/main/image-gen)


# MCP
Source: https://docs.chainlit.io/advanced-features/mcp

Model Control Protocol (MCP) allows you to integrate external tool providers with your Chainlit application. This enables your AI models to use tools through standardized interfaces.

## Overview

MCP provides a mechanism for Chainlit applications to connect to either server-sent events (SSE) or streamable HTTP based services, or command-line (stdio) based tools. Once connected, your application can discover available tools, execute them, and integrate their responses into your application's flow.

<Card title="Chainlit MCP Cookbook" icon="github" href="https://github.com/Chainlit/cookbook/tree/main/mcp">
  End to end cookbook example showcasing MCP tool calling with Claude.
</Card>

<Frame>
  <video />
</Frame>

### Contact us for Enterprise Ready MCP

We're working with companies to create their MCP stacks, enabling AI agents to consume their data and context in standardized ways. Fill out this [form](https://docs.google.com/forms/d/e/1FAIpQLSdObSIeIFt4nHppZ6r2rIoEe-jZRo4CqxbmRKKgb-ZsSPONnQ/viewform?usp=dialog).

## Connections Types

| WebSockets | HTTP+SSE | Streamable HTTP | stdio |
| ---------- | -------- | --------------- | ----- |
| ❌          | ✅        | ✅               | ✅     |

Chainlit supports three types of MCP connections:

1. **SSE (Server-Sent Events)**: Connect to a remote service via HTTP
2. **Streamable HTTP**: Send HTTP requests to a server and receive JSON responses or connect using SSE streams
3. **stdio**: Execute a local command and communicate via standard I/O

> ⚠️ **Security Warning**: The stdio connection type spawns actual subprocesses on the Chainlit server. Only use this with trusted commands in controlled environments. Ensure proper validation of user inputs to prevent command injection vulnerabilities.

<Note>**Command Availability Warning**: When using the stdio connection type with commands like `npx` or `uvx`, these commands must be available on the Chainlit server where the application is running. The subprocess is executed on the server, not on the client machine.</Note>

### Server-Side Configuration (`config.toml`)

You can control which MCP connection types are enabled globally and restrict allowed stdio commands by modifying your project's `config.toml` file (usually located at the root of your project or `.chainlit/config.toml`).

Under the `[features.mcp]` section, you can configure SSE, Streamable HTTP and stdio separately:

<Warning>
  Since Chainlit 2.7.0, `mcp.enabled` must be explicitly set to `true` in `config.toml`. It is no longer auto-inferred from the existence of an `on_mcp_connect` callback.
</Warning>

```toml theme={null}
[features]
# ... other feature flags

[features.mcp]
    # Enable or disable MCP features globally
    enabled = false

[features.mcp.sse]
    # Enable or disable the SSE connection type globally
    enabled = true

[features.mcp.streamable-http]
    # Enable or disable the Streamable HTTP connection type globally
    enabled = true

[features.mcp.stdio]
    # Enable or disable the stdio connection type globally
    enabled = true
    # Define an allowlist of executables for the stdio type.
    # Only the base names of executables listed here can be used.
    # This is a crucial security measure for stdio connections.
    # Example: allows running `npx ...` and `uvx ...` but blocks others.
    allowed_executables = [ "npx", "uvx" ]
```

## Setup

### 1. Register Connection Handlers

To use MCP in your Chainlit application, you need to implement the `on_mcp_connect` handler. The `on_mcp_disconnect` handler is optional but recommended for proper cleanup.

```python theme={null}
import chainlit as cl
from mcp import ClientSession

@cl.on_mcp_connect
async def on_mcp_connect(connection, session: ClientSession):
    """Called when an MCP connection is established"""
    # Your connection initialization code here
    # This handler is required for MCP to work
    
@cl.on_mcp_disconnect
async def on_mcp_disconnect(name: str, session: ClientSession):
    """Called when an MCP connection is terminated"""
    # Your cleanup code here
    # This handler is optional
```

### 2. Client Configuration

The client needs to provide the connection details through the Chainlit interface. This includes:

* Connection name (unique identifier)
* Client type (`sse`, `streamable-http` or `stdio`)
* For SSE and Streamable HTTP: URL endpoint
* For stdio: Full command (e.g., `npx your-tool-package` or `uvx your-tool-package`)

<Frame>
  <img />
</Frame>

## Working with MCP Connections

### Retrieving Available Tools

Upon connection, you can discover the available tools provided by the MCP service:

```python theme={null}
@cl.on_mcp_connect
async def on_mcp(connection, session: ClientSession):
    # List available tools
    result = await session.list_tools()
    
    # Process tool metadata
    tools = [{
        "name": t.name,
        "description": t.description,
        "input_schema": t.inputSchema,
    } for t in result.tools]
    
    # Store tools for later use
    mcp_tools = cl.user_session.get("mcp_tools", {})
    mcp_tools[connection.name] = tools
    cl.user_session.set("mcp_tools", mcp_tools)
```

### Executing Tools

You can execute tools using the MCP session:

```python theme={null}
@cl.step(type="tool") 
async def call_tool(tool_use):
    tool_name = tool_use.name
    tool_input = tool_use.input
    
    # Find appropriate MCP connection for this tool
    mcp_name = find_mcp_for_tool(tool_name)
    
    # Get the MCP session
    mcp_session, _ = cl.context.session.mcp_sessions.get(mcp_name)
    
    # Call the tool
    result = await mcp_session.call_tool(tool_name, tool_input)
    
    return result
```

## Integrating with LLMs

MCP tools can be seamlessly integrated with LLMs that support tool calling:

```python theme={null}
async def call_model_with_tools():
    # Get tools from all MCP connections
    mcp_tools = cl.user_session.get("mcp_tools", {})
    all_tools = [tool for connection_tools in mcp_tools.values() for tool in connection_tools]
    
    # Call your LLM with the tools
    response = await your_llm_client.call(
        messages=messages,
        tools=all_tools
    )
    
    # Handle tool calls if needed
    if response.has_tool_calls():
        # Process tool calls
        pass
        
    return response
```

## Session Management

MCP connections are managed at the session level. Each WebSocket session can have multiple named MCP connections. The connections are cleaned up when:

1. The user explicitly disconnects
2. The same connection name is reused (old connection is replaced)
3. The WebSocket session ends


# Multi-Modality
Source: https://docs.chainlit.io/advanced-features/multi-modal



The term 'Multi-Modal' refers to the ability to support more than just text, encompassing images, videos, audio and files.

## Voice Assistant

Chainlit let's you access the user's microphone audio stream and process it in real-time. This can be used to create voice assistants, transcribe audio, or even process audio in real-time.

<Note>
  The user will only be able to use the microphone if you implemented the
  [@cl.on\_audio\_chunk](/api-reference/lifecycle-hooks/on-audio-chunk) decorator.
</Note>

<CardGroup>
  <Card title="OpenAI Realtime" icon="microphone-lines" href="https://github.com/Chainlit/cookbook/tree/main/realtime-assistant">
    Cookbook example showcasing how to use Chainlit with realtime audio APIs.
  </Card>

  <Card title="Text To Speech -> Speech to Text" icon="microphone" href="https://github.com/Chainlit/cookbook/blob/main/openai-whisper/app.py">
    Cookbook example showcasing speech to text -> answer generation -> text to speech.
  </Card>
</CardGroup>

<Frame>
  <video />
</Frame>

## Spontaneous File Uploads

Within the Chainlit application, users have the flexibility to attach any file to their messages. This can be achieved either by utilizing the drag and drop feature or by clicking on the `attach` button located in the chat bar.

<Frame>
  <img />
</Frame>

As a developer, you have the capability to access these attached files through the [cl.on\_message](/api-reference/lifecycle-hooks/on-message) decorated function.

```py theme={null}
import chainlit as cl


@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    await cl.Message(content=f"Received {len(images)} image(s)").send()

```

### Disabling Spontaneous File Uploads

If you wish to disable this feature (which would prevent users from attaching files to their messages), you can do so by setting `features.spontaneous_file_upload.enabled=false` in your Chainlit [config](/backend/config/features) file.


# Streaming
Source: https://docs.chainlit.io/advanced-features/streaming



Chainlit supports streaming for both [Message](/concepts/message) and [Step](/concepts/step). Here is an example with `openai`.

<Frame>
  <img />
</Frame>

```python theme={null}
from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI(api_key="YOUR_OPENAI_API_KEY")


settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
```

## Integrations

Streaming is also supported at a higher level for some integrations.

For example, to use streaming with Langchain just pass `streaming=True` when instantiating the LLM:

```python theme={null}
llm = OpenAI(temperature=0, streaming=True)
```

Also make sure to pass a [callback handler](/api-reference/integrations/langchain) to your chain or agent run.

See [here](/api-reference/integrations/langchain#final-answer-streaming) for final answer streaming.


# Testing & Debugging
Source: https://docs.chainlit.io/advanced-features/test-debug



To test or debug your application files and decorated functions, you will need to provide the Chainlit context to your test suite.

In your main application script or test files add:

```
if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
```

Then run the script from your IDE in debug mode.


# Action
Source: https://docs.chainlit.io/api-reference/action



The `Action` class is designed to create and manage actions to be sent and displayed in the chatbot user interface. Actions consist of buttons that the user can interact with, and these interactions trigger specific functionalities within your app.

## Attributes

<ParamField type="str">
  Name of the action, this should match the action callback.
</ParamField>

<ParamField type="Dict">
  The payload associated with the action.
</ParamField>

<ParamField type="str">
  The lucide icon name for the action button. See [https://lucide.dev/icons/](https://lucide.dev/icons/).
</ParamField>

<ParamField type="str">
  The label of the action. This is what the user will see. If no label and no icon is provided, the name is display as a fallback.
</ParamField>

<ParamField type="str">
  The description of the action. This is what the user will see when they hover
  the action.
</ParamField>

## Usage

```python theme={null}
import chainlit as cl

@cl.action_callback("action_button")
async def on_action(action):
    await cl.Message(content=f"Executed {action.name}").send()
    # Optionally remove the action button from the chatbot user interface
    await action.remove()

@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="action_button", payload={"value": "example_value"}, label="Click me!")
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()
```


# AskActionMessage
Source: https://docs.chainlit.io/api-reference/ask/ask-for-action



Ask for the user to take an action before continuing.
If the user does not answer in time (see timeout), a `TimeoutError` will be raised or `None` will be returned depending on `raise_on_timeout` parameter.
If a project ID is configured, the messages will be uploaded to the cloud storage.

### Attributes

<ParamField type="str">
  The content of the message.
</ParamField>

<ParamField type="List[Action]">
  The list of [Action](/api-reference/action) to prompt the user.
</ParamField>

<ParamField type="str">
  The author of the message, defaults to the chatbot name defined in your
  config.
</ParamField>

<ParamField type="int">
  The number of seconds to wait for an answer before raising a TimeoutError.
</ParamField>

<ParamField type="bool">
  Whether to raise a socketio TimeoutError if the user does not answer in time.
</ParamField>

### Returns

<ResponseField name="response" type="AskActionResponse | None">
  The response of the user.
</ResponseField>

### Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    res = await cl.AskActionMessage(
        content="Pick an action!",
        actions=[
            cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
            cl.Action(name="cancel", payload={"value": "cancel"}, label="❌ Cancel"),
        ],
    ).send()

    if res and res.get("payload").get("value") == "continue":
        await cl.Message(
            content="Continue!",
        ).send()
```


# AskElementMessage
Source: https://docs.chainlit.io/api-reference/ask/ask-for-element



Ask for the user to complete a custom element (fill a form) before continuing.
This allows agents to send interactive, consent-gated UI components to the front end, let users review or edit their values, and submit them back to the backend.

If the user does not answer in time (see timeout), a `TimeoutError` will be raised or `None` will be returned depending on `raise_on_timeout` parameter.
If a project ID is configured, the messages will be uploaded to the cloud storage.

### Attributes

<ParamField type="str">
  The content of the message.
</ParamField>

<ParamField type="CustomElement">
  The [CustomElement](api-reference/elements/custom) to display to the user for interaction.
</ParamField>

<ParamField type="str">
  The author of the message, defaults to the chatbot name defined in your
  config.
</ParamField>

<ParamField type="int">
  The number of seconds to wait for an answer before raising a TimeoutError.
</ParamField>

<ParamField type="bool">
  Whether to raise a socketio TimeoutError if the user does not answer in time.
</ParamField>

### Returns

<ResponseField name="response" type="AskElementResponse | None">
  The response from the user containing the submitted element data.
</ResponseField>

### Example

#### Backend: Ask To Fill Jira Ticket Form

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def on_start():
    element = cl.CustomElement(
        name="JiraTicket",
        display="inline",
        props={
            "timeout": 20,
            "fields": [
                {"id": "summary", "label": "Summary", "type": "text", "required": True},
                {"id": "description", "label": "Description", "type": "textarea"},
                {
                    "id": "due",
                    "label": "Due Date",
                    "type": "date",
                },
                {
                    "id": "priority",
                    "label": "Priority",
                    "type": "select",
                    "options": ["Low", "Medium", "High"],
                    "value": "Medium",
                    "required": True,
                },
            ],
        },
    )
    res = await cl.AskElementMessage(
        content="Create a new Jira ticket:", element=element, timeout=10
    ).send()
    if res and res.get("submitted"):
        await cl.Message(
            content=f"Ticket '{res['summary']}' with priority {res['priority']} submitted"
        ).send()
```

#### Frontend: Jira Ticket Custom Element Implementation

The custom element should be implemented as a React component that handles form submission. Here's an example for the LogExpense component:

```jsx theme={null}
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import React, { useEffect, useMemo, useState } from 'react';

export default function JiraTicket() {
  const [timeLeft, setTimeLeft] = useState(props.timeout || 30);
  const [values, setValues] = useState(() => {
    const init = {};
    (props.fields || []).forEach((f) => {
      init[f.id] = f.value || '';
    });
    return init;
  });

  const allValid = useMemo(() => {
    if (!props.fields) return true;
    return props.fields.every((f) => {
      if (!f.required) return true;
      const val = values[f.id];
      return val !== undefined && val !== '';
    });
  }, [props.fields, values]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeLeft((t) => (t > 0 ? t - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleChange = (id, val) => {
    setValues((v) => ({ ...v, [id]: val }));
  };

  const renderField = (field) => {
    const value = values[field.id];
    switch (field.type) {
      case 'textarea':
        return <Textarea id={field.id} value={value} onChange={(e) => handleChange(field.id, e.target.value)} />;
      case 'select':
        return (
          <Select value={value} onValueChange={(val) => handleChange(field.id, val)}>
            <SelectTrigger id={field.id}>
              <SelectValue placeholder={field.label} />
            </SelectTrigger>
            <SelectContent>
              {field.options.map((opt) => (
                <SelectItem key={opt} value={opt}>
                  {opt}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );
      case 'date':
        return <Input type="date" id={field.id} value={value} onChange={(e) => handleChange(field.id, e.target.value)} />;
      case 'datetime':
        return <Input type="datetime-local" id={field.id} value={value} onChange={(e) => handleChange(field.id, e.target.value)} />;
      default:
        return <Input id={field.id} value={value} onChange={(e) => handleChange(field.id, e.target.value)} />;
    }
  };

  return (
    <Card id="jira-ticket" className="mt-4 w-full max-w-3xl grid grid-cols-2 gap-4">
      <CardHeader className="col-span-2">
        <CardTitle>Create JIRA Ticket</CardTitle>
        <CardDescription>Provide details for the new issue. {timeLeft}s left</CardDescription>
      </CardHeader>
      <CardContent className="col-span-2 grid grid-cols-2 gap-4">
        {props.fields.map((field) => (
          <div key={field.id} className="flex flex-col gap-2">
            <Label htmlFor={field.id}>
              {field.label}
              {field.required && <span className="text-red-500">*</span>}
            </Label>
            {renderField(field)}
          </div>
        ))}
      </CardContent>
      <CardFooter className="col-span-2 flex justify-end gap-2">
        <Button id="ticket-cancel" variant="outline" onClick={() => cancelElement()}>
          Cancel
        </Button>
        <Button
          id="ticket-submit"
          disabled={!allValid}
          onClick={() => submitElement(values)}
        >
          Submit
        </Button>
      </CardFooter>
    </Card>
  );
}
```


# AskFileMessage
Source: https://docs.chainlit.io/api-reference/ask/ask-for-file



Ask the user to upload a file before continuing.
If the user does not answer in time (see timeout), a TimeoutError will be raised or None will be returned depending on raise\_on\_timeout.
If a project ID is configured, the messages will be uploaded to the cloud storage.

### Attributes

<ParamField type="str">
  Text displayed above the upload button.
</ParamField>

<ParamField type="Union[List[str], Dict[str, List[str]]]">
  List of mime type to accept like `["text/csv", "application/pdf"]` or a dict like `{"text/plain": [".txt", ".py"]}`.
  More infos here [https://react-dropzone.org/#!/Accepting%20specific%20file%20types](https://react-dropzone.org/#!/Accepting%20specific%20file%20types).
</ParamField>

<ParamField type="int">
  Maximum file size in MB. Defaults to 2.
</ParamField>

<ParamField type="int">
  Maximum number of files to upload. Defaults to 1. Maximum value is 10.
</ParamField>

<ParamField type="str">
  The author of the message, defaults to the chatbot name defined in your
  config.
</ParamField>

<ParamField type="int">
  The number of seconds to wait for an answer before raising a TimeoutError.
</ParamField>

<ParamField type="bool">
  Whether to raise a socketio TimeoutError if the user does not answer in time.
</ParamField>

### Returns

<ResponseField name="response" type="List[AskFileResponse] | None">
  The files uploaded by the user.
</ResponseField>

### Example

```python Ask for a text file theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["text/plain"]
        ).send()

    text_file = files[0]

    with open(text_file.path, "r", encoding="utf-8") as f:
        text = f.read()

    # Let the user know that the system is ready
    await cl.Message(
        content=f"`{text_file.name}` uploaded, it contains {len(text)} characters!"
    ).send()

```

You can also pass a dict to the `accept` parameter to precise the file extension for each mime type:

```python Ask for a python file theme={null}
import chainlit as cl

file = await cl.AskFileMessage(
        content="Please upload a python file to begin!", accept={"text/plain": [".py"]}
      ).send()
```


# AskUserMessage
Source: https://docs.chainlit.io/api-reference/ask/ask-for-input



Ask for the user input before continuing.
If the user does not answer in time (see timeout), a TimeoutError will be raised or None will be returned depending on raise\_on\_timeout.
If a project ID is configured, the messages will be uploaded to the cloud storage.

### Attributes

<ParamField type="str">
  The content of the message.
</ParamField>

<ParamField type="str">
  The author of the message, defaults to the chatbot name defined in your
  config.
</ParamField>

<ParamField type="int">
  The number of seconds to wait for an answer before raising a TimeoutError.
</ParamField>

<ParamField type="bool">
  Whether to raise a socketio TimeoutError if the user does not answer in time.
</ParamField>

### Returns

<ResponseField name="response" type="StepDict | None">
  The response of the user.
</ResponseField>

### Usage

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
    if res:
        await cl.Message(
            content=f"Your name is: {res['output']}",
        ).send()
```


# author_rename and Message author
Source: https://docs.chainlit.io/api-reference/author-rename



This documentation covers two methods for setting or renaming the author of a message to display more friendly author names in the UI: the `author_rename` decorator and the Message author specification at message creation.

## Method 1: author\_rename

Useful for renaming the author of a message dynamically during the message handling process.

## Parameters

<ParamField type="str">
  The original author name.
</ParamField>

## Returns

<ResponseField name="author" type="str">
  The renamed author
</ResponseField>

## Usage

```python theme={null}
from langchain import OpenAI, LLMMathChain
import chainlit as cl


@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"LLMMathChain": "Albert Einstein", "Chatbot": "Assistant"}
    return rename_dict.get(orig_author, orig_author)


@cl.on_message
async def main(message: cl.Message):
    llm = OpenAI(temperature=0)
    llm_math = LLMMathChain.from_llm(llm=llm)
    res = await llm_math.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(content="Hello").send()
```

## Method 2: Message author

Allows for naming the author of a message at the moment of the message creation.

### Usage

You can specify the author directly when creating a new message object:

```python theme={null}
from langchain import OpenAI, LLMMathChain
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    llm = OpenAI(temperature=0)
    llm_math = LLMMathChain.from_llm(llm=llm)
    res = await llm_math.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Specify the author at message creation
    response_message = cl.Message(content="Hello", author="NewChatBotName")
    await response_message.send()
```


# cache
Source: https://docs.chainlit.io/api-reference/cache



The `cache` decorator is a tool for caching results of resource-intensive calculations or loading processes. It can be conveniently combined with the [file watcher](/backend/command-line) to prevent resource reloading each time the application restarts. This not only saves time, but also enhances overall efficiency.

## Parameters

<ParamField type="Callable">
  The target function whose results need to be cached.
</ParamField>

## Returns

<ResponseField name="cached_value" type="Any">
  The computed value that is stored in the cache after its initial calculation.
</ResponseField>

## Usage

```python theme={null}
import time
import chainlit as cl

@cl.cache
def to_cache():
    time.sleep(5)  # Simulate a time-consuming process
    return "Hello!"

value = to_cache()

@cl.on_message
async def main(message: cl.Message):
    await cl.Message(
        content=value,
    ).send()
```

In this example, the `to_cache` function simulates a time-consuming process that returns a value. By using the `cl.cache` decorator, the result of the function is cached after its first execution. Future calls to the `to_cache` function return the cached value without running the time-consuming process again.


# Chat Profiles
Source: https://docs.chainlit.io/api-reference/chat-profiles



Decorator to define the list of chat profiles.

If authentication is enabled, you can access the user details to create the list of chat profiles conditionally.

The icon is optional.

## Parameters

<ParamField type="User">
  The message coming from the UI.
</ParamField>

## ChatProfile Fields

| Field                  | Type                      | Required | Description                                                         |
| ---------------------- | ------------------------- | -------- | ------------------------------------------------------------------- |
| `name`                 | `str`                     | Yes      | Internal identifier. Stored in `user_session` as `"chat_profile"`.  |
| `markdown_description` | `str`                     | Yes      | Description shown in the profile selector, supports Markdown.       |
| `icon`                 | `str`                     | No       | URL of the profile icon.                                            |
| `display_name`         | `str`                     | No       | User-facing label shown in the UI. Falls back to `name` if omitted. |
| `starters`             | `list[Starter]`           | No       | Starter messages shown when this profile is selected.               |
| `config_overrides`     | `ChainlitConfigOverrides` | No       | Per-profile config overrides.                                       |

## Usage

```python Simple example theme={null}
import chainlit as cl


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
    ]

@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"starting chat using the {chat_profile} chat profile"
    ).send()
```

```python With authentication theme={null}
from typing import Optional

import chainlit as cl


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] != "ADMIN":
        return None

    return [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**, a *1.5T parameter model* trained on 3.5TB of text data.",
            icon="https://picsum.photos/250",
        ),
        cl.ChatProfile(
            name="GPT-5",
            markdown_description="The underlying LLM model is **GPT-5**.",
            icon="https://picsum.photos/200",
        ),
    ]


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    if (username, password) == ("admin", "admin"):
        return cl.User(identifier="admin", metadata={"role": "ADMIN"})
    else:
        return None


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"starting chat with {user.identifier} using the {chat_profile} chat profile"
    ).send()
```

## With Localization

The `@cl.set_chat_profiles` callback accepts an optional `language` parameter, allowing you to return localized chat profile labels and descriptions.

```python With localization theme={null}
import chainlit as cl


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User, language: str):
    if language == "fr":
        return [
            cl.ChatProfile(
                name="GPT-4",
                markdown_description="Le modèle sous-jacent est **GPT-4**.",
                icon="https://picsum.photos/250",
            ),
        ]
    return [
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
    ]
```

## Display Name

Use `display_name` to show a user-friendly label in the UI while keeping a stable internal identifier in `name`. This is useful for localised names or names containing special characters.

```python theme={null}
import chainlit as cl

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="ad_designer",          # internal ID stored in user_session
            display_name="广告设计师",    # shown in the UI
            markdown_description="Profile for ad design tasks.",
        ),
        cl.ChatProfile(
            name="copywriter",
            display_name="Copywriter",
            markdown_description="Profile for writing tasks.",
        ),
    ]

@cl.on_chat_start
async def on_chat_start():
    # user_session always holds the internal `name`, not display_name
    chat_profile = cl.user_session.get("chat_profile")  # "ad_designer"
```

<Note>
  Since version **2.8.5**.
</Note>

## Dynamic Configuration

You can override the global `config.toml` for specific ChatProfiles by configuring overrides

```python theme={null}
from chainlit.config import (
    ChainlitConfigOverrides,
    FeaturesSettings,
    McpFeature,
    UISettings,
)

@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    return [
        cl.ChatProfile(
            name="MCP Enabled",
            markdown_description="Profile with **MCP features enabled**. This profile has *Model Context Protocol* support activated. [Learn more](https://example.com/mcp)",
            icon="https://picsum.photos/250",
            starters=starters,
            config_overrides=ChainlitConfigOverrides(
                ui=UISettings(name="MCP UI"),
                features=FeaturesSettings(
                    mcp=McpFeature(
                        enabled=True,
                        stdio={"enabled": True},
                        sse={"enabled": True},
                        streamable_http={"enabled": True},
                    )
                ),
            ),
        ),
```


# Chat Settings
Source: https://docs.chainlit.io/api-reference/chat-settings



The `ChatSettings` class is designed to create and send a dynamic form to the UI. This form can be updated by the user.

## Attributes

<ParamField type="List[InputWidget]">
  The fields of the form. Mutually exclusive with `tabs` — use one or the other.
</ParamField>

<ParamField type="List[Tab]">
  Group inputs into named tabs. Each `Tab` has an `id`, a `label`, and its own list of `inputs`.
  Mutually exclusive with the top-level `inputs` list.
</ParamField>

## Methods

### `send()`

Sends the settings form to the UI **and** commits the current values into the session (`session.chat_settings`). Use this when initializing settings or when you want to update both the UI and the committed session state.

### `refresh()`

Pushes the settings form to the UI **without** updating the committed session settings. This is useful inside `@cl.on_settings_edit` when you want to dynamically update the available widgets (e.g., show/hide fields based on a selection) without treating the edit as a confirmed change.

<Note>
  Since version **2.11.0**.
</Note>

## Usage

```python theme={null}
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Slider(
                id="SAI_Steps",
                label="Stability AI - Steps",
                initial=30,
                min=10,
                max=150,
                step=1,
                description="Amount of inference steps performed on image generation.",
            ),
            Slider(
                id="SAI_Cfg_Scale",
                label="Stability AI - Cfg_Scale",
                initial=7,
                min=1,
                max=35,
                step=0.1,
                description="Influences how strongly your generation is guided to match your prompt.",
            ),
            Slider(
                id="SAI_Width",
                label="Stability AI - Image Width",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
            Slider(
                id="SAI_Height",
                label="Stability AI - Image Height",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)

```

You can also access the Chainlit chat settings using a combination of the `@` and `/` commands. Using `@`, you can trigger the chat settings **Select** input, and using `/`, you can choose the selected setting’s input values.

### Single Select option Type

<Frame>
  <img />
</Frame>

### Multi Select option Type

<Frame>
  <img />
</Frame>

## Dynamic Widget Refresh

Use `refresh()` inside `@cl.on_settings_edit` to update the form dynamically as the user edits, without committing changes to the session. The committed session settings only change when the user confirms (triggers `@cl.on_settings_update`).

```python theme={null}
import chainlit as cl
from chainlit.input_widget import Select, Slider


@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(
                id="Mode",
                label="Mode",
                values=["simple", "advanced"],
                initial_index=0,
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0.7,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()


@cl.on_settings_edit
async def on_edit(settings):
    inputs = [
        Select(
            id="Mode",
            label="Mode",
            values=["simple", "advanced"],
            initial_value=settings["Mode"],
        ),
        Slider(
            id="Temperature",
            label="Temperature",
            initial=settings.get("Temperature", 0.7),
            min=0,
            max=2,
            step=0.1,
        ),
    ]
    if settings["Mode"] == "advanced":
        inputs.append(
            Slider(
                id="TopP",
                label="Top P",
                initial=settings.get("TopP", 0.9),
                min=0,
                max=1,
                step=0.05,
            )
        )
    await cl.ChatSettings(inputs).refresh()


@cl.on_settings_update
async def on_update(settings):
    print("Confirmed settings:", settings)
```

<Note>
  Since version **2.11.0**.
</Note>

## Tabs

Use `Tab` to group settings into named tabs when you have many inputs across distinct categories.

```python theme={null}
import chainlit as cl
from chainlit.input_widget import Select, Slider, Tab


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        tabs=[
            Tab(
                id="llm",
                label="LLM",
                inputs=[
                    Select(
                        id="Model",
                        label="Model",
                        values=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
                        initial_index=0,
                    ),
                    Slider(
                        id="Temperature",
                        label="Temperature",
                        initial=0.7,
                        min=0,
                        max=2,
                        step=0.1,
                    ),
                ],
            ),
            Tab(
                id="image",
                label="Image",
                inputs=[
                    Slider(
                        id="Width",
                        label="Image Width",
                        initial=512,
                        min=256,
                        max=2048,
                        step=64,
                    ),
                    Slider(
                        id="Height",
                        label="Image Height",
                        initial=512,
                        min=256,
                        max=2048,
                        step=64,
                    ),
                ],
            ),
        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
```

<Note>
  Since version **2.9.1**.
</Note>


# Custom Data Layer
Source: https://docs.chainlit.io/api-reference/data-persistence/custom-data-layer



The `BaseDataLayer` class serves as an abstract foundation for data persistence operations within the Chainlit framework.
This class outlines methods for managing users, feedback, elements, steps, and threads in a chatbot application.

## Methods

<ParamField type="Coroutine">
  Fetches a user by their identifier. Return type is optionally a `PersistedUser`.
</ParamField>

<ParamField type="Coroutine">
  Creates a new user based on the `User` instance provided. Return type is optionally a `PersistedUser`.
</ParamField>

<ParamField type="Coroutine">
  Inserts or updates feedback. Accepts a `Feedback` instance and returns a string as an identifier of the persisted feedback.
</ParamField>

<ParamField type="Coroutine">
  Deletes a feedback by `feedback_id`. Return `True` if it was successful.
</ParamField>

<ParamField type="Coroutine">
  Adds a new element to the data layer. Accepts `ElementDict` as an argument.
</ParamField>

<ParamField type="Coroutine">
  Retrieves an element by `thread_id` and `element_id`. Return type is optionally an `ElementDict`.
</ParamField>

<ParamField type="Coroutine">
  Deletes an element given its identifier `element_id`.
</ParamField>

<ParamField type="Coroutine">
  Creates a new step in the data layer. Accepts `StepDict` as an argument.
</ParamField>

<ParamField type="Coroutine">
  Updates an existing step. Accepts `StepDict` as an argument.
</ParamField>

<ParamField type="Coroutine">
  Deletes a step given its identifier `step_id`.
</ParamField>

<ParamField type="Coroutine">
  Fetches the author of a given thread by `thread_id`. Returns a string representing the author identifier.
</ParamField>

<ParamField type="Coroutine">
  Deletes a thread given its identifier `thread_id`.
</ParamField>

<ParamField type="Coroutine">
  Lists threads based on `pagination` and `filters` arguments. Returns a `PaginatedResponse[ThreadDict]`.
</ParamField>

<ParamField type="Coroutine">
  Retrieves a thread by its identifier `thread_id`. Return type is optionally a `ThreadDict`.
</ParamField>

<ParamField type="Coroutine">
  Updates a thread's details like name, user\_id, metadata, and tags. Arguments are mostly optional.
</ParamField>

<ParamField type="Coroutine">
  Deletes a user session given its identifier `id`. Returns a boolean value indicating success.
</ParamField>

<ParamField type="Coroutine">
  Returns the list of steps that the user has marked as favorites. Used to populate the favorite messages (prompt templates) feature in the composer. Returns a `List[StepDict]`.

  <Note>
    Since version **2.9.5**.
  </Note>
</ParamField>

<ParamField type="Coroutine">
  Called when the Chainlit server shuts down. Use this to close database connections, HTTP sessions, or other resources held by the data layer. Must be implemented by all subclasses.

  <Warning>
    Since version **2.8.2**. This is a **breaking change** — all custom `BaseDataLayer` and `BaseStorageClient` subclasses must implement this method.
  </Warning>
</ParamField>

## Decorators

<ParamField type="Decorator">
  Queues certain methods to execute only after the first user message is received, especially useful for `WebsocketSessions`.
</ParamField>

## Example

Due to the abstract nature of `BaseDataLayer`, direct instantiation and usage are not practical without subclassing and implementing the abstract methods.

You can refer to the [guide for custom data layer implementation](/data-layers/overview).


# Audio
Source: https://docs.chainlit.io/api-reference/elements/audio



The `Audio` class allows you to display an audio player for a specific audio file in the chatbot user interface.

You must provide either an url or a path or content bytes.

## Attributes

<ParamField type="str">
  The name of the audio file to be displayed in the UI. This is shown to users.
</ParamField>

<ParamField type="ElementDisplay">
  Determines where the element should be displayed in the UI. Choices are "side"
  (default), "inline", or "page".
</ParamField>

<ParamField type="str">
  The remote URL of the audio.
</ParamField>

<ParamField type="str">
  The local file path of the audio.
</ParamField>

<ParamField type="bytes">
  The file content of the audio in bytes format.
</ParamField>

<ParamField type="bool">
  Whether the audio should start playing automatically.
</ParamField>

## Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    elements = [
        cl.Audio(name="example.mp3", path="./example.mp3", display="inline"),
    ]
    await cl.Message(
        content="Here is an audio file",
        elements=elements,
    ).send()
```


# Custom
Source: https://docs.chainlit.io/api-reference/elements/custom



The `CustomElement` class allows you to render a custom `.jsx` snippet. The `.jsx` file should be placed in `public/elements/ELEMENT_NAME.jsx`.

## Attributes

<ParamField type="str">
  The name of the custom Element. It should match the name of your JSX file (without the `.jsx` extension).
</ParamField>

<ParamField type="Dict">
  The props to pass to the JSX.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the text element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

## How to Write the JSX file

<Note>If you are not familiar with UI development, you can pass these instructions to an LLM to ask it to generate the `.jsx` for you!</Note>

To implement the `jsx` file for your Chainlit custom element, follow these instructions.

### Component definition

Only write JSX code, no TSX. Each `.jsx` file should export default one component like:

```jsx theme={null}
export default function MyComponent() {
    return <div>Hello World</div>
}
```

The component `props` are globally injected (not as a function argument). **NEVER** pass them as function argument.

### Use Tailwind for Styling

Under the hood, the code will be rendered in a shadcn + tailwind environment.
The theme is relying on CSS variables.

Here is an example rendering a `div` with a primary color background and round border:

```jsx theme={null}
export default function TailwindExample() {
    return <div className="bg-primary rounded-md h-4 w-full" />
}
```

### Only Use Allowed Imports

Only use available packages for imports. Here is the full list:

* `react`
* `sonner`
* `zod`
* `recoil`
* `react-hook-form`
* `lucide-react`
* `@/components/ui/accordion`
* `@/components/ui/aspect-ratio`
* `@/components/ui/avatar`
* `@/components/ui/badge`
* `@/components/ui/button`
* `@/components/ui/card`
* `@/components/ui/carousel`
* `@/components/ui/checkbox`
* `@/components/ui/command`
* `@/components/ui/dialog`
* `@/components/ui/dropdown-menu`
* `@/components/ui/form`
* `@/components/ui/hover-card`
* `@/components/ui/input`
* `@/components/ui/label`
* `@/components/ui/pagination`
* `@/components/ui/popover`
* `@/components/ui/progress`
* `@/components/ui/scroll-area`
* `@/components/ui/separator`
* `@/components/ui/select`
* `@/components/ui/sheet`
* `@/components/ui/skeleton`
* `@/components/ui/switch`
* `@/components/ui/table`
* `@/components/ui/textarea`
* `@/components/ui/tooltip`

<Note>The `@/components/ui` imports are from Shadcn.</Note>

### Available APIs

Chainlit exposes the following APIs globally to make the custom element interactive.

```ts theme={null}
interface APIs {
    // Update the element props. This will re-render the element.
    updateElement: (nextProps: Record<string, any>) => Promise<{success: boolean}>;
    // Delete the element entirely.
    deleteElement: () => Promise<{success: boolean}>;
    // Call an action defined in the Chainlit app
    callAction: (action: {name: string, payload: Record<string, unknown>}) =>Promise<{success: boolean}>;
    // Send a user message
    sendUserMessage: (message: string, command?: string) => void;
}
```

### Example of a Counter Element

```jsx theme={null}
import { Button } from "@/components/ui/button"
import { X, Plus } from 'lucide-react';

export default function Counter() {
    return (
        <div id="custom-counter" className="mt-4 flex flex-col gap-2">
                <div>Count: {props.count}</div>
                <Button id="increment" onClick={() => updateElement(Object.assign(props, {count: props.count + 1}))}><Plus /> Increment</Button>
                <Button id="remove" onClick={deleteElement}><X /> Remove</Button>
        </div>
    );
}
```

## Full Example

Let's build a custom element to render the status of a Linear ticket.

First, we write a small Chainlit application faking fetching data from linear:

```python app.py theme={null}
import chainlit as cl

async def get_ticket():
    """Pretending to fetch data from linear"""
    return {
        "title": "Fix Authentication Bug",
        "status": "in-progress",
        "assignee": "Sarah Chen",
        "deadline": "2025-01-15",
        "tags": ["security", "high-priority", "backend"]
    }

@cl.on_message
async def on_message(msg: cl.Message):
    # Let's pretend the user is asking about a linear ticket.
    # Usually an LLM with tool calling would be used to decide to render the component or not.
    
    props = await get_ticket()
    
    ticket_element = cl.CustomElement(name="LinearTicket", props=props)
    # Store the element if we want to update it server side at a later stage.
    cl.user_session.set("ticket_el", ticket_element)
    
    await cl.Message(content="Here is the ticket information!", elements=[ticket_element]).send()
```

Second we implement the custom element we reference in the Python code:

```jsx public/elements/LinearTicket.jsx theme={null}
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Clock, User, Tag } from "lucide-react"

export default function TicketStatusCard() {
  const getProgressValue = (status) => {
    const progress = {
      'open': 25,
      'in-progress': 50,
      'resolved': 75,
      'closed': 100
    }
    return progress[status] || 0
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg font-medium">
            {props.title || 'Untitled Ticket'}
          </CardTitle>
          <Badge 
            variant="outline" 
          >
            {props.status || 'Unknown'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Progress value={getProgressValue(props.status)} className="h-2" />
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <User className="h-4 w-4 opacity-70" />
              <span>{props.assignee || 'Unassigned'}</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 opacity-70" />
              <span>{props.deadline || 'No deadline'}</span>
            </div>
            <div className="flex items-center gap-2 col-span-2">
              <Tag className="h-4 w-4 opacity-70" />
              <span>{props.tags?.join(', ') || 'No tags'}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

Finally, we start the application with `chainlit run app.py` and send a first message in the UI.

<Frame>
  <img />
</Frame>

## Advanced

### Update Props from Python

To update a custom element props from the python code, you can store the element instance in the user session and call `.update()` on it.

```python theme={null}
import chainlit as cl

@cl.on_chat_start
async def start():
    element = cl.CustomElement(name="Foo", props={"foo": "bar"})
    cl.user_session.set("element", element)

@cl.on_message
async def on_message():
    element = cl.user_session.get("element")
    element.props["foo"] = "baz"
    await element.update()
```

### Call a Function from Python

If you need to call a function directly from the python code, you can use `cl.CopilotFunction`.

```python call_func.py theme={null}
import chainlit as cl

@cl.on_chat_start
async def start():
    element = cl.CustomElement(name="CallFn")
    await cl.Message(content="Hello", elements=[element]).send()
    
@cl.on_message
async def on_msg(msg: cl.Message):
    fn = cl.CopilotFunction(name="test", args={"content": msg.content})
    res = await fn.acall()
```

```jsx CallFn.jsx theme={null}
import { useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { callFnState } from '@chainlit/react-client';

export default function CallFnExample() {
    const callFn = useRecoilValue(callFnState);

    useEffect(() => {
        if (callFn?.name === "test") {
          // Replace the console log with your actual function
          console.log("Function called with", callFn.args.content)
          callFn.callback()
        }
      }, [callFn]);

      return null
}
```


# Dataframe
Source: https://docs.chainlit.io/api-reference/elements/dataframe



The `Dataframe` class is designed to send a dataframe to the chatbot user interface. Both `pandas` and `polars` DataFrames are supported — neither library is a hard dependency, so you can use whichever you have installed.

## Attributes

<ParamField type="str">
  The name of the dataframe to be displayed in the UI.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the dataframe element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="Union[pd.DataFrame, pl.DataFrame]">
  A pandas or polars DataFrame instance.

  <Note>
    Polars support added in version **2.11.0**.
  </Note>
</ParamField>

## Example

```python theme={null}
import pandas as pd

import chainlit as cl


@cl.on_chat_start
async def start():
    # Create a sample DataFrame with more than 10 rows to test pagination functionality
    data = {
        "Name": [
            "Alice",
            "David",
            "Charlie",
            "Bob",
            "Eva",
            "Grace",
            "Hannah",
            "Jack",
            "Frank",
            "Kara",
            "Liam",
            "Ivy",
            "Mia",
            "Noah",
            "Olivia",
        ],
        "Age": [25, 40, 35, 30, 45, 55, 60, 70, 50, 75, 80, 65, 85, 90, 95],
        "City": [
            "New York",
            "Houston",
            "Chicago",
            "Los Angeles",
            "Phoenix",
            "San Antonio",
            "San Diego",
            "San Jose",
            "Philadelphia",
            "Austin",
            "Fort Worth",
            "Dallas",
            "Jacksonville",
            "Columbus",
            "Charlotte",
        ],
        "Salary": [
            70000,
            100000,
            90000,
            80000,
            110000,
            130000,
            140000,
            160000,
            120000,
            170000,
            180000,
            150000,
            190000,
            200000,
            210000,
        ],
    }

    df = pd.DataFrame(data)

    elements = [cl.Dataframe(data=df, display="inline", name="Dataframe")]

    await cl.Message(content="This message has a Dataframe", elements=elements).send()
```

### Polars

```python theme={null}
import polars as pl

import chainlit as cl


@cl.on_chat_start
async def start():
    df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 30, 35],
            "City": ["New York", "Los Angeles", "Chicago"],
        }
    )

    elements = [cl.Dataframe(data=df, display="inline", name="Dataframe")]

    await cl.Message(content="This message has a Dataframe", elements=elements).send()
```


# File
Source: https://docs.chainlit.io/api-reference/elements/file



The `File` class allows you to display a button that lets users download the content of the file.

You must provide either an url or a path or content bytes.

## Attributes

<ParamField type="str">
  The name of the file. This will be shown to users.
</ParamField>

<ParamField type="str">
  The remote URL of the file image source.
</ParamField>

<ParamField type="str">
  The local file path of the file image.
</ParamField>

<ParamField type="bytes">
  The file content of the file image in bytes format.
</ParamField>

## Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    elements = [
        cl.File(
            name="hello.py",
            path="./hello.py",
            display="inline",
        ),
    ]

    await cl.Message(
        content="This message has a file element", elements=elements
    ).send()
```


# Image
Source: https://docs.chainlit.io/api-reference/elements/image



The `Image` class is designed to create and handle image elements to be sent and displayed in the chatbot user interface.

You must provide either an url or a path or content bytes.

## Attributes

<ParamField type="str">
  The name of the image to be displayed in the UI.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the image element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="ElementSize">
  Determines the size of the image. Only works with display="inline". Choices
  are "small", "medium" (default), or "large".
</ParamField>

<ParamField type="str">
  The remote URL of the image source.
</ParamField>

<ParamField type="str">
  The local file path of the image.
</ParamField>

<ParamField type="bytes">
  The file content of the image in bytes format.
</ParamField>

## Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    image = cl.Image(path="./cat.jpeg", name="image1", display="inline")

    # Attach the image to the message
    await cl.Message(
        content="This message has an image!",
        elements=[image],
    ).send()
```


# PDF viewer
Source: https://docs.chainlit.io/api-reference/elements/pdf



The `Pdf` class allows you to display a PDF hosted remotely or locally in the chatbot UI. This class either takes a URL of a PDF hosted online, or the path of a local PDF.

<Note>
  Since version **2.11.0**, the PDF viewer uses a custom React-based renderer
  with zoom, pagination, download, and print controls instead of the browser's
  built-in iframe viewer. The `pdfjs-dist` worker is bundled locally — no
  external CDN requests are made. If you relied on the previous iframe behavior
  or applied custom CSS targeting the old viewer, you may need to update your
  styles.
</Note>

## Attributes

<ParamField type="str">
  The name of the PDF to be displayed in the UI.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the PDF element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="str">
  The remote URL of the PDF file. Must provide url for a remote PDF (or either
  path or content for a local PDF).
</ParamField>

<ParamField type="str">
  The local file path of the PDF. Must provide either path or content for a
  local PDF (or url for a remote PDF).
</ParamField>

<ParamField type="bytes">
  The file content of the PDF in bytes format. Must provide either path or
  content for a local PDF (or url for a remote PDF).
</ParamField>

<ParamField type="int">
  The default rendered page. Must be an integer greater than 0 and less than or
  equal to the total number of pages in the PDF. The default value is 1.
</ParamField>

## Example

### Inline

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    # Sending a pdf with the local file path
    elements = [
      cl.Pdf(name="pdf1", display="inline", path="./pdf1.pdf", page=1)
    ]

    await cl.Message(content="Look at this local pdf!", elements=elements).send()
```

### Side and Page

You must have the name of the pdf in the content of the message for the link to be created.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    # Sending a pdf with the local file path
    elements = [
      cl.Pdf(name="pdf1", display="side", path="./pdf1.pdf", page=1)
    ]
    # Reminder: The name of the pdf must be in the content of the message
    await cl.Message(content="Look at this local pdf1!", elements=elements).send()
```


# Plotly
Source: https://docs.chainlit.io/api-reference/elements/plotly



The `Plotly` class allows you to display a Plotly chart in the chatbot UI. This class takes a Plotly figure.

The advantage of the `Plotly` element over the `Pyplot` element is that it's interactive (the user can zoom on the chart for example).

## Attributes

<ParamField type="str">
  The name of the chart to be displayed in the UI.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the chart element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="ElementSize">
  Determines the size of the chart. Only works with display="inline". Choices
  are "small", "medium" (default), or "large".
</ParamField>

<ParamField type="str">
  The `plotly.graph_objects.Figure` instance that you want to display.
</ParamField>

### Example

```python theme={null}
import plotly.graph_objects as go
import chainlit as cl


@cl.on_chat_start
async def start():
    fig = go.Figure(
        data=[go.Bar(y=[2, 1, 3])],
        layout_title_text="An example figure",
    )
    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

    await cl.Message(content="This message has a chart", elements=elements).send()
```


# Pyplot
Source: https://docs.chainlit.io/api-reference/elements/pyplot



The `Pyplot` class allows you to display a Matplotlib pyplot chart in the chatbot UI. This class takes a pyplot figure.

The difference of between this element and the `Plotly` element is that the user is shown a static image of the chart when using `Pyplot`.

## Attributes

<ParamField type="str">
  The name of the chart to be displayed in the UI.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the chart element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="ElementSize">
  Determines the size of the chart. Only works with display="inline". Choices
  are "small", "medium" (default), or "large".
</ParamField>

<ParamField type="str">
  The `matplotlib.figure.Figure` instance that you want to display.
</ParamField>

## Example

```python theme={null}
import matplotlib.pyplot as plt
import chainlit as cl


@cl.on_chat_start
async def main():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

    elements = [
        cl.Pyplot(name="plot", figure=fig, display="inline"),
    ]
    await cl.Message(
        content="Here is a simple plot",
        elements=elements,
    ).send()
```


# TaskList
Source: https://docs.chainlit.io/api-reference/elements/tasklist



The `TaskList` class allows you to display a task list next to the chatbot UI.

## Attributes

<ParamField type="str">
  The status of the TaskList. We suggest using something short like "Ready",
  "Running...", "Failed", "Done".
</ParamField>

<ParamField type="Task">
  The list of tasks to be displayed in the UI.
</ParamField>

## Task Attributes

<ParamField type="str">
  The task label shown in the UI. Supports Markdown formatting (e.g. `**bold**`, `[links](url)`).
</ParamField>

<ParamField type="TaskStatus">
  One of `TaskStatus.READY`, `TaskStatus.RUNNING`, `TaskStatus.DONE`, or `TaskStatus.FAILED`.
</ParamField>

<ParamField type="str">
  Optional message ID to link the task to a chat message, enabling task navigation in history.
</ParamField>

<Note>
  Markdown in `Task.title` is supported since version **2.9.0**.
</Note>

## Usage

The TaskList element is slightly different from other elements in that it is not attached to a Message or Step but can be sent directly to the chat interface.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    # Create the TaskList
    task_list = cl.TaskList()
    task_list.status = "Running..."

    # Create a task and put it in the running state
    task1 = cl.Task(title="Processing data", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task1)
    # Create another task that is in the ready state
    task2 = cl.Task(title="Performing calculations")
    await task_list.add_task(task2)

    # Optional: link a message to each task to allow task navigation in the chat history
    message = await cl.Message(content="Started processing data").send()
    task1.forId = message.id

    # Update the task list in the interface
    await task_list.send()

    # Perform some action on your end
    await cl.sleep(1)

    # Update the task statuses
    task1.status = cl.TaskStatus.DONE
    task2.status = cl.TaskStatus.FAILED
    task_list.status = "Failed"
    await task_list.send()

```

<Frame>
  <video />
</Frame>


# Text
Source: https://docs.chainlit.io/api-reference/elements/text



The `Text` class allows you to display a text element in the chatbot UI. This class takes a string and creates a text element that can be sent to the UI.
It supports the markdown syntax for formatting text.

You must provide either an url or a path or content bytes.

## Attributes

<ParamField type="str">
  The name of the text element to be displayed in the UI.
</ParamField>

<ParamField type="Union[str, bytes]">
  The text string or bytes that should be displayed as the content of the text
  element.
</ParamField>

<ParamField type="str">
  The remote URL of the text source.
</ParamField>

<ParamField type="str">
  The local file path of the text file.
</ParamField>

<ParamField type="ElementDisplay">
  Determines how the text element should be displayed in the UI. Choices are
  "side", "inline", or "page".
</ParamField>

<ParamField type="str">
  Language of the code if the text is a piece of code. See
  [https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages](https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages)
  for a list of supported languages.
</ParamField>

## Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    text_content = "Hello, this is a text element."
    elements = [
        cl.Text(name="simple_text", content=text_content, display="inline")
    ]

    await cl.Message(
        content="Check out this text element!",
        elements=elements,
    ).send()
```


# Video
Source: https://docs.chainlit.io/api-reference/elements/video



The `Video` class allows you to display an video player for a specific video file in the chatbot user interface.

You must provide either an url or a path or content bytes.

## Attributes

<ParamField type="str">
  The name of the video file to be displayed in the UI. This is shown to users.
</ParamField>

<ParamField type="ElementDisplay">
  Determines where the element should be displayed in the UI. Choices are "side"
  (default), "inline", or "page".
</ParamField>

<ParamField type="str">
  The remote URL of the video.
</ParamField>

<ParamField type="str">
  The local file path of the video.
</ParamField>

<ParamField type="bytes">
  The file content of the video in bytes format.
</ParamField>

## Example

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    elements = [
        cl.Video(name="example.mp4", path="./example.mp4", display="inline"),
    ]
    await cl.Message(
        content="Here is an video file",
        elements=elements,
    ).send()
```


# Checkbox
Source: https://docs.chainlit.io/api-reference/input-widgets/checkbox



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label displayed next to the checkbox.
</ParamField>

<ParamField type="bool">
  The initial checked state of the checkbox.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import Checkbox


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Checkbox(
                id="VerboseMode",
                label="Enable verbose output",
                initial=False,
            )
        ]
    ).send()
    value = settings["VerboseMode"]

```


# DatePicker
Source: https://docs.chainlit.io/api-reference/input-widgets/datepicker



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="Literal['single', 'range']">
  Selection mode. `"single"` selects one date, `"range"` selects a start and end date.
</ParamField>

<ParamField type="str | date | tuple[str | date, str | date] | None">
  The initial value. For `"single"` mode, pass an ISO date string or `date` object.
  For `"range"` mode, pass a tuple of two values (start, end).
</ParamField>

<ParamField type="str | date | None">
  Minimum selectable date. Dates before this are disabled in the calendar.
</ParamField>

<ParamField type="str | date | None">
  Maximum selectable date. Dates after this are disabled in the calendar.
</ParamField>

<ParamField type="str | None">
  Display format string using [date-fns format tokens](https://date-fns.org/docs/format) (e.g. `"yyyy/MM/dd"`).
</ParamField>

<ParamField type="str | None">
  Placeholder text shown when no date is selected.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

<Note>
  Since version **2.9.6**.
</Note>

### Usage

```python Single date theme={null}
import chainlit as cl
from chainlit.input_widget import DatePicker


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            DatePicker(
                id="start_date",
                label="Start Date",
                placeholder="Pick a date",
                min_date="2025-01-01",
                max_date="2026-12-31",
            )
        ]
    ).send()
    value = settings["start_date"]
```

```python Date range theme={null}
import chainlit as cl
from chainlit.input_widget import DatePicker


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            DatePicker(
                id="date_range",
                label="Date Range",
                mode="range",
                initial=("2025-06-01", "2025-06-30"),
            )
        ]
    ).send()
    value = settings["date_range"]
```


# MultiSelect
Source: https://docs.chainlit.io/api-reference/input-widgets/multiselect



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="List[str]">
  Labels for the select options.
</ParamField>

<ParamField type="Dict[str, str]">
  Labels with corresponding values for the select options.
</ParamField>

<ParamField type="List[str]">
  The initially selected values.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import MultiSelect


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            MultiSelect(
                id="Tools",
                label="Enabled Tools",
                values=["web_search", "calculator", "file_reader", "code_interpreter"],
                initial=["web_search", "calculator"],
            )
        ]
    ).send()
    value = settings["Tools"]

```


# RadioGroup
Source: https://docs.chainlit.io/api-reference/input-widgets/radiogroup



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="List[str]">
  Labels for the radio options.
</ParamField>

<ParamField type="Dict[str, str]">
  Labels with corresponding values for the radio options.
</ParamField>

<ParamField type="str">
  The initially selected value.
</ParamField>

<ParamField type="int">
  Index of the initial value. Can only be used in combination with `values`.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import RadioGroup


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            RadioGroup(
                id="ResponseLength",
                label="Response Length",
                values=["Short", "Medium", "Long"],
                initial_index=1,
            )
        ]
    ).send()
    value = settings["ResponseLength"]

```


# Select
Source: https://docs.chainlit.io/api-reference/input-widgets/select



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="List[str]">
  Labels for the select options.
</ParamField>

<ParamField type="Dict[str, str]">
  Labels with corresponding values for the select options.
</ParamField>

<ParamField type="int">
  The initial value of the input widget.
</ParamField>

<ParamField type="int">
  Index of the initial value of the input widget.
  Can only be used in combination with 'values'.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import Select


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            )
        ]
    ).send()
    value = settings["Model"]

```


# Slider
Source: https://docs.chainlit.io/api-reference/input-widgets/slider



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="int">
  The initial value of the input widget.
</ParamField>

<ParamField type="int">
  The minimum permitted slider value. Defaults to 0.
</ParamField>

<ParamField type="int">
  The maximum permitted slider value. Defaults to 10.
</ParamField>

<ParamField type="int">
  The stepping interval of the slider. Defaults to 1.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import Slider


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
    value = settings["Temperature"]

```


# Switch
Source: https://docs.chainlit.io/api-reference/input-widgets/switch



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="int">
  The initial value of the input widget.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import Switch


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
        ]
    ).send()
    value = settings["Streaming"]

```


# Tags
Source: https://docs.chainlit.io/api-reference/input-widgets/tags



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="List[str]">
  The initial values of the input widget.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import Tags


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Tags(id="StopSequence", label="OpenAI - StopSequence", initial=["Answer:"]),
        ]
    ).send()
    value = settings["StopSequence"]

```


# TextInput
Source: https://docs.chainlit.io/api-reference/input-widgets/textinput



### Attributes

<ParamField type="str">
  The identifier used to retrieve the widget value from the settings.
</ParamField>

<ParamField type="str">
  The label of the input widget.
</ParamField>

<ParamField type="str">
  The initial value of the input widget.
</ParamField>

<ParamField type="str">
  The placeholder value of the input widget.
</ParamField>

<ParamField type="str">
  The tooltip text shown when hovering over the tooltip icon next to the label.
</ParamField>

<ParamField type="str">
  The text displayed underneath the input widget.
</ParamField>

### Usage

```python Code Example theme={null}
import chainlit as cl
from chainlit.input_widget import TextInput


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            TextInput(id="AgentName", label="Agent Name", initial="AI"),
        ]
    ).send()
    value = settings["AgentName"]

```


# Langchain Callback Handler
Source: https://docs.chainlit.io/api-reference/integrations/langchain



The following code example demonstrates how to pass a callback handler:

```python theme={null}
llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm=llm)

@cl.on_message
async def main(message: cl.Message):

    res = await llm_math.acall(message.content, callbacks=[cl.LangchainCallbackHandler()])

    await cl.Message(content="Hello").send()
```

## Final Answer streaming

If streaming is enabled at the LLM level, Langchain will only stream the intermediate steps. You can enable final answer streaming by passing `stream_final_answer=True` to the callback handler.

```python theme={null}
# Optionally, you can also pass the prefix tokens that will be used to identify the final answer
answer_prefix_tokens=["FINAL", "ANSWER"]

cl.LangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=answer_prefix_tokens,
    )
```

<Warning>
  Final answer streaming will only work with prompts that have a consistent
  final answer pattern. It will also not work with
  `AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`
</Warning>


# LlamaIndex Callback Handler
Source: https://docs.chainlit.io/api-reference/integrations/llamaindex



Callback Handler to enable Chainlit to display intermediate steps in the UI.

### Usage

```python Code Example theme={null}
from llama_index.core.callbacks import CallbackManager
from llama_index.core.service_context import ServiceContext
import chainlit as cl



@cl.on_chat_start
async def start():
    service_context = ServiceContext.from_defaults(callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]))
    # use the service context to create the predictor
```


# on_audio_chunk
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-audio-chunk



Hook to react to an incoming audio chunk from the user's microphone.

## Usage

```python theme={null}
from io import BytesIO
import chainlit as cl


@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.InputAudioChunk):
    pass
```


# on_audio_end
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-audio-end



Hook to react to the end of an audio recording coming from the user's microphone.

## Usage

```python theme={null}
from io import BytesIO
import chainlit as cl


@cl.on_audio_end
async def on_audio_end():
    pass
```


# on_chat_end
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-chat-end



Hook to react to the user websocket disconnection event.

## Usage

```python theme={null}
import chainlit as cl


@cl.on_chat_start
def start():
    print("hello", cl.user_session.get("id"))


@cl.on_chat_end
def end():
    print("goodbye", cl.user_session.get("id"))

```


# on_chat_resume
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-chat-resume



Decorator to enable users to continue a conversation.
Requires both [data persistence](/data-persistence/overview) and [authentication](/authentication) to be enabled.

This decorator will automatically:

* Send the persisted messages and elements to the UI.
* Restore the user session.

<Warning>
  Only JSON serializable fields of the user session will be saved and restored.
</Warning>

## Usage

At minimum, you will need to use the `@cl.on_chat_resume` decorator to resume conversations.

```python theme={null}
@cl.on_chat_resume
async def on_chat_resume(thread):
    pass
```

However, if you are using a Langchain agent for instance, you will need to reinstantiate and set it in the user session yourself.

<Card title="Resume Langchain Chat Example" icon="message" href="https://github.com/Chainlit/cookbook/tree/main/resume-chat">
  Practical example of how to resume a chat with context.
</Card>

## Parameters

<ParamField type="ThreadDict">
  The persisted chat to resume.
</ParamField>


# on_chat_start
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-chat-start



Hook to react to the user websocket connection event.

## Usage

```python Code Example theme={null}
from chainlit import AskUserMessage, Message, on_chat_start


@on_chat_start
async def main():
    res = await AskUserMessage(content="What is your name?", timeout=30).send()
    if res:
        await Message(
            content=f"Your name is: {res['output']}.\nChainlit installation is working!\nYou can now start building your own chainlit apps!",
        ).send()
```


# on_logout
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-logout



Decorator to react to a user logging out. Useful to clear cookies or other user data through the HTTP response.

## Parameters

<ParamField type="fastapi.Request">
  The request object.
</ParamField>

<ParamField type="fastapi.Response">
  The response object.
</ParamField>

## Usage

```python theme={null}
from fastapi import Request, Response

import chainlit as cl


@cl.on_logout
def main(request: Request, response: Response):
    response.delete_cookie("my_cookie")
```


# on_message
Source: https://docs.chainlit.io/api-reference/lifecycle-hooks/on-message



Decorator to react to messages coming from the UI.
The decorated function is called every time a new message is received.

## Parameters

<ParamField type="cl.Message">
  The message coming from the UI.
</ParamField>

## Usage

```python theme={null}
import chainlit as cl

@cl.on_message
def main(message: cl.Message):
  content = message.content
  # do something
```


# make_async
Source: https://docs.chainlit.io/api-reference/make-async



The `make_async` function takes a synchronous function (for instance a LangChain agent) and returns an asynchronous function that will run the original function in a separate thread.
This is useful to run long running synchronous tasks without blocking the event loop.

## Parameters

<ParamField type="Callable">
  The synchronous function to run in a separate thread.
</ParamField>

## Returns

<ResponseField name="async_function" type="Coroutine">
  The asynchronous function that will run the synchronous function in a separate
  thread.
</ResponseField>

## Usage

```python theme={null}
import time
import chainlit as cl

def sync_func():
    time.sleep(5)
    return "Hello!"

@cl.on_message
async def main(message: cl.Message):
    answer = await cl.make_async(sync_func)()
    await cl.Message(
        content=answer,
    ).send()
```

```python LangChain agent theme={null}
import chainlit as cl

res = await cl.make_async(agent)(input_str, callbacks=[cl.LangchainCallbackHandler()])
await cl.Message(content=res["text"]).send()
```


# Message
Source: https://docs.chainlit.io/api-reference/message



The `Message` class is designed to send, stream, update or remove messages.

## Parameters

<ParamField type="str">
  The content of the message.
</ParamField>

<ParamField type="str">
  The author of the message, defaults to the chatbot name defined in your config
  file.
</ParamField>

<ParamField type="Element[]">
  Elements to attach to the message.
</ParamField>

<ParamField type="Action[]">
  Actions to attach to the message.
</ParamField>

<ParamField type="str">
  Language of the code if the content is code. See
  [https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages](https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages)
  for a list of supported languages.
</ParamField>

<ParamField type="Dict">
  Custom metadata dictionary to attach to the message. Persisted with the message in the data layer.
</ParamField>

<ParamField type="List[str]">
  Tags to attach to the message for filtering and categorization.
</ParamField>

<ParamField type="str">
  The [command](/concepts/command) selected by the user for this message. Set automatically by the UI when the user picks a command. Access this value in the [on\_message](/api-reference/lifecycle-hooks/on-message) handler via `msg.command`.

  <Note>
    Since version **2.1.0**.
  </Note>
</ParamField>

<ParamField type="Dict[str, str]">
  The [modes](/concepts/modes) selected by the user for this message, as a dict of `{mode_id: option_id}`. Set automatically by the UI when the user configures mode pickers. Access this value in the [on\_message](/api-reference/lifecycle-hooks/on-message) handler via `msg.modes`.

  <Note>
    Since version **2.9.4**.
  </Note>
</ParamField>

<ParamField type="str">
  Unique identifier for the message. Auto-generated as a UUID if not provided.
</ParamField>

<ParamField type="str">
  ID of the parent step or message. Automatically resolved from the current step context if not provided.
</ParamField>

<ParamField type="str">
  The message type (`assistant_message` or `user_message`). Automatically set based on the message direction.
</ParamField>

<ParamField type="str">
  ISO 8601 timestamp for the message creation. Automatically set to the current UTC time when `.send()` is called.
</ParamField>

## Send a message

Send a new message to the UI.

```python theme={null}
import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

## Stream a message

Send a message token by token to the UI.

```python theme={null}
import chainlit as cl

token_list = ["the", "quick", "brown", "fox"]


@cl.on_chat_start
async def main():
    msg = await cl.Message(content="").send()
    for token in token_list:
        await msg.stream_token(token)

    await msg.update()
```

## Update a message

Update a message that already has been sent.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    msg = cl.Message(content="Hello!")
    await msg.send()

    await cl.sleep(2)

    msg.content = "Hello again!"
    await msg.update()
```

## Remove a message

Remove a message from the UI.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    msg = cl.Message(content="Message 1")
    await msg.send()
    await cl.sleep(2)
    await msg.remove()
```


# Step Class
Source: https://docs.chainlit.io/api-reference/step-class



The `Step` class is a Python Context Manager that can be used to create steps in your chainlit app. The step is created when the context manager is entered and is updated to the client when the context manager is exited.

## Parameters

<ParamField type="str">
  The name of the step. Default to the name of the decorated function.
</ParamField>

<ParamField type="Enum">
  The type of the step, useful for monitoring and debugging.
</ParamField>

<ParamField type="List[Element]">
  Elements to attach to the step.
</ParamField>

<ParamField type="str">
  Language of the output. See
  [https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages](https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages)
  for a list of supported languages.
</ParamField>

<ParamField type="Union[bool, str]">
  By default only the output of the step is shown. Set this to `True` to also
  show the input. You can also set this to a language like `json` or `python` to
  syntax highlight the input.
</ParamField>

<ParamField type="bool">
  Whether the step should render expanded by default in the UI.

  <Note>
    Since version **2.3.0**. Requires a `defaultOpen` column in the `steps` table for SQL-based data layers. See the [migration guide](/guides/migration/2.3.0).
  </Note>
</ParamField>

<ParamField type="Dict">
  Custom metadata dictionary to attach to the step. Persisted with the step in the data layer.
</ParamField>

<ParamField type="List[str]">
  Tags to attach to the step for filtering and categorization.
</ParamField>

<ParamField type="str">
  Unique identifier for the step. Auto-generated as a UUID if not provided.
</ParamField>

<ParamField type="str">
  ID of the parent step. Automatically resolved from the context manager nesting hierarchy if not provided.
</ParamField>

<ParamField type="str">
  Name of a Lucide icon to display instead of the default step avatar. See [https://lucide.dev/icons](https://lucide.dev/icons) for available icons.

  <Note>
    Since version **2.11.0**.
  </Note>
</ParamField>

<ParamField type="str">
  ID of the thread this step belongs to. Automatically resolved from the current session context if not provided.
</ParamField>

## Send a Step

```python theme={null}
import chainlit as cl

@cl.on_message
async def main():
    async with cl.Step(name="Test") as step:
        # Step is sent as soon as the context manager is entered
        step.input = "hello"
        step.output = "world"

    # Step is updated when the context manager is exited
```

## Stream the Output

```python theme={null}
from openai import AsyncOpenAI

import chainlit as cl

client = AsyncOpenAI()

@cl.on_message
async def main(msg: cl.Message):

    async with cl.Step(name="gpt4", type="llm") as step:
        step.input = msg.content

        stream = await client.chat.completions.create(
            messages=[{"role": "user", "content": msg.content}],
            stream=True,
            model="gpt-4",
            temperature=0,
        )

        async for part in stream:
            delta = part.choices[0].delta
            if delta.content:
                # Stream the output of the step
                await step.stream_token(delta.content)
```

## Nest Steps

To nest steps, simply create a step inside another step.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    async with cl.Step(name="Parent step") as parent_step:
        parent_step.input = "Parent step input"

        async with cl.Step(name="Child step") as child_step:
            child_step.input = "Child step input"
            child_step.output = "Child step output"

        parent_step.output = "Parent step output"
```

## Update a Step

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    async with cl.Step(name="Parent step") as step:
        step.input = "Parent step input"
        step.output = "Parent step output"

    await cl.sleep(2)

    step.output = "Parent step output updated"
    await step.update()
```

## Remove a Step

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def main():
    async with cl.Step(name="Parent step") as step:
        step.input = "Parent step input"
        step.output = "Parent step output"

    await cl.sleep(2)

    await step.remove()
```


# Step Decorator
Source: https://docs.chainlit.io/api-reference/step-decorator



The step decorator will log steps based on the decorated function. By default, the arguments of the function will be used as the input of the step and the return value will be used as the output.

Under the hood, the step decorator is using the [cl.Step](/api-reference/step-class) class.

## Parameters

<ParamField type="str">
  The name of the step. Default to the name of the decorated function.
</ParamField>

<ParamField type="str">
  The type of the step, useful for monitoring and debugging.
</ParamField>

<ParamField type="str">
  Language of the output. See
  [https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages](https://react-code-blocks-rajinwonderland.vercel.app/?path=/story/codeblock--supported-languages)
  for a list of supported languages.
</ParamField>

<ParamField type="Union[bool, str]">
  By default only the output of the step is shown. Set this to `True` to also
  show the input. You can also set this to a language like `json` or `python` to
  syntax highlight the input.
</ParamField>

<ParamField type="bool">
  Whether the step should render expanded by default in the UI.

  <Note>
    Since version **2.3.0**. Requires a `defaultOpen` column in the `steps` table for SQL-based data layers. See the [migration guide](/guides/migration/2.3.0).
  </Note>
</ParamField>

<ParamField type="Dict">
  Custom metadata dictionary to attach to the step. Persisted with the step in the data layer.
</ParamField>

<ParamField type="List[str]">
  Tags to attach to the step for filtering and categorization.
</ParamField>

<ParamField type="str">
  Unique identifier for the step. Auto-generated as a UUID if not provided.
</ParamField>

<ParamField type="str">
  Name of a Lucide icon to display instead of the default step avatar. See [https://lucide.dev/icons](https://lucide.dev/icons) for available icons.

  <Note>
    Since version **2.11.0**.
  </Note>
</ParamField>

<ParamField type="str">
  ID of the parent step. Automatically resolved from the decorator nesting hierarchy if not provided.
</ParamField>

## Access the Current step

You can access the current step object using `cl.context.current_step` and override values.

```python theme={null}
import chainlit as cl

@cl.step
async def my_step():
    current_step = cl.context.current_step

    # Override the input of the step
    current_step.input = "My custom input"

    # Override the output of the step
    current_step.output = "My custom output"
```

## Stream the Output

```python theme={null}
from openai import AsyncOpenAI

import chainlit as cl

client = AsyncOpenAI(api_key="YOUR_API_KEY")

@cl.step(type="llm")
async def gpt4():
    settings = {
        "model": "gpt-4",
        "temperature": 0,
    }

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    current_step = cl.context.current_step

    async for part in stream:
        delta = part.choices[0].delta

        if delta.content:
            # Stream the output of the step
            await current_step.stream_token(delta.content)
```

## Nest Steps

If another step decorated function is called inside the decorated function, the child step will be nested under the parent step.

```python theme={null}
import chainlit as cl

@cl.step
async def parent_step():
    await child_step()
    return "Parent step output"

@cl.step
async def child_step():
    return "Child step output"

@cl.on_chat_start
async def main():
    await parent_step()
```


# Window Messaging
Source: https://docs.chainlit.io/api-reference/window-message



# on\_window\_message

Decorator to react to messages coming from the Web App's parent window.
The decorated function is called every time a new window message is received.

## Parameters

<ParamField type="str">
  The message coming from the Web App's parent window.
</ParamField>

## Usage

```python theme={null}
import chainlit as cl

@cl.on_window_message
def main(message: str):
  # do something
```

# send\_window\_message

Function to send messages to the Web App's parent window.

## Parameters

<ParamField type="str">
  The message to send to the Web App's parent window.
</ParamField>

## Usage

```python theme={null}
@cl.on_message
async def message():
  await cl.send_window_message("Server: Hello from Chainlit")
```


# Header
Source: https://docs.chainlit.io/authentication/header



Header auth is a simple way to authenticate users using a header. It is typically used to delegate authentication to a reverse proxy.

The `header_auth_callback` function is called with the headers of the request. It should return a `User` object if the user is authenticated, or `None` if the user is not authenticated.
The callback function (defined by the user) is responsible for managing the authentication logic.

## Example

```python theme={null}
from typing import Optional

import chainlit as cl


@cl.header_auth_callback
def header_auth_callback(headers: Dict) -> Optional[cl.User]:
  # Verify the signature of a token in the header (ex: jwt token)
  # or check that the value is matching a row from your database
  if headers.get("test-header") == "test-value":
    return cl.User(identifier="admin", metadata={"role": "admin", "provider": "header"})
  else:
    return None
```

Using this code, you will not be able to access the app unless the header `test-header` is set to `test-value` when sending any request to the app.


# OAuth
Source: https://docs.chainlit.io/authentication/oauth



OAuth lets you use third-party services to authenticate your users.

<Note>
  To active an OAuth provider, you need to define both the OAuth callback in
  your code and the provider(s) environment variables.
</Note>

## Providers

Follow these guides to create an OAuth app for your chosen provider(s). Then copy the information into the right environment variable to active the provider.

<Warning>
  If your app is served behind a reverse proxy (like cloud run) you will have to
  set the `CHAINLIT_URL` environment variable. For instance, if you host your
  application at `https://mydomain.com`, `CHAINLIT_URL` should be set to
  `https://mydomain.com`.
</Warning>

### GitHub

Go to this page to [create a new GitHub OAuth app](https://github.com/settings/applications/new).

The callback URL should be: `CHAINLIT_URL/auth/oauth/github/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/github/callback`.

You need to set the following environment variables:

* `OAUTH_GITHUB_CLIENT_ID`: Client ID
* `OAUTH_GITHUB_CLIENT_SECRET`: Client secret

### Gitlab

Go to this page to [create a new GitLab OAuth app](https://docs.gitlab.com/ee/integration/oauth_provider.html). When creating the app, you need to allow the `openid`, `profile` and `email` scopes.

The callback URL should be: `CHAINLIT_URL/auth/oauth/gitlab/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/gitlab/callback`.

You need to set the following environment variables:

* `OAUTH_GITLAB_CLIENT_ID`: Client ID
* `OAUTH_GITLAB_CLIENT_SECRET`: Client secret
* `OAUTH_GITLAB_DOMAIN`: domain name (without the protocol)

### Google

Go to this page to [create a new Google OAuth app](https://console.developers.google.com/apis/credentials).

The callback URL should be: `CHAINLIT_URL/auth/oauth/google/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/google/callback`.

You need to set the following environment variables:

* `OAUTH_GOOGLE_CLIENT_ID`: Client ID
* `OAUTH_GOOGLE_CLIENT_SECRET`: Client secret

### Azure Active Directory

Follow this guide to [create a new Azure Active Directory OAuth app](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).

The callback URL should be: `CHAINLIT_URL/auth/oauth/azure-ad/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/azure-ad/callback`.

You need to set the following environment variables:

* `OAUTH_AZURE_AD_CLIENT_ID`: Client ID
* `OAUTH_AZURE_AD_CLIENT_SECRET`: Client secret
* `OAUTH_AZURE_AD_TENANT_ID`: Azure tenant ID

Optional environment variables:

* `OAUTH_AZURE_AD_ENABLE_SINGLE_TENANT`: Set to `true` if your application supports "Accounts in this organizational directory only" (Single tenant). If not, do not set this environment variable at all.
* `OAUTH_AZURE_AD_SCOPES`: Space-separated list of OAuth scopes (default: `https://graph.microsoft.com/User.Read offline_access`).
* `OAUTH_AZURE_AD_HYBRID_SCOPES`: Space-separated list of scopes for the hybrid flow (default: `https://graph.microsoft.com/User.Read https://graph.microsoft.com/openid offline_access`).

<Note>
  `OAUTH_AZURE_AD_SCOPES` and `OAUTH_AZURE_AD_HYBRID_SCOPES` are available
  since version **2.11.0**.
</Note>

### Okta

Follow this guide to [create OIDC app integrations](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_oidc.htm).

The callback URL should be: `CHAINLIT_URL/auth/oauth/okta/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/okta/callback`.

You need to set the following environment variables:

* `OAUTH_OKTA_CLIENT_ID`: Client ID
* `OAUTH_OKTA_CLIENT_SECRET`: Client secret
* `OAUTH_OKTA_DOMAIN`: Domain name for your okta setup - e.g. [https://company.okta.com](https://company.okta.com)

There are several ways to configure the Okta OAuth routes:

* When using the [Single Sign-On to Okta](https://developer.okta.com/docs/reference/api/oidc/#composing-your-base-url) setup, you need to set the `OAUTH_OKTA_AUTHORIZATION_SERVER_ID` environment variable to `false`.
* When using Okta [as the identity platform for your app or API](https://developer.okta.com/docs/reference/api/oidc/#_2-okta-as-the-identity-platform-for-your-app-or-api) either:
  * set the `OAUTH_OKTA_AUTHORIZATION_SERVER_ID` environment variable to `default` if you have a developer account,
  * or set it to the authorization server id from your Custom Authorization Server.

### Descope

Head to the [Descope sign-up page](https://www.descope.com/sign-up), to get started with your account and set up your authentication.

The callback URL should be: `CHAINLIT_URL/auth/oauth/descope/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/descope/callback`.

You need to set the following environment variables:

* `OAUTH_DESCOPE_CLIENT_ID`: Descope Project ID, which can be found under [Project Settings](https://app.descope.com/settings/project) in the console.
* `OAUTH_DESCOPE_CLIENT_SECRET`: Descope Access Key, which can be created under [Access Keys](https://app.descope.com/accesskeys) in the console.

### Auth0

Follow this guide to [create an Auth0 application](https://auth0.com/docs/get-started/auth0-overview/create-applications).

The callback URL should be: `CHAINLIT_URL/auth/oauth/auth0/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/auth0/callback`.

You need to set the following environment variables:

* `OAUTH_AUTH0_CLIENT_ID`: Client ID
* `OAUTH_AUTH0_CLIENT_SECRET`: Client secret
* `OAUTH_AUTH0_DOMAIN`: Domain name for your auth0 setup

Optional environment variables:

* `OAUTH_AUTH0_ORIGINAL_DOMAIN`: Original domain name for your auth0 setup, if you are using a custom domain

### Amazon Cognito

Follow this guide to [create a new Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-user-pool.html).

The callback URL should be: `CHAINLIT_URL/auth/oauth/aws-cognito/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/aws-cognito/callback`.

You need to set the following environment variables:

* `OAUTH_COGNITO_CLIENT_ID`: Client ID
* `OAUTH_COGNITO_CLIENT_SECRET`: Client secret
* `OAUTH_COGNITO_DOMAIN`: Cognito Domain
* `OAUTH_COGNITO_SCOPE`: Access level

### Keycloak

Follow this documentation to [create a new client](https://www.keycloak.org/docs/latest/server_admin/index.html#assembly-managing-clients_server_administration_guide) in your realm.

You have the option of changing the `id` of your Keycloak provider, which by default is `keycloak`. This is useful if you want to display a more appropriate name on your login page. Use the `OAUTH_KEYCLOAK_NAME` environment variable to set the name. Don't choose an `id` that conflicts with any of the other Oauth providers.

The callback URL for your client should be: `CHAINLIT_URL/auth/oauth/${OAUTH_KEYCLOAK_NAME}/callback`. If your Chainlit app is hosted at localhost:8000, you should use `http://localhost:8000/auth/oauth/${OAUTH_KEYCLOAK_NAME}/callback`.

You need to set the following environment variables:

* `OAUTH_KEYCLOAK_CLIENT_ID`: Client ID
* `OAUTH_KEYCLOAK_CLIENT_SECRET`: Client secret
* `OAUTH_KEYCLOAK_REALM`: The realm which contains your client.
* `OAUTH_KEYCLOAK_BASE_URL`: Your Keycloak URL.
* `OAUTH_KEYCLOAK_NAME`: Optional, see above.

### Custom Provider

It's possible to plug-in for any OAuth provider using Chainlit. Required steps are:

* modifying `providers` variable in runtime
* implementing `CustomOAuthProvider(OAuthProvider)` class with methods and fields:
  * `get_token(self, code, url)`
  * `get_user_info(self, token)`
  * `authorize_params`
  * `env`
* providing environmental variables as described in `env`, for example:
  * `YOUR_PROVIDER_CLIENT_ID`
  * `YOUR_PROVIDER_CLIENT_SECRET`

[This cookbook example](https://github.com/Chainlit/cookbook/tree/main/auth) describes how to do it, also check [base class](https://github.com/Chainlit/chainlit/blob/2cb38ad8596ac547355f87266bc15ab3dfd632d2/backend/chainlit/oauth_providers.py#L13) for reference.

## Prompt Configuration

<Note>
  Since version **1.3.0**.
</Note>

Chainlit allows you to configure how OAuth providers handle re-authentication through the `prompt` parameter. This is particularly useful for controlling the login behavior when users log out.

You can configure this behavior using two environment variables:

* `OAUTH_PROMPT`: Sets the default prompt behavior for all OAuth providers
* `OAUTH_<PROVIDER>_PROMPT`: Sets the prompt behavior for a specific provider (e.g., `OAUTH_GITHUB_PROMPT`)

The supported values for these variables are:

* `none`: No interaction required (default if not set)
* `login`: Forces re-authentication
* `consent`: Asks for approval of the requested scopes
* `select_account`: Allows users to select a different account

For example:

```bash theme={null}
# Force consent prompt for all providers
OAUTH_PROMPT=consent

# Override specific provider to force login
OAUTH_GITHUB_PROMPT=login
```

Note: The behavior and support for different prompt values may vary between OAuth providers. For instance:

* GitHub responds well to `prompt=consent`
* Some providers like Descope only respect `prompt=login`

This feature is particularly useful when you want to:

* Allow users to properly log out and switch accounts
* Force re-authentication for security purposes
* Give users the option to change which scopes they approve
* Prevent automatic re-authentication after logout

The prompt parameter is defined in the OpenID Connect Core 1.0 specification. For more technical details, refer to the [OpenID Connect documentation](https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest).

## Examples

### Allow all users who passed the oauth authentication.

```python theme={null}
from typing import Dict, Optional
import chainlit as cl


@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  return default_user
```

### Only allow users from a specific google domain.

```python theme={null}
from typing import Dict, Optional
import chainlit as cl


@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  if provider_id == "google":
    if raw_user_data["hd"] == "example.org":
      return default_user
  return None
```


# Overview
Source: https://docs.chainlit.io/authentication/overview



Chainlit applications are public by default.
To enable authentication and make your app private, you need to:

1. Define a `CHAINLIT_AUTH_SECRET` environment variable. This is a secret string that is used to sign the authentication tokens. You can change it at any time, but it will log out all users. You can easily generate one using `chainlit create-secret`.
2. Add one or more authentication callbacks to your app:

<CardGroup>
  <Card title="Password Auth" icon="shield" href="/authentication/password">
    Authenticate users with login/password.
  </Card>

  <Card title="OAuth" icon="google" href="/authentication/oauth">
    Authenticate users with your own OAuth app (like Google).
  </Card>

  <Card title="Header" icon="code" href="/authentication/header">
    Authenticate users based on a custom header.
  </Card>
</CardGroup>

Each callback take a different input and optionally return a `cl.User` object. If the callback returns `None`, the authentication is considered as failed.

<Warning>
  Make sure each user has a unique identifier to prevent them from sharing their
  data.
</Warning>

## Get the current authenticated user

You can access the current authenticated user through the [User Session](/concepts/user-session).

```py theme={null}
@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user")
    await cl.Message(f"Hello {app_user.identifier}").send()
```


# Password
Source: https://docs.chainlit.io/authentication/password



The `@cl.password_auth_callback` receives the username and password from the login form. Returning an `cl.User` object will authenticate the user while returning `None` will fail the authentication.

You can verify the credentials against any service that you'd like (your own DB, a private google sheet etc.).

<Warning>
  The usual security best practices applies here, hash password before storing
  them.
</Warning>

## Example

```python theme={null}
from typing import Optional
import chainlit as cl

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
```


# Command Line Options
Source: https://docs.chainlit.io/backend/command-line



The Chainlit CLI (Command Line Interface) is a tool that allows you to interact with the Chainlit system via command line. It provides several commands to manage your Chainlit applications.

## Commands

### `init`

The `init` command initializes a Chainlit project by creating a configuration file located at `.chainlit/config.toml`

```bash theme={null}
chainlit init
```

### `run`

The `run` command starts a Chainlit application.

```bash theme={null}
chainlit run [OPTIONS] TARGET
```

Options:

* `-w, --watch`: Reload the app when the module changes. When this option is specified, the file watcher will be started and any changes to files will cause the server to reload the app, allowing faster iterations.
* `-h, --headless`: Prevents the app from opening in the browser.
* `-d, --debug`: Sets the log level to debug. Default log level is error.
* `-c, --ci`: Runs in CI mode.
* `--no-cache`: Disables third parties cache, such as langchain.
* `--host`: Specifies a different host to run the server on.
* `--port`: Specifies a different port to run the server on.
* `--root-path`: Specifies a subpath to run the server on.


# Features
Source: https://docs.chainlit.io/backend/config/features



## Options

### File Upload

<ParamField type="bool">
  Authorize users to upload files with messages. The files are then accessible
  in [cl.on\_message](/api-reference/lifecycle-hooks/on-message).
</ParamField>

<ParamField type="Union[List[str], Dict[str, List[str]]]">
  Restrict user to only upload accepted mime file types. Example: \["text/plain",
  "application/pdf", "image/x-png"]
</ParamField>

<ParamField type="int">
  Restrict user to upload maximum number of files at a time.
</ParamField>

<ParamField type="int">
  Restrict uploading file size (MB).
</ParamField>

### Audio

<ParamField type="bool">
  Enable audio features.
</ParamField>

<Warning>
  Since Chainlit 2.7.0, `audio.enabled` must be explicitly set to `true` in `config.toml`. It is no longer auto-inferred from the existence of an `on_audio_chunk` callback.
</Warning>

<ParamField type="int">
  Audio sample rate in hertz. Defaults to 24kHz
</ParamField>

### MCP

See [MCP server-side configuration](/advanced-features/mcp#server-side-configuration-config-toml)

### Slack

See [Slack integration documentation](/deploy/slack)

### Favorites

<ParamField type="bool">
  Enable favorite messages (prompt templates). When enabled, users can star their
  own messages and reuse them as prompt templates from the composer. Requires
  [data persistence](/data-persistence/overview) to store favorites.

  <Note>
    Since version **2.9.5**.
  </Note>
</ParamField>

### Other

<ParamField type="bool">
  Process and display mathematical expressions. This can clash with "\$"
  characters in messages.
</ParamField>

<ParamField type="bool">
  Autoscroll new user messages at the top of the window.
</ParamField>

<ParamField type="bool">
  Autoscroll assistant messages as they stream. Set to `false` to keep the
  viewport stable while new assistant tokens arrive.

  <Note>
    Since version **2.9.4**.
  </Note>
</ParamField>

<ParamField type="bool">
  Process and display HTML in messages. This can be a security risk (see
  [https://stackoverflow.com/questions/19603097/why-is-it-dangerous-to-render-user-generated-html-or-javascript](https://stackoverflow.com/questions/19603097/why-is-it-dangerous-to-render-user-generated-html-or-javascript)).
</ParamField>

<ParamField type="bool">
  Automatically tag threads with the current chat profile (if a chat profile is
  used)
</ParamField>

<ParamField type="bool">
  Allow the user to edit their messages.
</ParamField>

<ParamField type="bool">
  Allow users to share threads with other users. Requires [authentication](/authentication/overview), [data persistence](/data-persistence/overview), and an [`on_shared_thread_view`](/api-reference/lifecycle-hooks/on-shared-thread-view) callback.
</ParamField>

## Default configuration

```toml theme={null}
[features]
# Process and display HTML in messages. This can be a security risk (see https://stackoverflow.com/questions/19603097/why-is-it-dangerous-to-render-user-generated-html-or-javascript)
unsafe_allow_html = false

# Process and display mathematical expressions. This can clash with "$" characters in messages.
latex = false

# Autoscroll new user messages at the top of the window
user_message_autoscroll = true

# Autoscroll assistant messages as they stream
assistant_message_autoscroll = true

# Automatically tag threads with the current chat profile (if a chat profile is used)
auto_tag_thread = true

# Allow users to edit their own messages
edit_message = true

# Allow users to share threads (requires on_shared_thread_view callback)
allow_thread_sharing = false

# Enable favorite messages (prompt templates)
favorites = false

# Authorize users to spontaneously upload files with messages
[features.spontaneous_file_upload]
    enabled = true
    # Define accepted file types using MIME types
    # Examples:
    # 1. For specific file types:
    #    accept = ["image/jpeg", "image/png", "application/pdf"]
    # 2. For all files of certain type:
    #    accept = ["image/*", "audio/*", "video/*"]
    # 3. For specific file extensions:
    #    accept = {{ "application/octet-stream" = [".xyz", ".pdb"] }}
    # Note: Using "*/*" is not recommended as it may cause browser warnings
    accept = ["*/*"]
    max_files = 20
    max_size_mb = 500

[features.audio]
    # Enable audio features
    enabled = false
    # Sample rate of the audio
    sample_rate = 24000

[features.mcp]
    # Enable Model Context Protocol (MCP) features
    enabled = false
```


# Overview
Source: https://docs.chainlit.io/backend/config/overview



The `.chainlit/config.toml` file is created when you run `chainlit run ...` or `chainlit init`. It allows you to configure your Chainlit app and to enable/disable specific features.

You can also dynamically override specific `config.toml` variables by Chat Profile at runtime. See [Dynamic Profile-based Configuration](/api-reference/lifecycle-hooks/on-profile-switch) for details.

It is composed of three sections:

<CardGroup>
  <Card title="project" icon="rocket-launch" href="/backend/config/project">
    Project configuration.
  </Card>

  <Card title="features" icon="flag" href="/backend/config/features">
    Enable/disable features.
  </Card>

  <Card title="UI" icon="palette" href="/backend/config/ui">
    UI configuration.
  </Card>
</CardGroup>


# Project
Source: https://docs.chainlit.io/backend/config/project



## Options

<ParamField type="List[str]">
  Authorized origins to access the app/copilot.
</ParamField>

<ParamField type="List[str]">
  Socket.io client transports option
</ParamField>

<ParamField type="List[str]">
  List of environment variables to be provided by each user to use the app. If empty, no environment variables will be asked to the user.
</ParamField>

<ParamField type="bool">
  Whether to persist user environment variables (API keys) to the database. When enabled, users do not need to re-enter their keys on each session.
</ParamField>

<ParamField type="bool">
  Whether to mask user environment variables in the UI using a password-type input field.
</ParamField>

<ParamField type="str">
  Path to the local langchain cache database
</ParamField>

<ParamField type="int">
  Duration (in seconds) during which the session is saved when the connection is lost
</ParamField>

<ParamField type="int">
  Duration (in seconds) of the user session expiry. 15 days by default
</ParamField>

<ParamField type="bool">
  Enable third parties caching (e.g LangChain cache)
</ParamField>

## Default configuration

```toml theme={null}
[project]
# List of environment variables to be provided by each user to use the app.
user_env = []

# Whether to persist user environment variables (API keys) to the database
persist_user_env = false

# Whether to mask user environment variables (API keys) in the UI with password type
mask_user_env = false

# Duration (in seconds) during which the session is saved when the connection is lost
session_timeout = 3600

# Duration (in seconds) of the user session expiry
user_session_timeout = 1296000  # 15 days

# Enable third parties caching (e.g., LangChain cache)
cache = false

# Authorized origins
allow_origins = ["*"]
```


# UI
Source: https://docs.chainlit.io/backend/config/ui



## Options

<ParamField type="str">
  The name of both the application and the chatbot.
</ParamField>

<ParamField type="str">
  The content of the `<meta name="description">` of the application.
</ParamField>

<ParamField type="Literal['hidden', 'tool_call', 'full']">
  The chain of thought (COT) is a feature that shows the user the steps the
  chatbot took to reach a conclusion. You can hide the COT, only show the tool
  calls, or show it in full.
</ParamField>

<ParamField type="Literal['light', 'dark']">
  Name of the theme used by default
</ParamField>

<ParamField type="Literal['default', 'wide']">
  Name of the layout used by default
</ParamField>

<ParamField type="str">
  Passing this option will display a Github-shaped link. If not passed we will
  display the link to Chainlit repo.
</ParamField>

<ParamField type="str">
  Custom CSS file that allows you to customize the UI
</ParamField>

<ParamField type="str">
  Custom CSS file tag attributes, i.e. `<stylesheet src="public/custom.css" ... ></stylesheet>`
</ParamField>

<ParamField type="str">
  Custom JavaScript file that allows you to customize the UI
</ParamField>

<ParamField type="str">
  Custom JavaScript file tag attributes, i.e. `<script src="public/custom.js" ... ></script>`
</ParamField>

<ParamField type="Literal['classic', 'modern']">
  Switch between two available alert styles:

  * `'classic'`: Traditional left-border style
  * `'modern'`: Rounded corners with softer borders and transparent background
</ParamField>

<ParamField type="str">
  Custom image displayed as the background on the login page
</ParamField>

<ParamField type="str">
  Filter applied to the custom background image on the login page
</ParamField>

<ParamField type="str">
  Filter applied to the custom background image on the login page when the dark theme is selected
</ParamField>

<ParamField type="str">
  Content of the `<meta property="og:url">` tag. Used in link previews (e.g. iMessage, Twitter). Defaults to the Chainlit GitHub repository URL if not set.
</ParamField>

<ParamField type="str">
  Content of the `<meta property="og:image">` tag used for site preview
</ParamField>

<ParamField type="str">
  URL of the image used as the application logo on the welcome screen and during login/logout
</ParamField>

<ParamField type="str">
  URL of the image used as the avatar for messages sent by the assistant
</ParamField>

<ParamField type="str">
  Directory containing custom frontend production build files, if applicable
</ParamField>

<ParamField type="str">
  Force a specific UI language for all users, overriding the browser's language preference.
  Accepts any locale code present in `.chainlit/translations/` (e.g. `en-US`, `fr-FR`, `he-IL`).
  When unset (default), the language is detected from the user's browser.

  <Note>
    Since version **2.9.3**.
  </Note>
</ParamField>

<ParamField type="List[HeaderLink]">
  Additional links displayed in the header next to (or replacing, if not provided) the GitHub link.
  Each link supports an optional `target` field to control how the link opens: `_blank` (default), `_self`, `_parent`, or `_top`.

  <Note>
    The `target` field is available since version **2.8.3**.
  </Note>
</ParamField>

<ParamField type="bool">
  Whether to show a confirmation dialog when the user clicks "New Chat".
  Set to `false` to skip the dialog and immediately clear the chat.

  <Note>
    Since version **2.9.6**.
  </Note>
</ParamField>

<ParamField type="Literal['message_composer', 'sidebar']">
  Where to display chat settings. `"message_composer"` shows them in a modal triggered from the composer.
  `"sidebar"` moves them to a resizable right sidebar with a gear icon toggle in the header.

  <Note>
    Since version **2.9.6**.
  </Note>
</ParamField>

<ParamField type="bool">
  Whether the chat settings sidebar is open when the page loads. Only applies when
  `chat_settings_location` is set to `"sidebar"`.

  <Note>
    Since version **2.9.6**.
  </Note>
</ParamField>

## Default configuration

```toml theme={null}
[UI]
# Name of the assistant.
name = "Assistant"

# default_theme = "dark"

# layout = "wide"

# default_sidebar_state = "open"

# Show confirmation dialog when creating a new chat
# confirm_new_chat = true

# Where to display chat settings: "message_composer" (default modal) or "sidebar"
# chat_settings_location = "message_composer"

# Whether the chat settings sidebar is open on page load (sidebar mode only)
# default_chat_settings_open = false

# Description of the assistant. This is used for HTML tags.
# description = ""

# Chain of Thought (CoT) display mode. Can be "hidden", "tool_call" or "full".
cot = "full"

# Force a specific UI language for all users (overrides browser detection).
# Accepts any locale available under .chainlit/translations/
# language = "en-US"

# Specify a CSS file that can be used to customize the user interface.
# The CSS file can be served from the public directory or via an external link.
# custom_css = "/public/test.css"

# Specify additional attributes for a custom CSS file
# custom_css_attributes = "media=\\\"print\\\""

# Specify a JavaScript file that can be used to customize the user interface.
# The JavaScript file can be served from the public directory.
# custom_js = "/public/test.js"

# The style of alert boxes. Can be "classic" or "modern".
alert_style = "classic"

# Specify additional attributes for custom JS file
# custom_js_attributes = "async type = \\\"module\\\""

# Custom login page image, relative to public directory or external URL
# login_page_image = "/public/custom-background.jpg"

# Custom login page image filter (Tailwind internal filters, no dark/light variants)
# login_page_image_filter = "brightness-50 grayscale"
# login_page_image_dark_filter = "contrast-200 blur-sm"


# Specify a custom meta url for link previews (og:url).
# custom_meta_url = "https://example.com"

# Specify a custom meta image url.
# custom_meta_image_url = "https://chainlit-cloud.s3.eu-west-3.amazonaws.com/logo/chainlit_banner.png"

# Load assistant logo directly from URL.
logo_file_url = ""

# Load assistant avatar image directly from URL.
default_avatar_file_url = ""

# Specify a custom build directory for the frontend.
# This can be used to customize the frontend code.
# Be careful: If this is a relative path, it should not start with a slash.
# custom_build = "./public/build"

# Specify optional one or more custom links in the header.
# [[UI.header_links]]
#     name = "Issues"
#     display_name = "Report Issue"
#     icon_url = "https://avatars.githubusercontent.com/u/128686189?s=200&v=4"
#     url = "https://github.com/Chainlit/chainlit/issues"
#     target = "_self"  # Optional: _blank (default), _self, _parent, _top
```


# Environment Variables
Source: https://docs.chainlit.io/backend/env-variables



Hardcoding API keys in your code is not a good practice. It makes your code less portable and less flexible. It also makes it harder to keep your code secure. Instead, you should use environment variables to store values that are specific to your development environment.

Chainlit will automatically load environment variables from a `.env` file in the root of your project. This file should be added to your `.gitignore` file so that it is not committed to your repository.

```bash .env theme={null}
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
```

## Public Apps & Environment Variables

If you want to share your app to a broader audience, you should not put your own OpenAI API keys in the `.env` file.
Instead, you should use `user_env` in the Chainlit config to ask each user to provide their own keys.

You can then access the user's keys in your code using:

```python theme={null}
import chainlit as cl

user_env = cl.user_session.get("env")
```


# Action
Source: https://docs.chainlit.io/concepts/action



Actions are a way to send clickable buttons to the user interface. Each action is attached to a [Message](/api-reference/message) and can be used to trigger a python function when the user clicks on it.

## Create an action

Actions are sent to the UI through messages:

```python theme={null}
import chainlit as cl

@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="action_button",
            icon="mouse-pointer-click",
            payload={"value": "example_value"},
            label="Click me!"
        )
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()
```

## Define a Python Callback

To handle the user's click on the action button, you need to define a callback function with the `@cl.action_callback` decorator:

```python theme={null}
@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    print(action.payload)
```

<Card title="Action API" icon="bolt" href="/api-reference/action">
  Learn how more about Actions.
</Card>


# Chat Life Cycle
Source: https://docs.chainlit.io/concepts/chat-lifecycle



Whenever a user connects to your Chainlit app, a new chat session is created. A chat session goes through a life cycle of events, which you can respond to by defining hooks.

## On Chat Start

The [on\_chat\_start](/api-reference/lifecycle-hooks/on-chat-start) decorator is used to define a hook that is called when a new chat session is created.

```python theme={null}
@cl.on_chat_start
def on_chat_start():
    print("A new chat session has started!")
```

## On Message

The [on\_message](/api-reference/lifecycle-hooks/on-message) decorator is used to define a hook that is called when a new message is received from the user.

```python theme={null}
@cl.on_message
def on_message(msg: cl.Message):
    print("The user sent: ", msg.content)
```

## On Stop

The `on_stop` decorator is used to define a hook that is called when the user clicks the stop button while a task was running.

```python theme={null}
@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
```

## On Chat End

The [on\_chat\_end](/api-reference/lifecycle-hooks/on-chat-end) decorator is used to define a hook that is called when the chat session ends either because the user disconnected or started a new chat session.

```python theme={null}
@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")
```

## On Chat Resume

The [on\_chat\_resume](/api-reference/lifecycle-hooks/on-chat-resume) decorator is used to define a hook that is called when a user resumes a chat session that was previously disconnected. This can only happen if [authentication](/authentication) and [data persistence](/data-persistence) are enabled.

```python theme={null}
from chainlit.types import ThreadDict

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")
```


# Command
Source: https://docs.chainlit.io/concepts/command



Commands are a great way to capture user intent in a deterministic way.

## Attributes

<ParamField type="str">
  Identifier for the command, this will be used in the UI.
</ParamField>

<ParamField type="str">
  The lucide icon name for the command. See [https://lucide.dev/icons/](https://lucide.dev/icons/).
</ParamField>

<ParamField type="str">
  The description of the command.
</ParamField>

<ParamField type="boolean">
  Whether to display the command as a button in the message composer.
</ParamField>

<ParamField type="boolean">
  Whether to keep the command active after the user sent the message.
</ParamField>

## Set available commands

You can set the available commands at any moment using the `cl.context.emitter.set_commands` method.

```python theme={null}
import chainlit as cl

commands = [
    {"id": "Picture", "icon": "image", "description": "Use DALL-E"},
    {"id": "Search", "icon": "globe", "description": "Find on the web"},
    {
        "id": "Canvas",
        "icon": "pen-line",
        "description": "Collaborate on writing and code",
    },
]

@cl.on_chat_start
async def start():
    await cl.context.emitter.set_commands(commands)

@cl.on_message
async def message(msg: cl.Message):
    if msg.command == "Picture":
        # User is using the Picture command
        pass
    pass
```

<Frame>
  <img />
</Frame>

<Note>
  Since version **2.1.0**. If you use a SQL-based data layer, the `steps` table requires a `command` column. See the [migration guide](/guides/migration/2.1.0).
</Note>


# Element
Source: https://docs.chainlit.io/concepts/element



Text messages are the building blocks of a chatbot, but we often want to send more than just text to the user such as images, videos, and more.

That is where elements come in. Each element is a piece of content that can be attached to a [Message](/concepts/message) or a [Step](/concepts/step) and displayed on the user interface.

<CardGroup>
  <Card title="Image Element" icon="image" href="/api-reference/elements/image">
    Ideal to display generated images.
  </Card>

  <Card title="PDF Element" icon="file-pdf" href="/api-reference/elements/pdf">
    Ideal to display RAG sources.
  </Card>

  <Card title="Custom Element" icon="react" href="/api-reference/elements/custom">
    Write your own element in JSX.
  </Card>

  <Card title="More Elements" icon="wind" href="/api-reference/elements">
    The complete list of elements you can display on the user interface.
  </Card>
</CardGroup>

## Example

To attach an element to a message or step, we need to:

1. Instantiate the element
2. Attach the element to a message or step

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    image = cl.Image(path="./cat.jpeg", name="image1", display="inline")

    # Attach the image to the message
    await cl.Message(
        content="This message has an image!",
        elements=[image],
    ).send()
```

## Display Options

There are 3 display options that determine how an element is rendered:

### Side

```python theme={null}
@cl.on_chat_start
async def start():
    # Notice the display option
    image = cl.Image(path="./cat.jpeg", name="cat image", display="side")

    await cl.Message(
        # Notice that the name of the image is referenced in the message content
        content="Here is the cat image!",
        elements=[image],
    ).send()
```

The image will not be displayed in the message. Instead, the name of the image will be displayed as clickable link.
When the user clicks on the link, the image will be displayed on the side of the message.

### Page

```python theme={null}
@cl.on_chat_start
async def start():
    # Notice the display option
    image = cl.Image(path="./cat.jpeg", name="cat image", display="page")

    await cl.Message(
        # Notice that the name of the image is referenced in the message content
        content="Here is the cat image!",
        elements=[image],
    ).send()
```

The image will not be displayed in the message. Instead, the name of the image will be displayed as clickable link.
Clicking on the link will redirect to a dedicated page where the image will be displayed.

### Inline

```python theme={null}
@cl.on_chat_start
async def start():
    # Notice the display option
    image = cl.Image(path="./cat.jpeg", name="cat image", display="inline")

    await cl.Message(
        # Notice that the name of the image is NOT referenced in the message content
        content="Hello!",
        elements=[image],
    ).send()
```

The image will be displayed below with the message regardless of whether the image name is referenced in the message content.

## Control the Element Sidebar from Python

You can open/close the sidebar directly in Python. Elements attached to the sidebar will not be persisted, as this sidebar state is not the result of an interaction in the UI.

```python theme={null}
import chainlit as cl


@cl.on_chat_start
async def start():
    # Define the elements you want to display
    elements = [
        cl.Image(path="./cat.jpeg", name="image1"),
        cl.Pdf(path="./dummy.pdf", name="pdf1"),
        cl.Text(content="Here is a side text document", name="text1"),
        cl.Text(content="Here is a page text document", name="text2"),
    ]

    # Setting elements will open the sidebar
    await cl.ElementSidebar.set_elements(elements)
    await cl.ElementSidebar.set_title("Test title")

@cl.on_message
async def message(msg: cl.Message):
    # You can update the elements
    await cl.ElementSidebar.set_elements([cl.Text(content="Text changed!")])
    # You can update the title
    await cl.ElementSidebar.set_title("Title changed!")

    await cl.sleep(2)

    # Setting the elements to an empty array will close the sidebar
    await cl.ElementSidebar.set_elements([])
```


# Message
Source: https://docs.chainlit.io/concepts/message



A Message is a piece of information that is sent from the user to an assistant and vice versa.
Coupled with life cycle hooks, they are the building blocks of a chat.

A message has a content, a timestamp and cannot be nested.

## Example: Reply to a user message

Lets create a simple assistant that replies to a user message with a greeting.

```py theme={null}
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    response = f"Hello, you just sent: {message.content}!"
    await cl.Message(response).send()
```

<Card title="Message API" icon="message" href="/api-reference/message">
  Learn more about the Message API.
</Card>

## Chat Context

Since LLMs are stateless, you will often have to accumulate the messages of the current conversation in a list to provide the full context to LLM with each query.

You could do that manually with the [user\_session](/concepts/user-session). However, Chainlit provides a built-in way to do this:

```py chat_context theme={null}
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    # Get all the messages in the conversation in the OpenAI format
    print(cl.chat_context.to_openai())

    # Send the response
    response = f"Hello, you just sent: {message.content}!"
    await cl.Message(response).send()
```

Every message sent or received will be automatically accumulated in `cl.chat_context`.
You can then use `cl.chat_context.to_openai()` to get the conversation in the OpenAI format and feed it to the LLM.


# Modes
Source: https://docs.chainlit.io/concepts/modes



The Modes system allows you to define multiple picker categories (e.g., Model, Reasoning Effort, Persona) that users can configure for their chat session. This is more flexible than a single LLM picker and persists across messages.

## Data Structure

### ModeOption

A single selectable option within a Mode.

<ParamField type="str">
  Unique identifier for this option (e.g., "gpt-4", "planning").
</ParamField>

<ParamField type="str">
  Display name shown in the UI (e.g., "GPT-4", "Planning").
</ParamField>

<ParamField type="str">
  Brief description shown in the dropdown.
</ParamField>

<ParamField type="str">
  The lucide icon name or URL for the option. See [https://lucide.dev/icons/](https://lucide.dev/icons/).
</ParamField>

<ParamField type="boolean">
  Whether this option should be selected by default.
</ParamField>

### Mode

A category of options (e.g., "Model", "Reasoning").

<ParamField type="str">
  Unique identifier for the mode (e.g., "model").
</ParamField>

<ParamField type="str">
  Display name for the picker trigger.
</ParamField>

<ParamField type="List[ModeOption]">
  List of available options for this mode.
</ParamField>

## Set available Modes

You can define available modes using `cl.context.emitter.set_modes` inside the `on_chat_start` handler.

```python theme={null}
import chainlit as cl

@cl.on_chat_start
async def start():
    # Define a Model picker
    model_mode = cl.Mode(
        id="model",
        name="Model",
        options=[
            cl.ModeOption(id="gpt-4", name="GPT-4", icon="sparkles", default=True),
            cl.ModeOption(id="gpt-3.5", name="GPT-3.5", icon="bolt"),
        ]
    )

    # Define a Reasoning Effort picker
    reasoning_mode = cl.Mode(
        id="reasoning",
        name="Reasoning",
        options=[
            cl.ModeOption(id="high", name="High Effort", description="Think harder"),
            cl.ModeOption(id="low", name="Low Effort", description="Faster response"),
        ]
    )
    
    # Send modes to the UI
    await cl.context.emitter.set_modes([model_mode, reasoning_mode])

@cl.on_message
async def message(msg: cl.Message):
    # Access selected modes directly from the message object
    # Returns a dict of {mode_id: option_id}
    print(msg.modes) 
    # Output: {'model': 'gpt-4', 'reasoning': 'low'}
    
    selected_model = msg.modes.get("model")
    
    await cl.Message(
        content=f"Using model: {selected_model}"
    ).send()
```

<Frame>
  <img />
</Frame>

<Warning>
  Since version **2.9.4**. If you use a SQL-based data layer, the `steps` table requires a `modes` column. See the [migration guide](/guides/migration/2.9.4).
</Warning>


# Starters
Source: https://docs.chainlit.io/concepts/starters



Starters are suggestions to help your users get started with your assistant.

```python starters.py theme={null}
import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
        ),

        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
            command="code",
        ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
        )
    ]
# ...
```

<Frame>
  <img />
</Frame>

## Starter Categories

You can group starters into categories that appear as clickable buttons. Users select a category to reveal its starters. Define categories with `@cl.set_starter_categories`:

```python starter_categories.py theme={null}
import chainlit as cl

@cl.set_starter_categories
async def starter_categories(user: cl.User):
    return [
        cl.StarterCategory(
            label="Creative",
            icon="https://example.com/creative.png",  # optional
            starters=[
                cl.Starter(label="Write a poem", message="Write a poem about the sea"),
                cl.Starter(label="Write a story", message="Write a short story"),
            ],
        ),
        cl.StarterCategory(
            label="Educational",
            starters=[
                cl.Starter(label="Explain", message="Explain quantum computing"),
            ],
        ),
    ]
```

`StarterCategory` accepts:

* `label` (str) — the category button text
* `icon` (str, optional) — URL for the category icon
* `starters` (List\[Starter]) — starters shown when the category is selected

The callback accepts the same optional parameters as `@cl.set_starters`: `user`, `language`, and `chat_profile`. All are optional — declare only what you need.

```python profile_categories.py theme={null}
@cl.set_starter_categories
async def starter_categories(user: cl.User, language: str, chat_profile: str):
    if chat_profile == "Advanced":
        return [
            cl.StarterCategory(
                label="Advanced",
                starters=[
                    cl.Starter(label="Deep dive", message="Explain in detail"),
                ],
            ),
        ]
    return [
        cl.StarterCategory(
            label="General",
            starters=[
                cl.Starter(label="Hello", message="Say hello"),
            ],
        ),
    ]
```

<Note>
  The `chat_profile` parameter is available since version **2.11.1**.
</Note>

When both `@cl.set_starters` and `@cl.set_starter_categories` are defined, categories take precedence.

<Note>
  Since version **2.10.0**.
</Note>

## With Localization

The `@cl.set_starters` callback accepts an optional `language` parameter, allowing you to return localized starters based on the user's language.

```python localized_starters.py theme={null}
@cl.set_starters
async def set_starters(current_user: cl.User, language: str):
    if language == "fr":
        return [
            cl.Starter(
                label="Routine matinale",
                message="Pouvez-vous m'aider à créer une routine matinale personnalisée ?",
                icon="/public/idea.svg",
            ),
        ]
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine?",
            icon="/public/idea.svg",
        ),
    ]
```

## With Chat Profiles

Starters also work with [Chat Profiles](/advanced-features/chat-profiles). You can define different starters for different chat profiles.

```python starters_with_chat_profiles.py theme={null}
@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] != "ADMIN":
        return None

    return [
        cl.ChatProfile(
            name="My Chat Profile",
            icon="https://picsum.photos/250",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/public/idea.svg",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/public/learn.svg",
                ),
            ],
        )
    ]
```


# Step
Source: https://docs.chainlit.io/concepts/step



LLM powered Assistants take multiple steps to process a user's request, forming a chain of thought.
Unlike a [Message](concepts/message), a Step has a type, an input/output and a start/end.

Depending on the `config.ui.cot` setting, the full chain of thought can be displayed in full, hidden or only the tool calls.

## A Simple Tool Calling Example

Lets take a simple example of a Chain of Thought that takes a user's message, process it and sends a response.

```py theme={null}
import chainlit as cl


@cl.step(type="tool")
async def tool():
    # Simulate a running task
    await cl.sleep(2)

    return "Response from the tool!"


@cl.on_message
async def main(message: cl.Message):
    # Call the tool
    tool_res = await tool()

    # Send the final answer.
    await cl.Message(content="This is the final answer").send()
```

<Frame>
  <img />
</Frame>

## Step API

There are two ways to create steps, either by using the the `@cl.step` decorator or by using the `cl.Step` class.

<CardGroup>
  <Card title="@cl.step" icon="at" href="/api-reference/step-decorator">
    Easier to use but requires to split your step logic in a function.
  </Card>

  <Card title="with cl.Step():" icon="code" href="/api-reference/step-class">
    More verbose but usable in any context as a Python Context Manager.
  </Card>
</CardGroup>


# User Session
Source: https://docs.chainlit.io/concepts/user-session



The user session is designed to persist data in memory through the [life cycle](/concepts/chat-lifecycle) of a chat session. Each user session is unique to a user and a given chat session.

## Why use the user session?

Let's say you want to keep track of each chat session message count.

A naive implementation might look like this:

<Warning>
  This example is for illustrative purposes only. It is not recommended to use
  this code in production.
</Warning>

```python Naive Example theme={null}
import chainlit as cl

counter = 0


@cl.on_message
async def on_message(message: cl.Message):
    global counter
    counter += 1

    await cl.Message(content=f"You sent {counter} message(s)!").send()
```

At first glance, this code seems to work. However, it has a major flaw. If two users are chatting with the bot at the same time, both users will increment the same `counter`.

This is where the user session comes in. Let's rewrite the above example using the user session:

```python Correct example theme={null}
import chainlit as cl


@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("counter", 0)


@cl.on_message
async def on_message(message: cl.Message):
    counter = cl.user_session.get("counter")
    counter += 1
    cl.user_session.set("counter", counter)

    await cl.Message(content=f"You sent {counter} message(s)!").send()
```

## User Session Default Values

By default, Chainlit stores chat session related data in the user session.

The following keys are reserved for chat session related data:

<ParamField type="str">
  The session id.
</ParamField>

<ParamField type="cl.User">
  Only set if you are enabled [Authentication](/authentication). Contains the
  user object of the user that started this chat session.
</ParamField>

<ParamField type="str">
  Only relevant if you are using the [Chat
  Profiles](/advanced-features/chat-profiles) feature. Contains the chat profile
  selected by this user.
</ParamField>

<ParamField type="Dict">
  Only relevant if you are using the [Chat
  Settings](/advanced-features/chat-settings) feature. Contains the chat
  settings given by this user.
</ParamField>

<ParamField type="Dict">
  Only relevant if you are using the [user\_env](/backend/config/project) config.
  Contains the environment variables given by this user.
</ParamField>


# Avatars
Source: https://docs.chainlit.io/customisation/avatars



The default assistant avatar is the favicon of the application. See how to customize the favicon [here](/customisation/custom-logo-and-favicon).

However, you can customize the avatar by placing an image file in the `/public/avatars` folder.
The image file should be named after the author of the message. For example, if the author is `My Assistant`, the avatar should be named `my_assistant.png`.

```
public/
└── avatars/
    └── my_assistant.png
```


# CSS
Source: https://docs.chainlit.io/customisation/custom-css



Chainlit Application allows for design customization through the use of a custom CSS stylesheet. To enable this, modify your configuration settings in .chainlit/config.toml.

```toml config.toml theme={null}
[UI]
# ...
# This can either be a css file in your `public` dir or a URL
custom_css = '/public/stylesheet.css'
```

<Note>
  At the moment, we do not provide a detailed guide of all the available css
  classes. It is up to you to dig in the Web Inspector and find the css class
  you wish to override.
</Note>

Once the configuration is updated, restart the application. Your custom styling will now be applied.

## CSS Variables

Chainlit exposes CSS variables that let you customize specific UI elements without digging into class names.

### Stop Icon & Loading Cursor

You can override the appearance and animation of the stop button icon and the loading (blinking) cursor:

| Variable                     | Description                               | Default                  |
| ---------------------------- | ----------------------------------------- | ------------------------ |
| `--stop-icon-mask`           | SVG data URI for the stop icon shape      | Built-in square icon     |
| `--stop-icon-color`          | Stop icon color                           | `currentColor`           |
| `--stop-icon-animation`      | Stop icon CSS animation                   | `none`                   |
| `--loading-cursor-mask`      | SVG data URI for the loading cursor shape | Built-in circle          |
| `--loading-cursor-color`     | Loading cursor color                      | `hsl(var(--foreground))` |
| `--loading-cursor-size`      | Loading cursor size                       | `0.875rem`               |
| `--loading-cursor-animation` | Loading cursor CSS animation              | `pulse`                  |

```css theme={null}
:root {
    --stop-icon-animation: my-pulse 2s ease-in-out infinite;
    --loading-cursor-animation: my-breathe 2s ease-in-out infinite;
    --loading-cursor-size: 1.25rem;
}
@keyframes my-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.92); }
}
@keyframes my-breathe {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.85); }
}
```

<Note>
  Since version **2.11.0**.
</Note>


# JS
Source: https://docs.chainlit.io/customisation/custom-js



You can inject a custom JavaScript script into the application by adding the following to your `config.toml`:

```toml config.toml theme={null}
[UI]
# ...
# This can either be a css file in your `public` dir or a URL
custom_js = '/public/my_js_script.js'
```

Once the configuration is updated, restart the application. Your custom script will now be loaded.


# Logo and Favicon
Source: https://docs.chainlit.io/customisation/custom-logo-and-favicon



You can customize the Chainlit application with your own logo and favicon.

<Warning>
  Assets such as favicons and logos are cached by default by your browser. You
  might have to clear your browser cache to see the changes.
</Warning>

## Use your Logo

Chainlit Application offers support for both dark and light modes. To accommodate this, prepare two versions of your logo, named `logo_dark.png` and `logo_light.png`. Place these logos in a `/public` folder next to your application. Once you restart the application, your custom logos should be displayed accordingly.

<Card title="Custom Logo Example" icon="pied-piper-alt" href="https://github.com/Chainlit/cookbook/tree/main/custom-logo">
  Practical example of how to use custom logos in your Chainlit application.
</Card>

## Use your Favicon

To further enhance branding, you can also update the application's favicon. Place an image file named `favicon` in the `public` folder next to your application. After restarting the application, the new favicon will take effect.

## Customize Login Page Background image

If authentication is enabled, a background image (defaulting to the Chainlit logo) will be displayed on the login page.
You can customize it by editing the following fields of your `.chainlit/config.toml` file.

```toml config.toml theme={null}
[UI]
# Custom login page image, relative to public directory or external URL
login_page_image = "/public/custom-background.jpg"

# Custom login page image filter (Tailwind internal filters, no dark/light variants)
# login_page_image_filter = "brightness-50 grayscale"
# login_page_image_dark_filter = "contrast-200 blur-sm"
```


# Overview
Source: https://docs.chainlit.io/customisation/overview



You can tailor your Chainlit Application to reflect your organization's branding or personal style. Our intention is to provide a good level of customization to ensure a consistent user experience that aligns with your visual guidelines.

In this section we will go through the different options available.

<CardGroup>
  <Card title="Custom Logo and Favicon" icon="image" href="/customisation/custom-logo-and-favicon">
    Learn how to display your own logo and favicon
  </Card>

  <Card title="Custom CSS" icon="paint-roller" href="/customisation/custom-css">
    Learn how to provide your own CSS stylesheet.
  </Card>

  <Card title="Translation Files" icon="file-code" href="/customisation/translation">
    Learn how to navigate and modify translation files for UI text customization.
  </Card>

  <Card title="Theme" icon="palette" href="/customisation/theme">
    Learn about creating your own theme.
  </Card>
</CardGroup>


# Theme
Source: https://docs.chainlit.io/customisation/theme



Chainlit's theme is based on CSS variables.

To modify the CSS variables, create a `theme.json` file under `/public` with the following content.

You can check [Shadcn's documentation](https://ui.shadcn.com/docs/theming#list-of-variables) to learn about the role of each variable.

<Note>If the UI is not updated, try to empty your browser cache.</Note>

```json theme.json theme={null}
{
    "custom_fonts": [],
    "variables": {
        "light": {
            "--font-sans": "'Inter', sans-serif",
            "--font-mono": "source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace",
            "--background": "0 0% 100%",
            "--foreground": "0 0% 5%",
            "--card": "0 0% 100%",
            "--card-foreground": "0 0% 5%",
            "--popover": "0 0% 100%",
            "--popover-foreground": "0 0% 5%",
            "--primary": "340 92% 52%",
            "--primary-foreground": "0 0% 100%",
            "--secondary": "210 40% 96.1%",
            "--secondary-foreground": "222.2 47.4% 11.2%",
            "--muted": "0 0% 90%",
            "--muted-foreground": "0 0% 36%",
            "--accent": "0 0% 95%",
            "--accent-foreground": "222.2 47.4% 11.2%",
            "--destructive": "0 84.2% 60.2%",
            "--destructive-foreground": "210 40% 98%",
            "--border": "0 0% 90%",
            "--input": "0 0% 90%",
            "--ring": "340 92% 52%",
            "--radius": "0.75rem",
            "--sidebar-background": "0 0% 98%",
            "--sidebar-foreground": "240 5.3% 26.1%",
            "--sidebar-primary": "240 5.9% 10%",
            "--sidebar-primary-foreground": "0 0% 98%",
            "--sidebar-accent": "240 4.8% 95.9%",
            "--sidebar-accent-foreground": "240 5.9% 10%",
            "--sidebar-border": "220 13% 91%",
            "--sidebar-ring": "217.2 91.2% 59.8%"
        },
        "dark": {
            "--font-sans": "'Inter', sans-serif",
            "--font-mono": "source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace",
            "--background": "0 0% 13%",
            "--foreground": "0 0% 93%",
            "--card": "0 0% 18%",
            "--card-foreground": "210 40% 98%",
            "--popover": "0 0% 18%",
            "--popover-foreground": "210 40% 98%",
            "--primary": "340 92% 52%",
            "--primary-foreground": "0 0% 100%",
            "--secondary": "0 0% 19%",
            "--secondary-foreground": "210 40% 98%",
            "--muted": "0 1% 26%",
            "--muted-foreground": "0 0% 71%",
            "--accent": "0 0% 26%",
            "--accent-foreground": "210 40% 98%",
            "--destructive": "0 62.8% 30.6%",
            "--destructive-foreground": "210 40% 98%",
            "--border": "0 1% 26%",
            "--input": "0 1% 26%",
            "--ring": "340 92% 52%",
            "--sidebar-background": "0 0% 9%",
            "--sidebar-foreground": "240 4.8% 95.9%",
            "--sidebar-primary": "224.3 76.3% 48%",
            "--sidebar-primary-foreground": "0 0% 100%",
            "--sidebar-accent": "0 0% 13%",
            "--sidebar-accent-foreground": "240 4.8% 95.9%",
            "--sidebar-border": "240 3.7% 15.9%",
            "--sidebar-ring": "217.2 91.2% 59.8%"
        }
    }
}
```

As you may have noticed, the colors are not expressed in Hexadecimal but rather in HSL. This is mandatory.
You can easily [convert any color to HSL](https://www.google.com/search?q=hex+to+hsl).

The `custom_fonts` array can receive URLs (typically from google fonts) like:

```json theme={null}
custom_fonts: ["https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap"]
```


# Translation
Source: https://docs.chainlit.io/customisation/translation



Translation files are located in the `.chainlit/translations` directory. The files are named after the language code, e.g. `en-US.json` for English (United States).

<Note>
  The language is dynamically set for each user based on the language of the
  browser. The default language is `en-US`.
</Note>

## Customizing UI text

In addition to standard translations, you can customize the text of front-end components used within the UI. Each UI element is associated with a unique translation key in the translation files. By modifying these keys, you can personalize or localize the UI text according to your needs.

For example, to change the label of a navigation tab from "Readme" to "Documentation", locate the corresponding key in your translation file (e.g., `components.organisms.header.readme`) and update the value:

```json theme={null}
"components.organisms.header.readme": "Documentation"
```

## Customizing the chat watermark

The disclaimer text shown below the chat input ("LLMs can make mistakes. Check important info.") is defined under the `chat.watermark` key in your translation file:

```json theme={null}
"chat": {
  "watermark": "LLMs can make mistakes. [See our privacy policy](https://example.com/privacy)."
}
```

The watermark text supports Markdown, so you can add links (e.g. to a privacy policy or usage notes) and basic formatting like `**bold**` and `*italic*`.

<Note>
  Markdown in the watermark is supported since version **2.9.1**.
</Note>

## Built-in languages

Chainlit ships with translations for the following languages:

| Code    | Language                          |
| ------- | --------------------------------- |
| `ar-SA` | Arabic (Saudi Arabia)             |
| `bn`    | Bengali                           |
| `da-DK` | Danish (Denmark)                  |
| `de-DE` | German (Germany)                  |
| `el-GR` | Greek (Greece)                    |
| `en-US` | English (United States) — default |
| `es`    | Spanish                           |
| `fr-FR` | French (France)                   |
| `gu`    | Gujarati                          |
| `he-IL` | Hebrew (Israel)                   |
| `hi`    | Hindi                             |
| `it`    | Italian                           |
| `ja`    | Japanese                          |
| `kn`    | Kannada                           |
| `ko`    | Korean                            |
| `ml`    | Malayalam                         |
| `mr`    | Marathi                           |
| `nl`    | Dutch                             |
| `pt-PT` | Portuguese (Portugal)             |
| `ta`    | Tamil                             |
| `te`    | Telugu                            |
| `zh-CN` | Chinese (Simplified)              |
| `zh-TW` | Chinese (Traditional)             |

## Adding a new language

To add a new language, create a new file in the `.chainlit/translations` directory with the language code as the filename. The language code should be in the format of `languageCode-COUNTRYCODE`, e.g. `en-US` for English (United States) or `en-GB` for English (United Kingdom).

## Lint translations

To lint the translations, run the following command:

```bash theme={null}
chainlit lint-translations
```

## Translate chainlit.md file

You can define multiple translations for the `chainlit.md` file. For instance `chainlit_pt-BR.md` for Portuguese (Brazil) and `chainlit_es-ES.md` for Spanish (Spain).
The file will be loaded based on the browser's language, defaulting to `chainlit.md` if no translation is available.

## Resetting

To reset the the translations, remove the `.chainlit/translations` directory and restart your Chainlit application:

```bash theme={null}
chainlit run my-app.py
```


# DynamoDB Data Layer
Source: https://docs.chainlit.io/data-layers/dynamodb



This data layer also supports the `BaseStorageClient` that enables you to store your elements into AWS S3 or Azure Blob Storage.

## Example

Here is an example of setting up this data layer. First install boto3:

```bash theme={null}
pip install boto3
```

Import the custom data layer and storage client, and set the `cl_data._data_layer` variable at the beginning of your Chainlit app.

```python theme={null}
import chainlit.data as cl_data
from chainlit.data.dynamodb import DynamoDBDataLayer
from chainlit.data.storage_clients.s3 import S3StorageClient

storage_client = S3StorageClient(bucket="<Your Bucket>")

cl_data._data_layer = DynamoDBDataLayer(table_name="<Your Table>", storage_provider=storage_client)
```

## Table structure

Here is the Cloudformation used to create the dynamo table:

```json theme={null}
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "DynamoDBTable": {
      "Type": "AWS::DynamoDB::Table",
      "Properties": {
        "TableName": "<YOUR-TABLE-NAME>",
        "AttributeDefinitions": [
          {
            "AttributeName": "PK",
            "AttributeType": "S"
          },
          {
            "AttributeName": "SK",
            "AttributeType": "S"
          },
          {
            "AttributeName": "UserThreadPK",
            "AttributeType": "S"
          },
          {
            "AttributeName": "UserThreadSK",
            "AttributeType": "S"
          }
        ],
        "KeySchema": [
          {
            "AttributeName": "PK",
            "KeyType": "HASH"
          },
          {
            "AttributeName": "SK",
            "KeyType": "RANGE"
          }
        ],
        "GlobalSecondaryIndexes": [
          {
            "IndexName": "UserThread",
            "KeySchema": [
              {
                "AttributeName": "UserThreadPK",
                "KeyType": "HASH"
              },
              {
                "AttributeName": "UserThreadSK",
                "KeyType": "RANGE"
              }
            ],
            "Projection": {
              "ProjectionType": "INCLUDE",
              "NonKeyAttributes": ["id", "name"]
            }
          }
        ],
        "BillingMode": "PAY_PER_REQUEST"
      }
    }
  }
}
```

## Logging

DynamoDB data layer defines a child of chainlit logger.

```python theme={null}
import logging
from chainlit import logger

logger.getChild("DynamoDB").setLevel(logging.DEBUG)
```

## Limitations

Filtering by positive/negative feedback is not supported.

The data layer methods are not async. Boto3 is not async and therefore the data layer uses non-async blocking io.

## Design

This implementation uses Single Table Design. There are 4 different entity types in one table identified by the prefixes in PK & SK.

Here are the entity types:

```ts theme={null}
type User = {
    PK: "USER#{user.identifier}"
    SK: "USER"
    // ...PersistedUser
}

type Thread = {
    PK: f"THREAD#{thread_id}"
    SK: "THREAD"
    // GSI: UserThread for querying in list_threads
    UserThreadPK: f"USER#{user_id}"
    UserThreadSK: f"TS#{ts}"
    // ...ThreadDict
}

type Step = {
    PK: f"THREAD#{threadId}"
    SK: f"STEP#{stepId}"
    // ...StepDict

    // feedback is stored as part of step. 
    // NOTE: feedback.value is stored as Decimal in dynamo which is not json serializable
    feedback?: Feedback
}

type Element = {
    "PK": f"THREAD#{threadId}"
    "SK": f"ELEMENT#{element.id}"
    // ...ElementDict
}
```


# Official Data Layer
Source: https://docs.chainlit.io/data-layers/official



Follow the steps in this repository to persist your conversations in 2 minutes:

<Card title="Official Data Layer" icon="message" href="https://github.com/Chainlit/chainlit-datalayer">
  Out-of-the-box data layer schema to store your threads, steps, feedback, etc.
</Card>

<Warning>
  Do not forget to have your Chainlit application point to the database you set up by
  adding the `DATABASE_URL` environment variable in your `.env`.

  If you wish to store elements, the same goes for your files system configuration.
</Warning>

<Warning>
  The Official data layer Prisma schema has not been updated since Chainlit 2.0.0. If you are using Chainlit 2.1.0 or later, you need to manually add missing columns to the `"Step"` table. See the migration guides for [2.1.0](/guides/migration/2.1.0), [2.3.0](/guides/migration/2.3.0), and [2.9.4](/guides/migration/2.9.4).
</Warning>

<Tip>
  Custom element `props` are stored directly in PostgreSQL, not on cloud storage.
</Tip>


# Overview
Source: https://docs.chainlit.io/data-layers/overview



Choose one of the following options for your open source data layer:

* use the official Chainlit data layer (PostgreSQL + asyncpg)
* leverage a community-based data layer
* or build your own!

<CardGroup>
  <Card title="Official data layer" icon="check" href="/data-layers/official">
    The official Chainlit data layer
  </Card>

  <Card title="Community SQLAlchemy data layer" icon="database" href="/data-layers/sqlalchemy">
    The community SQLAlchemy data layer
  </Card>

  <Card title="Community DynamoDB data layer" icon="database" href="/data-layers/dynamodb">
    The community DynamoDB data layer
  </Card>

  <Card title="Custom data layer API" icon="text" href="/api-reference/data-persistence/custom-data-layer">
    The custom data layer implementation reference
  </Card>
</CardGroup>

## Official data layer

When using the [official data layer](/data-layers/official), just add the `DATABASE_URL` variable to your `.env` and
a cloud storage configuration if relevant.

## Community data layers

For community data layers, you need to import the corresponding data layer in your chainlit app.
Here is how you would do it with `SQLAlchemyDataLayer`:

```python theme={null}
import chainlit as cl

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(conninfo="...")
```

## Custom data layers

Follow the [reference](/api-reference/data-persistence/custom-data-layer) for an exhaustive list of the methods your custom data layer needs to implement.

## Cloud Storage Providers supported out-of-the-box

* AWS S3
  * LocalStack via `DEV_AWS_ENDPOINT` environment variable
* Azure
  * Blob Storage
  * Data Lake Storage (ADLS) Gen2
* Google Cloud Storage
  * via Private Key
  * via Application Default Credentials (e.g. in Google Cloud Run)


# SQLAlchemy Data Layer
Source: https://docs.chainlit.io/data-layers/sqlalchemy



This custom layer has been tested for PostgreSQL, however it should support more SQL databases thanks to the use of the SQL Alchemy database.

This data layer also supports the `BaseStorageClient` that enables you to store your elements into Azure Blob Storage or AWS S3.

<Warning>
  The schema below reflects the latest version of Chainlit. If you are upgrading from an earlier version, three columns have been added to the `steps` table since 2.0.0:

  | Column        | Since | Migration guide                             |
  | ------------- | ----- | ------------------------------------------- |
  | `command`     | 2.1.0 | [Migrate to 2.1.0](/guides/migration/2.1.0) |
  | `defaultOpen` | 2.3.0 | [Migrate to 2.3.0](/guides/migration/2.3.0) |
  | `modes`       | 2.9.4 | [Migrate to 2.9.4](/guides/migration/2.9.4) |
</Warning>

Here is the SQL used to create the schema for this data layer:

```sql theme={null}
CREATE TABLE users (
    "id" UUID PRIMARY KEY,
    "identifier" TEXT NOT NULL UNIQUE,
    "metadata" JSONB NOT NULL,
    "createdAt" TEXT
);

CREATE TABLE IF NOT EXISTS threads (
    "id" UUID PRIMARY KEY,
    "createdAt" TEXT,
    "name" TEXT,
    "userId" UUID,
    "userIdentifier" TEXT,
    "tags" TEXT[],
    "metadata" JSONB,
    FOREIGN KEY ("userId") REFERENCES users("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS steps (
    "id" UUID PRIMARY KEY,
    "name" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "threadId" UUID NOT NULL,
    "parentId" UUID,
    "streaming" BOOLEAN NOT NULL,
    "waitForAnswer" BOOLEAN,
    "isError" BOOLEAN,
    "metadata" JSONB,
    "tags" TEXT[],
    "input" TEXT,
    "output" TEXT,
    "createdAt" TEXT,
    "command" TEXT,
    "start" TEXT,
    "end" TEXT,
    "generation" JSONB,
    "showInput" TEXT,
    "language" TEXT,
    "indent" INT,
    "defaultOpen" BOOLEAN,
    "modes" JSONB,
    FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS elements (
    "id" UUID PRIMARY KEY,
    "threadId" UUID,
    "type" TEXT,
    "url" TEXT,
    "chainlitKey" TEXT,
    "name" TEXT NOT NULL,
    "display" TEXT,
    "objectKey" TEXT,
    "size" TEXT,
    "page" INT,
    "language" TEXT,
    "forId" UUID,
    "mime" TEXT,
    "props" JSONB,
    FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedbacks (
    "id" UUID PRIMARY KEY,
    "forId" UUID NOT NULL,
    "threadId" UUID NOT NULL,
    "value" INT NOT NULL,
    "comment" TEXT,
    FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
);
```

## Example

Here is an example of setting up this data layer on a PostgreSQL database with an Azure storage client. First install the required dependencies:

```bash theme={null}
pip install asyncpg SQLAlchemy azure-identity azure-storage-file-datalake aiohttp greenlet
```

Import the custom data layer and storage client, and indicate which data layer to use with `@cl.data_layer` at the beginning of your Chainlit app:

```python theme={null}
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.data.storage_clients.azure import AzureStorageClient

storage_client = AzureStorageClient(account_url="<your_account_url>", container="<your_container>")

@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(conninfo="<your conninfo>", storage_provider=storage_client)
```

Note that you need to add `+asyncpg` to the protocol in the `conninfo` string so that it uses the asyncpg library.


# Human Feedback
Source: https://docs.chainlit.io/data-persistence/feedback



Human feedback is a crucial part of developing your LLM app or agent.

It allows your users to provide direct feedback on the interaction, which can be used to improve the performance and accuracy of your system.

By enabling data persistence, each run triggered by a user input will be accompanied by thumbs up and thumbs down icons. Users can also add a text comment to their feedback for more detailed input.

<Frame>
  <img />
</Frame>

## Benefits

* **Dataset Creation:** Feedback interactions implicitly generate valuable training data to improve the agent's responses over time.

* **Accuracy Measurement:** Feedback scores enable objective measurement and comparison of different agent versions, facilitating continuous model improvement.

* **User-Centric Development:** Direct feedback promotes a user-centric approach, ensuring the model evolves to meet user needs and expectations.

* **Training and Fine-Tuning:** Human feedback allows for direct model training and fine-tuning based on specific interactions.

## How-to

To use human feedback, you first need to enable [data persistence](/data-persistence/overview).

<Frame>
  <img />
</Frame>

## Conclusion

Human feedback is a powerful tool for improving the performance of your LLM app. By enabling data persistence and collecting feedback, you can create a dataset that can be used to improve the system's accuracy.


# Chat History
Source: https://docs.chainlit.io/data-persistence/history



Chat history allow users to search, browse and resume their past conversations.

If data persistence is enabled but the user is not authenticated, the conversations will be stored but users won't be able to see the chat history.

You need both data persistence and [authentication](/authentication) configured to enable the chat history.

<Frame>
  <img />
</Frame>

## Resume a conversation

To let users continue persisted conversations, use [cl.on\_chat\_resume](/api-reference/lifecycle-hooks/on-chat-resume).

<Frame>
  <img />
</Frame>


# Overview
Source: https://docs.chainlit.io/data-persistence/overview



By default, your Chainlit app does not persist the chats and elements it generates. However, the ability to store and utilize this data can be a crucial part of your project or organization.

## Enable Data Persistence

To enable data persistence in your Chainlit app, you have several options:

<CardGroup>
  <Card title="Open Source Data Layer" icon="toolbox" href="/data-layers/overview">
    Use the official Chainlit data layer, leverage a community data layer or build your own.
  </Card>
</CardGroup>


# Tags & Metadata
Source: https://docs.chainlit.io/data-persistence/tags-metadata



Tags and metadata provide valuable context for your threads, steps and generations.

```py theme={null}
@cl.step(type="run")
async def func(input):
    # some code
    cl.context.current_step.metadata = {"experiment":"1"}
    cl.context.current_step.tags = ["to review"]
    # some code
    return output
```


# Copilot
Source: https://docs.chainlit.io/deploy/copilot



Software Copilot are a new kind of assistant embedded in your app/product. They are designed to help users get the most out of your app by providing contextual guidance and take actions on their behalf.

<Frame>
  <img />
</Frame>

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ✅         | ✅        | ✅     | ✅        | ✅            | ✅             | ✅        |

## Embedding the Copilot

First, make sure your Chainlit server is running. Then, add the following script at the end of your website's `<body>` tag:

<Note>
  This example assumes your Chainlit server is running on
  `http://localhost:8000`
</Note>

```html theme={null}
<head>
  <meta charset="utf-8" />
</head>
<body>
  <!-- ... -->
  <script src="http://localhost:8000/copilot/index.js"></script>
  <script>
    window.addEventListener("chainlit-call-fn", (e) => {
      const { name, args, callback } = e.detail;
      callback("You sent: " + args.msg);
    });
  </script>
  <script>
    window.mountChainlitWidget({
      chainlitServer: "http://localhost:8000",
    });
  </script>
</body>
```

<Warning>
  Remember the HTML file has to be served by a server, opening it directly in
  your browser won't work. You can use simple HTTP server for tests purpose.
</Warning>

That's it! You should now see a floating button on the bottom right corner of your website. Clicking on it will open the Copilot.

You can programmatically toggle the copilot with `window.toggleChainlitCopilot()`.

## Thread Persistence

The Copilot now supports persistent storage of the `threadId` in the browser's localStorage, enabling chat restoration after a page reload. This feature provides two JavaScript utility functions for managing thread persistence:

### getChainlitCopilotThreadId()

Retrieves the current threadId from localStorage.

**Returns:** `string | null` - The current threadId or null if not found

```javascript theme={null}
const threadId = window.getChainlitCopilotThreadId();
console.log("Current thread ID:", threadId);
```

### clearChainlitCopilotThreadId(newThreadId?)

Clears the existing threadId from localStorage. Optionally sets a new one.

**Parameters:**

* `newThreadId?` (optional): `string` - A new threadId to set after clearing

```javascript theme={null}
// Start a new thread programmatically
window.clearChainlitCopilotThreadId();

// Or with predefined ID
const newThreadId = crypto.randomUUID();
window.clearChainlitCopilotThreadId(newThreadId);
```

These functions provide developers with greater control over thread management and session continuity in the Copilot experience.

## Widget Configuration

The `mountChainlitWidget` function accepts the following options:

```ts theme={null}
export interface IWidgetConfig {
  // URL of the Chainlit server
  chainlitServer: string;
  // Required if authentication is enabled on the server
  accessToken?: string;
  // Theme of the copilot
  theme?: "light" | "dark";
  // Display mode: "floating" popover (default) or "sidebar" full-height panel
  displayMode?: "floating" | "sidebar";
  // Custom styling to apply to the widget button
  button?: {
    // ID of the container element to mount the button to
    containerId?: string;
    // URL of the image to use as the button icon
    imageUrl?: string;
    // The tailwind classname to apply to the button
    className?: string;
  };
  // Custom CSS styles in copilot
  customCssUrl?: string;
  // Allows passing extra query parameters in API requests to the Chainlit server
  additionalQueryParamsForAPI?: Record<string, string>;
  // Start widget container expanded, i.e. wide
  expanded?: boolean;
  // Set language of Chainlit's UI
  // Defaults to preferred language of the user
  // via navigator.language, then to en-US
  language?: string;
  // Start with the copilot chat panel open
  opened?: boolean;
}
```

## Sidebar Mode

By default the copilot renders as a floating popover. Set `displayMode` to `"sidebar"` to render it as a full-height side panel anchored to the right edge of the viewport. The panel pushes the host page content to make room and includes a drag handle on its left edge for resizing (300 px min, 50 % viewport max).

Users can switch between sidebar and floating modes via a dropdown in the copilot header. The selected mode and sidebar width are persisted in `localStorage` across sessions. An explicit `displayMode` in `mountChainlitWidget()` takes priority over the stored value.

```js theme={null}
window.mountChainlitWidget({
  chainlitServer: "http://localhost:8000",
  displayMode: "sidebar",
});
```

<Note>
  Since version **2.11.0**.
</Note>

## Function Calling

The Copilot can call functions on your website. This is useful for taking actions on behalf of the user. For example, you can call a function to create a new document, or to open a modal.

First, create a `CopilotFunction` in your Chainlit server:

```py theme={null}
import chainlit as cl


@cl.on_message
async def on_message(msg: cl.Message):
    if cl.context.session.client_type == "copilot":
        fn = cl.CopilotFunction(name="test", args={"msg": msg.content})
        res = await fn.acall()
        await cl.Message(content=res).send()
```

Then, in your app/website, add the following event listener:

```js theme={null}
window.addEventListener("chainlit-call-fn", (e) => {
  const { name, args, callback } = e.detail;
  if (name === "test") {
    console.log(name, args);
    callback("You sent: " + args.msg);
  }
});
```

As you can see, the event listener receives the function name, arguments, and a callback function. The callback function should be called with the result of the function call.

## Send a Message

The Copilot can also send messages directly to the Chainlit server. This is useful for sending context information or user actions to the Chainlit server (like the user selected from cell A1 to B1 on a table).

First, update the `@cl.on_message` decorated function to your Chainlit server:

```py theme={null}
import chainlit as cl


@cl.on_message
async def on_message(msg: cl.Message):
    if cl.context.session.client_type == "copilot":

        if msg.type == "system_message":
          # do something with the message
          return

        fn = cl.CopilotFunction(name="test", args={"msg": msg.content})
        res = await fn.acall()
        await cl.Message(content=res).send()
```

Then, in your app/website, you can emit an event like this:

```js theme={null}
window.sendChainlitMessage({
  type: "system_message",
  output: "Hello World!",
});
```

## Security

### Cross Origin Resource Sharing (CORS)

Don't forget to add the origin of the host website to the [allow\_origins](/backend/config/project) config field to a list of allowed origins.

### Authentication

If you want to authenticate users on the Copilot, you can enable [authentication](/authentication) on the Chainlit server.

<Warning>
  If the Chainlit app and the host website are deployed on different domains,
  you will have to add `CHAINLIT_COOKIE_SAMESITE=none` to the Chainlit app env
  variables.
</Warning>

While the standalone Chainlit application handles the authentication process, the Copilot needs to be configured with an access token. This token is used to authenticate the user with the Chainlit server.

The host app/website is responsible for generating the token and passing it to the as `accessToken`. Here are examples of how to generate the token in different languages:

<Note>
  You will need the `CHAINLIT_AUTH_SECRET` you generated when [configuring
  authentication](/authentication).
</Note>

<CodeGroup>
  ```py jwt.py theme={null}
  import jwt
  from datetime import datetime, timedelta

  CHAINLIT_AUTH_SECRET = "your-secret"

  def create_jwt(identifier: str, metadata: dict) -> str:
      to_encode = {
        "identifier": identifier,
        "metadata": metadata,
        "exp": datetime.utcnow() + timedelta(minutes=60 * 24 * 15),  # 15 days
        }

      encoded_jwt = jwt.encode(to_encode, CHAINLIT_AUTH_SECRET, algorithm="HS256")
      return encoded_jwt

  access_token = create_jwt("user-1", {"name": "John Doe"})
  ```

  ```ts jwt.ts theme={null}
  import jwt from "jsonwebtoken";

  const CHAINLIT_AUTH_SECRET = "your-secret";

  interface Metadata {
    [key: string]: any;
  }

  function createJwt(identifier: string, metadata: Metadata): string {
    const toEncode = {
      identifier: identifier,
      metadata: metadata,
      exp: Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 15, // 15 days
    };
    const encodedJwt = jwt.sign(toEncode, CHAINLIT_AUTH_SECRET, {
      algorithm: "HS256",
    });
    return encodedJwt;
  }

  const accessToken = createJwt("user-1", { name: "John Doe" });
  ```
</CodeGroup>


# Discord
Source: https://docs.chainlit.io/deploy/discord



To make your Chainlit app available on Discord, you will need to create a Discord app and set up the necessary environment variables.

## How it Works

The Discord bot will listen to messages mentioning it in channels and direct messages.
It will send replies to a dedicated thread or DM depending on the context.

<Frame>
  <img />
</Frame>

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ❌         | ✅        | ❌     | ❌        | ✅            | ❌             | ✅        |

## Install the Discord Library

The Discord library is not included in the Chainlit dependencies. You will have to install it manually.

```bash theme={null}
pip install discord
```

## Create a Discord App

To start, navigate to the [Discord apps dashboard](https://discord.com/developers/applications). Here, you should find a button that says New Application. When you click this button, select the option to create your app from scratch.

<Frame>
  <img />
</Frame>

## Set the Environment Variables

Navigate to the Bot tab and click on `Reset Token`. This will make the token visible. Copy it and set it as an environment variable in your Chainlit app.

<Frame>
  <img />
</Frame>

```bash theme={null}
DISCORD_BOT_TOKEN=your_bot_token
```

## Set Intents

Navigate to the Bot tab and enable the `MESSAGE CONTENT INTENT`, then click on Save Changes.

<Frame>
  <img />
</Frame>

## Working Locally

If you are working locally, you will have to expose your local Chainlit app to the internet to receive incoming messages to Discord. You can use [ngrok](https://ngrok.com/) for this.

```bash theme={null}
ngrok http 8000
```

## Start the Chainlit App

Since the Chainlit app is not running, the Discord bot will not be able to communicate with it.

For the example, we will use this simple app:

```python my_app.py theme={null}
import chainlit as cl

@cl.on_message
async def on_message(msg: cl.Message):
    # Access the original discord message
    print(cl.user_session.get("discord_message"))
    # Access the discord user
    print(cl.user_session.get("user"))

    # Access potential attached files
    attached_files = msg.elements

    await cl.Message(content="Hello World").send()
```

Start the Chainlit app.

<Note>
  Using -h to not open the default Chainlit UI since we are using Discord.
</Note>

```bash theme={null}
chainlit run my_app.py -h
```

## Install the Discord Bot to Your Workspace

Navigate to the OAuth2 tab. In the OAuth2 URL Generator, select the `bot` scope.

<Frame>
  <img />
</Frame>

Then, in the Bot Permissions section, select the following permissions.

<Note>
  You can check that you have selected the right permissions by looking at the
  number of permissions parameter of the URL. It should be `377957238848`.
</Note>

<Frame>
  <img />
</Frame>

Copy the generated URL and paste it in your browser. You will be prompted to add the bot to a server. Select the server you want to add the bot to.

That's it! You should now be able to interact with your Chainlit app through Discord.

## Chat History

Chat history is directly available through discord.

```python theme={null}
from chainlit.discord.app import client as discord_client

import chainlit as cl
import discord

@cl.on_message
async def on_message(msg: cl.Message):
    # The user session resets on every Discord message.
    # So we add previous chat messages manually.
    messages = cl.user_session.get("messages", [])
    channel: discord.abc.MessageableChannel = cl.user_session.get("discord_channel")

    if channel:
        cl.user_session.get("messages")
        discord_messages = [message async for message in channel.history(limit=10)]

        # Go through last 10 messages and remove the current message.
        for x in discord_messages[::-1][:-1]:
            messages.append({
                "role": "assistant" if x.author.name == discord_client.user.name else "user",
                "content": x.clean_content if x.clean_content else x.channel.name # first message is empty
            })

    # Your code here
```


# Overview
Source: https://docs.chainlit.io/deploy/overview



A Chainlit application can be consumed through multiple platforms. Write your assistant logic once, use everywhere!

## Available Platforms

<CardGroup>
  <Card title="Web App" href="/deploy/webapp" icon="browser">
    The native Chainlit UI. Available on port 8000.
  </Card>

  <Card title="Copilot" icon="sparkles" href="/deploy/copilot">
    Embed your Chainlit app on any website as a Copilot.
  </Card>

  <Card title="Custom React App" icon="react" href="/deploy/react">
    Learn how to integrate your custom React frontend with the Chainlit backend.
  </Card>

  <Card
    title="Teams"
    href="/deploy/teams"
    icon={
<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
  <path
    fill="#5059C9"
    d="M10.765 6.875h3.616c.342 0 .619.276.619.617v3.288a2.272 2.272 0 01-2.274 2.27h-.01a2.272 2.272 0 01-2.274-2.27V7.199c0-.179.145-.323.323-.323zM13.21 6.225c.808 0 1.464-.655 1.464-1.462 0-.808-.656-1.463-1.465-1.463s-1.465.655-1.465 1.463c0 .807.656 1.462 1.465 1.462z"
  />
  <path
    fill="#7B83EB"
    d="M8.651 6.225a2.114 2.114 0 002.117-2.112A2.114 2.114 0 008.65 2a2.114 2.114 0 00-2.116 2.112c0 1.167.947 2.113 2.116 2.113zM11.473 6.875h-5.97a.611.611 0 00-.596.625v3.75A3.669 3.669 0 008.488 15a3.669 3.669 0 003.582-3.75V7.5a.611.611 0 00-.597-.625z"
  />
  <path
    fill="#000000"
    d="M8.814 6.875v5.255a.598.598 0 01-.596.595H5.193a3.951 3.951 0 01-.287-1.476V7.5a.61.61 0 01.597-.624h3.31z"
    opacity=".1"
  />
  <path
    fill="#000000"
    d="M8.488 6.875v5.58a.6.6 0 01-.596.595H5.347a3.22 3.22 0 01-.267-.65 3.951 3.951 0 01-.172-1.15V7.498a.61.61 0 01.596-.624h2.985z"
    opacity=".2"
  />
  <path
    fill="#000000"
    d="M8.488 6.875v4.93a.6.6 0 01-.596.595H5.08a3.951 3.951 0 01-.172-1.15V7.498a.61.61 0 01.596-.624h2.985z"
    opacity=".2"
  />
  <path
    fill="#000000"
    d="M8.163 6.875v4.93a.6.6 0 01-.596.595H5.079a3.951 3.951 0 01-.172-1.15V7.498a.61.61 0 01.596-.624h2.66z"
    opacity=".2"
  />
  <path
    fill="#000000"
    d="M8.814 5.195v1.024c-.055.003-.107.006-.163.006-.055 0-.107-.003-.163-.006A2.115 2.115 0 016.593 4.6h1.625a.598.598 0 01.596.594z"
    opacity=".1"
  />
  <path
    fill="#000000"
    d="M8.488 5.52v.699a2.115 2.115 0 01-1.79-1.293h1.195a.598.598 0 01.595.594z"
    opacity=".2"
  />
  <path
    fill="#000000"
    d="M8.488 5.52v.699a2.115 2.115 0 01-1.79-1.293h1.195a.598.598 0 01.595.594z"
    opacity=".2"
  />
  <path
    fill="#000000"
    d="M8.163 5.52v.647a2.115 2.115 0 01-1.465-1.242h.87a.598.598 0 01.595.595z"
    opacity=".2"
  />
  <path
    fill="url(#microsoft-teams-color-16__paint0_linear_2372_494)"
    d="M1.597 4.925h5.969c.33 0 .597.267.597.596v5.958a.596.596 0 01-.597.596h-5.97A.596.596 0 011 11.479V5.521c0-.33.267-.596.597-.596z"
  />
  <path
    fill="#ffffff"
    d="M6.152 7.193H4.959v3.243h-.76V7.193H3.01v-.63h3.141v.63z"
  />
  <defs>
    <linearGradient
      id="microsoft-teams-color-16__paint0_linear_2372_494"
      x1="2.244"
      x2="6.906"
      y1="4.46"
      y2="12.548"
      gradientUnits="userSpaceOnUse"
    >
      <stop stopColor="#5A62C3" />
      <stop offset=".5" stopColor="#4D55BD" />
      <stop offset="1" stopColor="#3940AB" />
    </linearGradient>
  </defs>
</svg>
}
  >
    Make your Chainlit app available on Teams.
  </Card>

  <Card
    title="Slack"
    icon={
<svg
  enableBackground="new 0 0 2447.6 2452.5"
  viewBox="0 0 2447.6 2452.5"
  xmlns="http://www.w3.org/2000/svg"
>
  <g clipRule="evenodd" fillRule="evenodd">
    <path
      d="m897.4 0c-135.3.1-244.8 109.9-244.7 245.2-.1 135.3 109.5 245.1 244.8 245.2h244.8v-245.1c.1-135.3-109.5-245.1-244.9-245.3.1 0 .1 0 0 0m0 654h-652.6c-135.3.1-244.9 109.9-244.8 245.2-.2 135.3 109.4 245.1 244.7 245.3h652.7c135.3-.1 244.9-109.9 244.8-245.2.1-135.4-109.5-245.2-244.8-245.3z"
      fill="#36c5f0"
    />
    <path
      d="m2447.6 899.2c.1-135.3-109.5-245.1-244.8-245.2-135.3.1-244.9 109.9-244.8 245.2v245.3h244.8c135.3-.1 244.9-109.9 244.8-245.3zm-652.7 0v-654c.1-135.2-109.4-245-244.7-245.2-135.3.1-244.9 109.9-244.8 245.2v654c-.2 135.3 109.4 245.1 244.7 245.3 135.3-.1 244.9-109.9 244.8-245.3z"
      fill="#2eb67d"
    />
    <path
      d="m1550.1 2452.5c135.3-.1 244.9-109.9 244.8-245.2.1-135.3-109.5-245.1-244.8-245.2h-244.8v245.2c-.1 135.2 109.5 245 244.8 245.2zm0-654.1h652.7c135.3-.1 244.9-109.9 244.8-245.2.2-135.3-109.4-245.1-244.7-245.3h-652.7c-135.3.1-244.9 109.9-244.8 245.2-.1 135.4 109.4 245.2 244.7 245.3z"
      fill="#ecb22e"
    />
    <path
      d="m0 1553.2c-.1 135.3 109.5 245.1 244.8 245.2 135.3-.1 244.9-109.9 244.8-245.2v-245.2h-244.8c-135.3.1-244.9 109.9-244.8 245.2zm652.7 0v654c-.2 135.3 109.4 245.1 244.7 245.3 135.3-.1 244.9-109.9 244.8-245.2v-653.9c.2-135.3-109.4-245.1-244.7-245.3-135.4 0-244.9 109.8-244.8 245.1 0 0 0 .1 0 0"
      fill="#e01e5a"
    />
  </g>
</svg>
}
    href="/deploy/slack"
  >
    Make your Chainlit app available on Slack.
  </Card>

  <Card
    title="Discord"
    href="/deploy/discord"
    icon={
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 127.14 96.36"><path fill="#5865f2" d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"/></svg>
}
  >
    Make your Chainlit app available on Discord.
  </Card>
</CardGroup>

## Tips & Tricks

### Start Chainlit with -h

When running a Chainlit app in production, you should always add `-h` to the
`chainlit run` command. Otherwise a browser window will be opened server side
and might break your deployment.

### Double check the host

By default, the Chainlit server host is `127.0.0.1`.
Typically, if you are running Chainlit on docker, you want to add `--host 0.0.0.0` to your chainlit command.

### Account for websockets

Chainlit is built upon websockets, which means the service you deploy your app
to has to support them. When auto scaling, make sure to enable sticky sessions (or session affinity).

Even with sticky sessions, load balancers sometime struggle to consistently route a client to the same container.
In that case you can set `transports = ["websocket"]` in your `.chainlit/config.toml` file.

### Deploying Chainlit on a subpath

If you need to deploy your Chainlit app to a subpath like
`https://my-app.com/chainlit`, you will need to set the `--root-path
/chainlit` flag when running the `chainlit run` command. This will ensure that
the app is served from the correct path.

### Cross origins

If your end users consumes the Chainlit UI from the same origin as the server, everything will work out of the box.
However, if you embed Chainlit on a website, the connection will fail because of CORS.

In that case, you will have to update the `allow_origins` field of your `.chainlit/config.toml`.

## Community resource

After you've successfully set up and tested your Chainlit application locally, the next step is to make it accessible to a wider audience by deploying it to a hosting service. This guide provides various options for self-hosting your Chainlit app.

* on [Ploomber Cloud](https://docs.cloud.ploomber.io/en/latest/apps/chainlit.html)
* on [AWS](https://ankushgarg.super.site/how-to-deploy-your-chatgpt-like-app-with-chainlit-and-aws-ecs)
* on [Azure Container](https://techcommunity.microsoft.com/t5/fasttrack-for-azure/create-an-azure-openai-langchain-chromadb-and-chainlit-chat-app/ba-p/3885602)
* on [Google Cloud Run](https://pseudohvr.medium.com/deploying-chainlit-on-gcp-72231ba6b77f)
* on [Google App Engine](https://github.com/amjadraza/langchain-chainlit-docker-deployment-template)
* on [Replit](https://replit.com/@DanConstantini/Build-a-Chatbot-with-OpenAI-LangChain-and-Chainlit?v=1)
* on [Render](https://discord.com/channels/1088038867602526210/1126834266504966294/1126845898287230977)
* on [Fly.io](https://dev.to/willydouhard/how-to-deploy-your-chainlit-app-to-flyio-38ja)
* on [HuggingFace Spaces](https://github.com/Chainlit/cookbook/tree/main/chroma-qa-chat)


# Additional resources
Source: https://docs.chainlit.io/deploy/react/additional-resources



## Additional Resources

* [@chainlit/react-client npm package](https://www.npmjs.com/package/@chainlit/react-client)\
  Explore the @chainlit/react-client npm package.

* [Recoil Documentation](https://recoiljs.org/docs/introduction/getting-started)\
  Learn more about setting up and using Recoil for state management in React applications.

* [SWR Documentation](https://swr.vercel.app/)\
  Discover how to leverage SWR for data fetching, caching, and revalidation in React applications.

* [Socket.IO Documentation](https://socket.io/docs/v4/)\
  Understand how real-time communication is handled via Socket.IO, integral to the `useChatInteract` hook's operations.

* [JWT Documentation](https://jwt.io/introduction/)\
  Learn about JSON Web Tokens (JWT) and how they are used for secure authentication.


# Installation and setup
Source: https://docs.chainlit.io/deploy/react/installation-and-setup



## Overview

The `@chainlit/react-client` package provides a set of React hooks as well as an API client to connect to your **Chainlit** application from any React application. The package includes hooks for managing chat sessions, messages, data, and interactions.

## Installation

To install the package, run the following command in your project directory:

```bash theme={null}
npm install @chainlit/react-client
```

This package uses **Recoil** to manage its state. This means you will have to wrap your application in a recoil provider:

```typescript theme={null}
import React from 'react';
import ReactDOM from 'react-dom/client';
import { RecoilRoot } from 'recoil';

import { ChainlitAPI, ChainlitContext } from '@chainlit/react-client';

const CHAINLIT_SERVER_URL = 'http://localhost:8000';

const apiClient = new ChainlitAPI(CHAINLIT_SERVER_URL, 'webapp');

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ChainlitContext.Provider value={apiClient}>
      <RecoilRoot>
        <MyApp />
      </RecoilRoot>
    </ChainlitContext.Provider>
  </React.StrictMode>
);
```


# Overview
Source: https://docs.chainlit.io/deploy/react/overview



Chainlit allows you to create a custom frontend for your application, offering you the flexibility to design a unique user experience. By integrating your frontend with Chainlit's backend, you can harness the full power of Chainlit's features, including:

* Abstractions for easier development
* Monitoring and observability
* Seamless integrations with various tools
* Robust authentication mechanisms
* Support for multi-user environments
* Efficient data streaming capabilities

<CardGroup>
  <Card title="Installation and Setup" icon="gear" href="/deploy/react/installation-and-setup">
    Learn how to install and set up the Chainlit React client.
  </Card>

  <Card title="Usage" icon="bolt" href="/deploy/react/usage">
    Explore the key features provided by the React client.
  </Card>

  <Card title="Additional Resources" icon="flag" href="/deploy/react/additional-resources">
    Explore additional resources for the React client.
  </Card>

  <Card title="Custom React frontend" icon="react" href="https://github.com/Chainlit/cookbook/tree/main/custom-frontend">
    Learn how to integrate your custom React frontend with the Chainlit backend.
  </Card>
</CardGroup>

The [@chainlit/react-client](https://www.npmjs.com/package/@chainlit/react-client) package is designed for integrating Chainlit applications with React. It offers several hooks and an API client for seamless connection and interaction.

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ✅         | ✅        | ✅     | ✅        | ✅            | ✅             | ✅        |


# Usage
Source: https://docs.chainlit.io/deploy/react/usage



## React Hooks

The `@chainlit/react-client` package provides several React hooks to manage various aspects of your chat application seamlessly:

* **[`useChatSession`](#usechatsession-hook)**: Manages the chat session's connection to the WebSocket server.
* **[`useChatMessages`](#usechatmessages-hook)**: Manages retrieval and rendering of chat messages.
* **[`useChatData`](#usechatdata-hook)**: Accesses chat-related data and states.
* **[`useChatInteract`](#usechatinteract-hook)**: Provides methods to interact with the chat system.
* **[`useAuth`](#useauth-hook)**: Handles authentication processes.
* **[`useApi`](#useapi-hook)**: Simplifies API interactions with built-in support for data fetching and error handling.

***

### `useChatSession` Hook

This hook is responsible for managing the chat session's connection to the WebSocket server.

#### Methods

* **`connect`**: Establishes a connection to the WebSocket server.
* **`disconnect`**: Disconnects from the WebSocket server.
* **`setChatProfile`**: Sets the chat profile state.

#### Example

```tsx theme={null}
import { useChatSession } from '@chainlit/react-client';

const ChatComponent = () => {
  const { connect, disconnect, chatProfile, setChatProfile } = useChatSession();

  // Connect to the WebSocket server
  useEffect(() => {
    connect({
      userEnv: {
        /* user environment variables */
      },
      accessToken: 'Bearer YOUR ACCESS TOKEN', // Optional Chainlit auth token
    });

    return () => {
      disconnect();
    };
  }, []);

  // Rest of your component logic
};
```

***

### `useChatMessages` Hook

The `useChatMessages` hook provides access to the current chat messages, the first user interaction, and the active thread ID within your React application. It leverages Recoil for state management, ensuring that your components reactively update in response to state changes.

#### Returned Values

* **`threadId`** (`string | undefined`):\
  The identifier of the current chat thread.
* **`messages`** (`IStep[]`):\
  An array of chat messages.
* **`firstInteraction`** (`string | undefined`):\
  The content of the first user-initiated interaction.

#### Example

```tsx theme={null}
import { useChatMessages } from '@chainlit/react-client';

const MessagesComponent = () => {
  const { messages, firstInteraction, threadId } = useChatMessages();

  return (
    <div>
      <h2>Thread ID: {threadId}</h2>
      {firstInteraction && <p>First Interaction: {firstInteraction}</p>}
      {messages.map((message) => (
        <p key={message.id}>{message.content}</p>
      ))}
    </div>
  );
};
```

***

### `useChatData` Hook

The `useChatData` hook offers comprehensive access to various chat-related states and data within your React application.

#### Returned Properties

* **`actions`** (`IAction[]`)
* **`askUser`** (`IAsk | undefined`)
* **`chatSettingsValue`** (`any`)
* **`connected`** (`boolean`)
* **`disabled`** (`boolean`)
* **`error`** (`boolean | undefined`)
* **`loading`** (`boolean`)
* **`tasklists`** (`ITasklistElement[]`)

#### Example

```tsx theme={null}
import { useChatData } from '@chainlit/react-client';

const ChatStatusComponent = () => {
  const { connected, loading, error, actions, askUser, chatSettingsValue } = useChatData();

  return (
    <div>
      <h2>Chat Status</h2>
      {loading && <p>Loading chat...</p>}
      {error && <p>There was an error with the chat session.</p>}
      <p>{connected ? 'Connected to chat.' : 'Disconnected from chat.'}</p>

      <h3>Available Actions</h3>
      <ul>
        {actions.map((action) => (
          <li key={action.id}>{action.name}</li>
        ))}
      </ul>

      {askUser && (
        <div>
          <h3>User Prompt</h3>
          <p>{askUser.message}</p>
        </div>
      )}

      <h3>Chat Settings</h3>
      <pre>{JSON.stringify(chatSettingsValue, null, 2)}</pre>
    </div>
  );
};
```

***

### `useChatInteract` Hook

The `useChatInteract` hook provides a comprehensive set of methods to interact with the chat system within your React application.

#### Methods

* **`sendMessage`**
* **`replyMessage`**
* **`clear`**
* **`uploadFile`**
* **`callAction`**
* **`startAudioStream`**
* **`sendAudioChunk`**
* **`stopTask`**

#### Example

```tsx theme={null}
import { useChatInteract } from '@chainlit/react-client';

const ChatInteraction = () => {
  const { sendMessage, replyMessage, clear } = useChatInteract();

  return (
    <div>
      <button onClick={() => sendMessage({ content: 'Hello!' })}>Send</button>
      <button onClick={() => replyMessage({ content: 'Reply!' })}>Reply</button>
      <button onClick={clear}>Clear</button>
    </div>
  );
};
```

***

### `useAuth` Hook

The `useAuth` hook manages authentication within your React application, providing functionalities like user sessions and token management.

#### Properties & Methods

* **`authConfig`**
* **`user`**
* **`accessToken`**
* **`isLoading`**
* **`logout`**

#### Example

```tsx theme={null}
import { useAuth } from '@chainlit/react-client';

const UserProfile = () => {
  const { user, logout } = useAuth();

  if (!user) return <p>No user logged in.</p>;

  return (
    <div>
      <p>Username: {user.username}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

***

### `useApi` Hook

The `useApi` hook simplifies data fetching and error handling using [SWR](https://swr.vercel.app/).

#### Example

```tsx theme={null}
import { useApi } from '@chainlit/react-client';

const Settings = () => {
  const { data, error, isLoading } = useApi('/project/settings');

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return <pre>{JSON.stringify(data, null, 2)}</pre>;
};
```


# Slack
Source: https://docs.chainlit.io/deploy/slack



To make your Chainlit app available on Slack, you will need to create a Slack app and set up the necessary environment variables.

## How it Works

The Slack bot will listen to messages mentioning it in channels and direct messages.
It will send replies to a dedicated thread or DM depending on the context.

<Frame>
  <img />
</Frame>

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ❌         | ✅        | ❌     | ❌        | ✅            | ❌             | ✅        |

## Install the Slack Bolt Library

The Slack Bolt library is not included in the Chainlit dependencies. You will have to install it manually.

```bash theme={null}
pip install slack_bolt
```

## Create a Slack App

To start, navigate to the [Slack apps dashboard for the Slack API](https://api.slack.com/apps). Here, you should find a green button that says Create New App. When you click this button, select the option to create your app from scratch.

Create a name for your bot, such as "ChainlitDemo". Select the workspace you would like your bot to exist in.

<Frame>
  <img />
</Frame>

## Connection Modes

Chainlit supports two ways to connect to Slack:

* **HTTP Mode** (default): Slack sends events to your Chainlit server via HTTP. Requires a public URL.
* **Socket Mode** (since 2.7.0): Chainlit connects to Slack via WebSocket. No public URL needed — ideal for local development or restrictive networks.

To use Socket Mode, set the `SLACK_WEBSOCKET_TOKEN` environment variable (see [Environment Variables](#set-the-environment-variables)). When set, Socket Mode takes priority over the HTTP handler.

## Working Locally

### With Socket Mode (recommended)

If you use Socket Mode, no public URL or ngrok is needed. Chainlit connects to Slack over WebSocket directly. See the [Socket Mode app manifest](#socket-mode) below.

### With HTTP Mode

If you are working locally with HTTP mode, you will have to expose your local Chainlit app to the internet to receive incoming messages from Slack. You can use [ngrok](https://ngrok.com/) for this.

```bash theme={null}
ngrok http 8000
```

This will give you a public URL that you can use to set up the app manifest. Do not forget to replace it once you deploy Chainlit to a public host.

## Set the App Manifest

Go to App Manifest and paste the following Yaml.

<Note>Replace the `{placeholders}` with your own values.</Note>

```yaml theme={null}
display_information:
  name: { APP_NAME }
features:
  bot_user:
    display_name: { APP_NAME }
    always_online: false
oauth_config:
  scopes:
    user:
      - im:history
      - channels:history
    bot:
      - app_mentions:read
      - channels:read
      - chat:write
      - files:read
      - files:write
      - im:history
      - im:read
      - im:write
      - users:read
      - users:read.email
      - channels:history
      - groups:history
settings:
  event_subscriptions:
    request_url: https://{ CHAINLIT_APP_HOST }/slack/events
    bot_events:
      - app_home_opened
      - app_mention
      - message.im
  interactivity:
    is_enabled: true
    request_url: https://{ CHAINLIT_APP_HOST }/slack/events
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

Click on Save Changes.

<Frame>
  <img />
</Frame>

You will see a warning stating that the URL is not verified. You can ignore this for now.

### Socket Mode

If you are using Socket Mode, apply these changes to the manifest above: remove both `request_url` fields and set `socket_mode_enabled` to `true`.

```yaml theme={null}
settings:
  event_subscriptions:
    request_url: https://{ CHAINLIT_APP_HOST }/slack/events # [!code --]
    bot_events:
      - app_home_opened
      - app_mention
      - message.im
  interactivity:
    is_enabled: true
    request_url: https://{ CHAINLIT_APP_HOST }/slack/events # [!code --]
  org_deploy_enabled: false
  socket_mode_enabled: false # [!code --]
  socket_mode_enabled: true # [!code ++]
  token_rotation_enabled: false
```

## \[Optional] Allow users to send DMs to Chainlit

By default the app will only listen to mentions in channels.

If you want to allow users to send direct messages to the app, go to App Home and enable "Allow users to send Slash commands and messages from the messages tab".

<Frame>
  <img />
</Frame>

## \[Optional] Emoji Reaction on Message Received

Adds an optional feature to show emoji reactions when Slack messages are received, providing immediate user feedback while the bot processes the request.

<Note>
  This feature requires the `reactions:write` OAuth scope. If you enable this feature, you'll need to add this scope to your Slack app's OAuth configuration.
</Note>

To enable this feature, add the following configuration to your `chainlit.md` file:

```toml theme={null}
[features.slack]
reaction_on_message_received = true
```

<Warning>
  This feature is disabled by default to maintain backward compatibility. If you enable this feature, you'll need to add the `reactions:write` scope to your Slack app's OAuth configuration.
</Warning>

<Frame>
  <img />
</Frame>

## \[Optional] Handling Emoji Reactions from Users

React to emoji reactions that users add to messages in your Slack workspace.

<Note>
  This feature requires the `reactions:read` OAuth scope and the `reaction_added` bot event. Add both to your Slack app's manifest and OAuth configuration.
</Note>

```python theme={null}
from typing import Any, Dict
import chainlit as cl

@cl.on_slack_reaction_added
async def handle_reaction(event: Dict[str, Any]):
    reaction = event.get("reaction")       # e.g. "thumbsup"
    user_id = event.get("user")            # Slack user ID
    item = event.get("item", {})           # reacted item info

    print(f"User {user_id} reacted with :{reaction}: in channel {item.get('channel')}")
```

The `event` dictionary contains:

| Key        | Description                                                           |
| ---------- | --------------------------------------------------------------------- |
| `reaction` | Emoji name without colons (e.g. `"thumbsup"`)                         |
| `user`     | Slack user ID who added the reaction                                  |
| `item`     | Dict with `type`, `ts` (timestamp), and `channel` of the reacted item |

<Note>
  Since version **2.8.5**.
</Note>

## Install the Slack App to Your Workspace

Navigate to the Install App tab and click on Install to Workspace.

## Set the Environment Variables

<Note>Set the environment variables outside of your application code.</Note>

### Bot Token

Once the slack application is installed, you will see the Bot User OAuth Token. Set this as an environment variable in your Chainlit app.

<Frame>
  <img />
</Frame>

```bash theme={null}
SLACK_BOT_TOKEN=your_bot_token
```

### Signing Secret

Navigate to the Basic Information tab and copy the Signing Secret. Then set it as an environment variable in your Chainlit app.

<Frame>
  <img />
</Frame>

```bash theme={null}
SLACK_SIGNING_SECRET=your_signing_secret
```

### App-Level Token (Socket Mode only)

If you are using Socket Mode, you also need an App-Level Token. Navigate to **Basic Information** > **App-Level Tokens**, create a token with the `connections:write` scope, and set it as an environment variable.

```bash theme={null}
SLACK_WEBSOCKET_TOKEN=your_app_level_token
```

<Note>
  When `SLACK_WEBSOCKET_TOKEN` is set, Chainlit uses Socket Mode and the HTTP `/slack/events` endpoint is not registered. You do not need `SLACK_SIGNING_SECRET` in Socket Mode.
</Note>

## Start the Chainlit App

Since the Chainlit app is not running, the Slack app will not be able to communicate with it.

For the example, we will use this simple app:

```python my_app.py theme={null}
import chainlit as cl

@cl.on_message
async def on_message(msg: cl.Message):
    # Access the original slack event
    print(cl.user_session.get("slack_event"))
    # Access the slack user
    print(cl.user_session.get("user"))

    # Access potential attached files
    attached_files = msg.elements

    await cl.Message(content="Hello World").send()
```

<Note>
  Reminder: Make sure the environment variables are set. If using HTTP mode,
  your local Chainlit app must be exposed to the internet via ngrok.
</Note>

Start the Chainlit app:

```bash theme={null}
chainlit run my_app.py -h
```

<Note>
  Using -h to not open the default Chainlit UI since we are using Slack.
</Note>

You should now be able to interact with your Chainlit app through Slack.

## Chat History

Chat history is directly available through the `fetch_slack_message_history` method.
It will fetch the last messages from the current thread or DM channel.

```python theme={null}
import chainlit as cl
import discord


@cl.on_message
async def on_message(msg: cl.Message):
    fetch_slack_message_history = cl.user_session.get("fetch_slack_message_history")

    if fetch_slack_message_history:
        print(await fetch_slack_message_history(limit=10))

    # Your code here
```


# Teams
Source: https://docs.chainlit.io/deploy/teams



To make your Chainlit app available on Teams, you will need to create a Teams bot and set up the necessary environment variables.

## How it Works

The Teams bot will be available in direct messages.

<Frame>
  <img />
</Frame>

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ❌         | ✅        | ❌     | ❌        | ❌            | ❌             | ✅        |

## Install the Botbuilder Library

The Botbuilder library is not included in the Chainlit dependencies. You will have to install it manually.

```bash theme={null}
pip install botbuilder-core
```

## Create a Teams App

To start, navigate to the [App Management](https://dev.teams.microsoft.com/apps) page. Here, create a new app.

<Frame>
  <img />
</Frame>

## Fill the App Basic Information

Navigate to Configure > Basic Information and fill in the basic information about your app.
You won't be able to publish your app until you fill in all the required fields.

<Frame>
  <img />
</Frame>

## Create the Bot

Navigate to Configure > App features and add the Bot feature.
Create a new bot and give it the following permissions and save.

<Frame>
  <img />
</Frame>

## Go to the Bot Framework Portal

Navigate to the [Bot Framework Portal](https://dev.botframework.com/bots/), click on the Bot you just created and go to the Settings page.

## Get the App ID

In the Bot Framework Portal, you will find the app ID. Copy it and set it as an environment variable in your Chainlit app.

```
TEAMS_APP_ID=your_app_id
```

<Frame>
  <img />
</Frame>

## Working Locally

If you are working locally, you will have to expose your local Chainlit app to the internet to receive incoming messages to Teams. You can use [ngrok](https://ngrok.com/) for this.

```bash theme={null}
ngrok http 8000
```

This will give you a public URL that you can use to set up the app manifest. Do not forget to replace it once you deploy Chainlit to a public host.

## Set the Message Endpoint

Under Configuration, set the messaging endpoint to your Chainlit app HTTPS URL and add the `/teams/events` suffix.

<Frame>
  <img />
</Frame>

## Get the App Secret

On the same page, you will find a blue "Manage Microsoft App ID and password" button. Click on it.

<Frame>
  <img />
</Frame>

Navigate to Manage > Certificates & secrets and create a new client secret. Copy it and set it as an environment variable in your Chainlit app.

```
TEAMS_APP_PASSWORD=your_app_secret
```

## Support Multi Tenant Account Types

Navigate to Manage > Authentication and toggle "Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant)" then save.

<Frame>
  <img />
</Frame>

## Start the Chainlit App

Since the Chainlit app is not running, the Teams bot will not be able to communicate with it.

For the example, we will use this simple app:

```python my_app.py theme={null}
import chainlit as cl

@cl.on_message
async def on_message(msg: cl.Message):
    # Access the teams user
    print(cl.user_session.get("user"))

    # Access potential attached files
    attached_files = msg.elements

    await cl.Message(content="Hello World").send()
```

<Note>
  Reminder: Make sure the environment variables are set and that your local
  chainlit app is exposed to the internet via ngrok.
</Note>

Start the Chainlit app:

```bash theme={null}
chainlit run my_app.py -h
```

<Note>
  Using -h to not open the default Chainlit UI since we are using Teams.
</Note>

## Publish the Bot

Back to the [App Management](https://dev.teams.microsoft.com/apps) page, navigate to "Publish to org" and click on "Publish".

<Frame>
  <img />
</Frame>

## Authorize the Bot

The Bot will have to be authorized by the Teams admin before it can be used. To do so navigate to the [Teams admin center](https://admin.teams.microsoft.com/policies/manage-apps) and find the app.

<Frame>
  <img />
</Frame>

Then authorize it.

<Frame>
  <img />
</Frame>

You should now be able to interact with your Chainlit app through Teams.


# Web App
Source: https://docs.chainlit.io/deploy/webapp



The native Chainlit UI that is available on port 8000. Should open in your default browser when you run `chainlit run`.

## Supported Features

| Message | Streaming | Elements | Audio | Ask User | Chat History | Chat Profiles | Feedback |
| ------- | --------- | -------- | ----- | -------- | ------------ | ------------- | -------- |
| ✅       | ✅         | ✅        | ✅     | ✅        | ✅            | ✅             | ✅        |

<Frame>
  <img />
</Frame>

## URL Parameters

The Chainlit web app supports the following URL query parameters:

| Parameter | Description                                                                                 |
| --------- | ------------------------------------------------------------------------------------------- |
| `prompt`  | Pre-fills the chat input with the given text. The user can edit or clear it before sending. |

**Example** — open the chat with a pre-typed message:

```
https://your-app.com/?prompt=Hello%20World
```

This is useful for creating deep-links into specific conversations, e.g. from a help widget or an email campaign.

<Note>
  Since version **2.9.1**.
</Note>

## Window Messaging

When running the Web App inside an iframe, the server and parent window can communicate using window messages. This is useful for sending context information to the Chainlit server and updating your parent window based on the server's response.

Add a `@cl.on_window_message` decorated function to your Chainlit server to receive messages sent from the parent window.

```py theme={null}
import chainlit as cl

@cl.on_window_message
async def window_message(message: str):
  if message.startswith("Client: "):
    await cl.Message(content=f"Window message received: {message}").send()
```

Then, in your app/website, you can emit a window message like this:

```js theme={null}
const iframe = document.getElementById('the-iframe');
iframe.contentWindow.postMessage('Client: Hello from parent window', '*');
```

To send a message from the server to the parent window, use `cl.send_window_message`:

```py theme={null}
import chainlit as cl

@cl.on_message
async def message():
  await cl.send_window_message("Server: Hello from Chainlit")
```

The parent window can listen for messages like this:

```js theme={null}
window.addEventListener('message', (event) => {
  if (event.data.startsWith("Server: ")) {
    console.log('Parent window received:', event.data);
  }
});
```

### Example

Check out this example from the cookbook that uses the window messaging feature: [https://github.com/Chainlit/cookbook/tree/main/window-message](https://github.com/Chainlit/cookbook/tree/main/window-message)


# Community
Source: https://docs.chainlit.io/examples/community



## Videos

* [Build Python LLM apps in minutes Using Chainlit ⚡️](https://www.youtube.com/watch?v=tv7rn5AsxFY) from [Krish Naik](https://twitter.com/Krishnaik06)
* [Build an Arxiv QA Chat Application in Minutes!](https://www.youtube.com/watch?v=9SBUStfCtmk) from [Chris Alexiuk](https://twitter.com/c_s_ale)
* [Chainlit: Build LLM Apps in MINUTES!](https://www.youtube.com/watch?v=rcXPq3UcxIY) from [WorldOfAI](https://www.youtube.com/@intheworldofai)
* [Now Build & Share LLM Apps Super Fast with Chainlit](https://www.youtube.com/watch?v=_S3usFpVJOM) from [Sunny Bhaveen Chandra](https://www.youtube.com/c/c17hawke)
* [Chainlit CrashCourse - Build LLM ChatBot with Chainlit and Python & GPT](https://www.youtube.com/watch?v=pqriC9OT2aY) from [JCharisTech](https://www.youtube.com/@JCharisTech)
* [Chat with ... anything](https://twitter.com/waseemhnyc/status/1665923724426502148) by [Waseem H](https://twitter.com/waseemhnyc)
* [Unleash the Power of Falcon with LangChain: Step-by-Step Guide to Run Chat App using Chainlit](https://www.youtube.com/watch?v=HG0_0lqrWs4\&ab_channel=MenloParkLab) by [Menlo Park Lab](https://www.youtube.com/@menloparklab)
* [Chainlit tutorial series](https://www.youtube.com/playlist?list=PL2fGiugrNoogRNUHUWCDAnooWKmfVDnFS) (in chinese) by [01coder](https://www.youtube.com/@01coder30)

## Articles

* [AI Agents tutorial: How to create information retrieval Chatbot](https://lablab.ai/t/agents-retrieval-chatbot) from [Jakub Misiło](https://www.linkedin.com/in/jmisilo/)
* [Create an Azure OpenAI, LangChain, ChromaDB, and Chainlit Chat App in Container Apps using Terraform](https://techcommunity.microsoft.com/t5/fasttrack-for-azure/create-an-azure-openai-langchain-chromadb-and-chainlit-chat-app/ba-p/3885602) from [Paolo Salvatori](https://techcommunity.microsoft.com/t5/user/viewprofilepage/user-id/988334#profile)
* [Create A Chatbot with Internet Connectivity Powered by Langchain and Chainlit](https://levelup.gitconnected.com/create-a-chatbot-with-internet-connectivity-powered-by-langchain-and-chainlit-cba86f57ab2e) from [Yeyu Hang](https://medium.com/@wenbohuang0307)
* [For Chatbot Development, Streamlit Is Good, But Chainlit Is Better](https://levelup.gitconnected.com/for-chatbot-development-streamlit-is-good-but-chainlit-is-better-4112f9473a69) from [Yeyu Hang](https://medium.com/@wenbohuang0307)
* [Build and Deploy a Chat App Powered by LangChain and Chainlit using Docker](https://levelup.gitconnected.com/build-deploy-a-chat-app-powered-by-langchain-chainlit-using-docker-4f687da08625) from [MA Raza, Ph.D.](https://medium.com/gitconnected/build-deploy-a-chat-app-powered-by-langchain-chainlit-using-docker-4f687da08625)

Note that some of those tutorials might use the old sync version of the package. See the [Migration Guide](/examples/openai-sql) to update those!


# Cookbook
Source: https://docs.chainlit.io/examples/cookbook



The Cookbook repository serves as a valuable resource and starting point for developers looking to explore the capabilities of Chainlit in creating LLM apps.

It provides a diverse collection of **example projects**, each residing in its own folder, showcasing the integration of various tools such as **OpenAI, Anthropiс, LangChain, LlamaIndex, ChromaDB, Pinecone and more**.

Whether you are seeking basic tutorials or in-depth use cases, the Cookbook repository offers inspiration and practical insights!

<Card title="https://github.com/Chainlit/cookbook" icon="github" href="https://github.com/Chainlit/cookbook" />


# Text to SQL
Source: https://docs.chainlit.io/examples/openai-sql



Let's build a simple app that helps users to create SQL queries with natural language.

<Frame>
  <video />
</Frame>

## Prerequisites

This example has extra dependencies. You can install them with:

```bash theme={null}
pip install chainlit openai
```

## Imports

```python app.py theme={null}
from openai import AsyncOpenAI


import chainlit as cl

cl.instrument_openai()

client = AsyncOpenAI(api_key="YOUR_OPENAI_API_KEY")
```

## Define a prompt template and LLM settings

````python app.py theme={null}
template = """SQL tables (and columns):
* Customers(customer_id, signup_date)
* Streaming(customer_id, video_id, watch_date, watch_minutes)

A well-written SQL query that {input}:
```"""


settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"],
}
````

## Add the Assistant Logic

Here, we decorate the `main` function with the [@on\_message](/api-reference/lifecycle-hooks/on-message) decorator to tell Chainlit to run the `main` function each time a user sends a message.

Then, we wrap our text to sql logic in a [Step](/concepts/step).

```python app.py theme={null}
@cl.set_starters
async def starters():
    return [
       cl.Starter(
           label=">50 minutes watched",
           message="Compute the number of customers who watched more than 50 minutes of video this month."
       )
    ]

@cl.on_message
async def main(message: cl.Message):
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": template.format(input=message.content),
            }
        ], stream=True, **settings
    )

    msg = await cl.Message(content="", language="sql").send()

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    await msg.update()
```

## Try it out

```bash theme={null}
chainlit run app.py -w
```

You can ask questions like `Compute the number of customers who watched more than 50 minutes of video this month`.


# Document QA
Source: https://docs.chainlit.io/examples/qa



In this example, we're going to build an chatbot QA app. We'll learn how to:

* Upload a document
* Create vector embeddings from a file
* Create a chatbot app with the ability to display sources used to generate an answer

This example is inspired from the [LangChain doc](https://python.langchain.com/en/latest/use_cases/question_answering.html)

## Prerequisites

This example has extra dependencies. You can install them with:

```bash theme={null}
pip install langchain langchain-community chromadb tiktoken openai langchain-openai
```

Then, you need to go to create an OpenAI key [here](https://platform.openai.com/account/api-keys).

<Note>
  The state of the union file is available
  [here](https://github.com/Chainlit/cookbook/blob/main/llama-index/data/state_of_the_union.txt)
</Note>

## Conversational Document QA with LangChain

```python qa.py theme={null}
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import (
    ConversationalRetrievalChain,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory

import chainlit as cl

os.environ["OPENAI_API_KEY"] = (
    "OPENAI_API_KEY"
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    with open(file.path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split the text into chunks
    texts = text_splitter.split_text(text)

    # Create a metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # Create a Chroma vector store
    embeddings = OpenAIEmbeddings()
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  # type: List[Document]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(
                    content=source_doc.page_content, name=source_name, display="side"
                )
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()
```

## Try it out

```bash theme={null}
chainlit run qa.py
```

You can then upload any `.txt` file to the UI and ask questions about it.
If you are using `state_of_the_union.txt` you can ask questions like `What did the president say about Ketanji Brown Jackson?`.

<img alt="QA" />


# Security - PII
Source: https://docs.chainlit.io/examples/security



When building chat applications, it's crucial to ensure the secure handling of sensitive data, especially Personal Identifiable Information (PII). PII can be directly or indirectly linked to an individual, making it essential to protect user privacy by preventing the transmission of such data to language models.

### Example of PII

Consider the text below, where PII has been highlighted:

> Hello, my name is **John** and I live in **New York**.
> My credit card number is **3782-8224-6310-005** and my phone number is **(212) 688-5500**.

And here is the anonymized version:

> Hello, my name is \<PERSON> and I live in \<LOCATION>. My credit card number is \<CREDIT\_CARD> and my phone number is \<PHONE\_NUMBER>.

## Analyze and anonymize data

Integrate [Microsoft Presidio](https://microsoft.github.io/presidio/) for robust data sanitization in your Chainlit application.

```python Code Example theme={null}
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Notice that the message is passed as is
    response = await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

Before proceeding, ensure that the Python packages required for PII analysis and anonymization are installed. Run the following commands in your terminal to install them:

```shell theme={null}
pip install presidio-analyzer presidio-anonymizer spacy
python -m spacy download en_core_web_lg
```

Create an async context manager that utilizes the Presidio Analyzer to inspect the incoming text for any PII. This context manager can be included in your main function to scrutinize messages before they are processed.
When PII is detected, you should present the user with the option to either continue or cancel the operation. Use Chainlit's messaging system to accomplish this.

```python Code Example theme={null}
from presidio_analyzer import AnalyzerEngine
from contextlib import asynccontextmanager

analyzer = AnalyzerEngine()

@asynccontextmanager
async def check_text(text: str):
  pii_results = analyzer.analyze(text=text, language="en")

  if pii_results:
    response = await cl.AskActionMessage(
      content="PII detected",
      actions=[
        cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
        cl.Action(name="cancel", payload={"value": "continue"}, label="❌ Cancel"),
      ],
    ).send()

    if response is None or response.get("payload").get("value") == "cancel":
      raise InterruptedError

  yield

# ...

@cl.on_message
async def main(message: cl.Message):
  async with check_text(message.content):
    # This block is only executed when the user press "Continue"
    response = await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

If your application has a requirement to anonymize PII, Presidio can also do that. Modify the check\_text context manager to return anonymized text when PII is detected.

```python Code Example theme={null}
from presidio_anonymizer import AnonymizerEngine

anonymizer = AnonymizerEngine()

@asynccontextmanager
async def check_text(text: str):
  pii_results = analyzer.analyze(text=text, language="en")

  if pii_results:
    response = await cl.AskActionMessage(
      content="PII detected",
      actions=[
        cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
        cl.Action(name="cancel", payload={"value": "continue"}, label="❌ Cancel"),
      ],
    ).send()

    if response is None or response.get("payload").get("value") == "cancel":
      raise InterruptedError

    yield anonymizer.anonymize(
      text=text,
      analyzer_results=pii_results,
    ).text
  else:
    yield text

# ...

@cl.on_message
async def main(message: cl.Message):
  async with check_text(message.content) as anonymized_message:
    response = await llm_chain.arun(
      anonymized_message
      callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
```


# Installation
Source: https://docs.chainlit.io/get-started/installation



Chainlit requires `python>=3.9`.

You can install Chainlit it via pip as follows:

```bash theme={null}
pip install chainlit
```

This will make the `chainlit` command available on your system.

Make sure everything runs smoothly:

```bash theme={null}
chainlit hello
```

This should spawn the chainlit UI and ask for your name like so:

<img alt="Hello" />

## Next steps

<CardGroup>
  <Card title="In Pure Python" icon="python" href="/get-started/pure-python">
    Learn on how to use Chainlit with any python code.
  </Card>

  <Card title="Integrations" icon="link" href="/integrations">
    Integrate Chainlit with other frameworks.
  </Card>
</CardGroup>


# Overview
Source: https://docs.chainlit.io/get-started/overview



Chainlit is an open-source Python package to build production ready Conversational AI.

<Frame>
  <video />
</Frame>

## Key features

1. [Build fast:](/examples/openai-sql) Get started in a couple lines of Python

2. [Authentication:](/authentication/overview) Integrate with corporate identity providers and existing authentication infrastructure

3. [Data persistence:](/data-persistence/overview) Collect, monitor and analyze data from your users

4. [Visualize multi-steps reasoning:](/concepts/step) Understand the intermediary steps that produced an output at a glance

5. [Multi Platform:](/deploy/overview) Write your assistant logic once, use everywhere

## Integrations

Chainlit is compatible with all Python programs and libraries. That being said, it comes with a set of integrations with popular libraries and frameworks.

<CardGroup>
  <Card title="LangChain" icon="circle" href="/integrations/langchain">
    Learn how to use any LangChain agent with Chainlit.
  </Card>

  <Card title="OpenAI" icon="circle" href="/integrations/openai">
    Learn how to explore your OpenAI calls in Chainlit.
  </Card>

  <Card title="OpenAI Assistant" icon="circle" href="https://github.com/Chainlit/cookbook/tree/main/openai-data-analyst">
    Learn how to integrate your OpenAI Assistants with Chainlit.
  </Card>

  <Card title="Mistral AI" icon="circle" href="/integrations/mistralai">
    Learn how to use any Mistral AI calls in Chainlit.
  </Card>

  <Card title="Semantic Kernel" icon="circle" href="/integrations/semantic-kernel">
    Learn how to integrate your Semantic Kernel code with Chainlit.
  </Card>

  <Card title="Llama Index" icon="circle" href="/integrations/llama-index">
    Learn how to integrate your Llama Index code with Chainlit.
  </Card>

  <Card title="Autogen" icon="circle" href="https://github.com/Chainlit/cookbook/tree/main/pyautogen">
    Learn how to integrate your Autogen agents with Chainlit.
  </Card>
</CardGroup>


# In Pure Python
Source: https://docs.chainlit.io/get-started/pure-python



In this tutorial, we'll walk through the steps to create a minimal LLM app.

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* Basic understanding of Python programming

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 2: Write the Application Logic

In `app.py`, import the Chainlit package and define a function that will handle incoming messages from the chatbot UI. Decorate the function with the `@cl.on_message` decorator to ensure it gets called whenever a user inputs a message.

Here's the basic structure of the script:

```python app.py theme={null}
import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

The `main` function will be called every time a user inputs a message in the chatbot UI. You can put your custom logic within the function to process the user's input, such as analyzing the text, calling an API, or computing a result.

The [Message](/api-reference/message) class is responsible for sending a reply back to the user. In this example, we simply send a message containing the user's input.

## Step 3: Run the Application

To start your Chainlit app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).

<img alt="PythonExample" />

## Next Steps

<CardGroup>
  <Card title="Concepts" icon="lightbulb" href="/concepts">
    Learn about the core concepts of Chainlit
  </Card>

  <Card title="Cookbook" icon="book" href="https://github.com/Chainlit/cookbook">
    Explore the Chainlit cookbook for more examples
  </Card>
</CardGroup>


# Migrate to Chainlit v1.0.500
Source: https://docs.chainlit.io/guides/migration/1.0.500



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md#10500---2023-04-02).

## How to migrate?

### 1. Regenerate translations

Since translation files have been updated, you need to regenerate them. To do so, remove the `.chainlit/translations` folder and restart your application.

### 2. Update the multi\_modal config setting

The `multi_modal` config setting has been updated. You can either remove the entire `./chainlit/config.toml` file and restart your app or update the `multi_modal` setting manually (example [here](http://localhost:3002/backend/config/features#default-configuration)).


# Migrate to Chainlit v1.1.0
Source: https://docs.chainlit.io/guides/migration/1.1.0



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md#110---2024-05-13).

## How to migrate?

### Rename the multi\_modal config setting

The `multi_modal` config setting has been renamed `spontaneous_file_upload`. You can either remove the entire `./chainlit/config.toml` file and restart your app or rename the `multi_modal` setting manually (example [here](/backend/config/features#default-configuration)).

<Warning>
  The cl.Message.send() method no longer returns the id of the message but the
  message itself. If you were using the id, you will need to update your code.
</Warning>


# Migrate to Chainlit v1.1.300
Source: https://docs.chainlit.io/guides/migration/1.1.300



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## New Feature: Starters

<Frame>
  <img />
</Frame>

This release introduces a new feature called Starters. Starters are suggestions to help your users get started with your assistant.
You can declare up to 4 starters and optionally define an icon for each one.

```python starters.py theme={null}
import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
            ),

        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
            ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
            ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
            )
        ]
# ...
```

Starters also work with Chat Profiles. You can define different starters for different chat profiles.

```python starters_with_chat_profiles.py theme={null}
@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] != "ADMIN":
        return None

    return [
        cl.ChatProfile(
            name="My Chat Profile",
            icon="https://picsum.photos/250",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/public/idea.svg",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/public/learn.svg",
                ),
            ],
        )
    ]
```

## Rework: Debugging

We created Chainlit with a vision to make debugging as easy as possible. This is why Chainlit was supporting complex Chain of Thoughts and even had its own prompt playground.
This was great but was mixing two different concepts in one place:

1. Building conversational AI with best in class user experience.
2. Debugging and iterating efficiently.

Separating these two concepts was the right thing to do to:

1. Provide an even better UX (see the new [Chain of Thought](#chain-of-thought-rework)).
2. Provide an even better debugging experience.

You can enable the new debug mode by adding `-d` to your `chainlit run` command. If your data layer supports it, you will see a debug button below each message taking you to the trace/prompt playground.

<Frame>
  <img />
</Frame>

This also means we let go of the prompt playground in Chainlit and welcome a simplified Chain of Thought for your users!

## Rework: Chain of Thought

The Chain of Thought has been reworked to only be one level deep and only include tools; ultimately users are only interested in the tools used by the LLM to generate the response.

```python new_cot.py theme={null}
import chainlit as cl

@cl.step(type="tool")
async def tool():
    # Faking a tool
    await cl.sleep(2)
    return "Tool Response"

@cl.on_message
async def on_message():
    msg = await cl.Message("").send()
    msg.content = await tool()
    await msg.update()
```

<Warning>
  Notice that the `root` attribute of [cl.Step](/concepts/step) has been
  removed. Use [cl.Message](/concepts/message) to send root level messages.
</Warning>

<Frame>
  <video />
</Frame>

The data layer is still be able to provide the full Chain of Thought for debugging purposes.

## Rework: Avatars

The previous `cl.Avatar` element was adding overhead to developers forcing them to resend the avatars to each session.
It was also not working with resumed conversations.

`cl.Avatar` has been removed entirely. Now, you should place your avatar files in `/public/avatars`.
Let's say your message author is `My Assistant`, then you should place the avatar in `/public/avatars/my-assistant.png`.

If no avatar is found, it will default to the favicon.

## Rework: Custom Endpoints

Chainlit is now mountable as a FastAPI sub application. This allows you to use Chainlit on your existing FastAPI application.

Check the [FastAPI integration](/integrations/fastapi) and [API documentation](/integrations/fastapi) for more information.

## Minor Changes

1. You can now configure the default theme in the `config.toml` file.

```toml config.toml theme={null}
[UI]
  [UI.theme]
      default = "dark"
```

2. The `running`, `took_one` and `took_other` translations have been replaced by `used`.
   Either manually replace them in your translations or delete the translations file to regenerate it.

3. The `show_readme_as_default` config has been removed in favor of starters.

4. Root level messages will no longer collapse.

## Conclusion

<Note>
  Full changelog available
  [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md#11300rc0---2024-05-27).
</Note>

This pre-release brings a lot of changes to Chainlit. It is not yet stable, but we are excited to hear your feedback on it and improve it further!


# Migrate to Chainlit v1.1.400
Source: https://docs.chainlit.io/guides/migration/1.1.400



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## More control over Chain of Thought

The `hide_cot` config parameter has been replaced with `cot`. The `cot` parameter can be set to `hidden`, `tool_call`, or `full`. This parameter controls the display of the Chain of Thought (COT) in the UI.

## `disable_feedback` is gone

Chainlit 1.1.400 takes a different approach to feedback. Now, a user input will trigger a run. Once the run is complete, the user can provide feedback for the whole run instead of being able to score each message. This change simplifies the feedback process and makes it more intuitive.


# Migrate to Chainlit v1.1.404
Source: https://docs.chainlit.io/guides/migration/1.1.404



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## Breaking Changes

### Python Version Requirement

Chainlit 1.1.404 requires Python 3.9 or higher. Ensure you're using a compatible Python version before upgrading.

### Security Changes

Chainlit now listens on 127.0.0.1 (localhost) instead of 0.0.0.0 (public) for improved security.

#### For Containerized Deployments

If you're using containerized deployments, you may need to specify `--host 0.0.0.0` for your container to work correctly with the new security changes.

## New Features and Changes

### Environment Variable for Custom Config Locations

You can now use the `CHAINLIT_APP_ROOT` environment variable to specify custom config locations.

### Improved Error Handling

* HTTP errors in data layers are now handled more gracefully.
* Fixed an AttributeError in the llama\_index integration.

### Configuration Update

The `edit_message` placement in the default config has been corrected. Check your `config.toml` file and update if necessary.

## Best Practices

1. **Review Your Python Environment**: Ensure you're using Python 3.9 or higher.
2. **Update Containerized Deployments**: If using containers, adjust your configurations to include `--host 0.0.0.0` if needed.
3. **Check Custom Configurations**: If you've customized your Chainlit configuration, review it against the new defaults.
4. **Test Your Integration**: If you're using the llama\_index integration, test thoroughly after upgrading.

## Additional Notes

* The frontend connection resuming after connection loss has been fixed.
* A new pytest-based testing infrastructure has been implemented for improved stability.

Remember to thoroughly test your application after upgrading to ensure compatibility with these changes.


# Migrate to Chainlit v2.0.0
Source: https://docs.chainlit.io/guides/migration/2.0.0



<Note>Join the discord for live updates: [https://discord.gg/AzyvDHWARx](https://discord.gg/AzyvDHWARx)</Note>

## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

The Chainlit UI (including the copilot) has been completely re-written with Shadcn/Tailwind. This brings several advantages:

1. The codebase is simpler and more contribution friendly.
2. It enabled the new custom element feature.
3. The theme customisation is more powerful.

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md#200---2025-01-06).

## How to migrate?

### 1. Regenerate the config file

The following fields have been removed from the `config.toml` file:

1. **follow\_symlink**: Chainlit no longer uses `StaticFiles` to serve files.
2. **font\_family**, **custom\_font**, **\[UI.theme]**: Theme customisation now uses a [separate file](/customisation/theme).
3. **audio**: Chainlit audio streaming has been rework to match the [realtime APIs](/advanced-features/multi-modal).

You can either manually remove those field or remove the `.chainlit/config.toml` file and restart your application.

### 2. Cookie Auth & Cross Origins

All of the authentication mechanisms now use cookie auth instead of directly using a JWT. This change makes Chainlit more secure.

This does not require any change in your app code. However, this implies that Chainlit is now more picky about cross origins (for instance when using a copilot on a website).

If you need to consume a Chainlit app on a different origin, make sure you allow it in the `config.toml` under `allow_origins`.

### 3. Actions

1. The **value** field has replaced with `payload` which accepts a Python dict. This makes actions more useful.
2. The **description** field has been renamed `tooltip`.
3. The field `icon` has been added. You can use any lucide icon name.
4. The **collapsed** field has been removed.

### 4. Copilot Widget Config

1. The **fontFamily** field has been removed. Check the [new custom theme documentation](/customisation/theme).
2. the `button.style` field has been replaced with `button.className`. You can use any tailwind class to style the widget button.


# Migrate to Chainlit v2.1.0
Source: https://docs.chainlit.io/guides/migration/2.1.0



## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

Chainlit 2.1.0 introduces [Commands](/concepts/command) — a way to capture user intent in a deterministic way. Users can select a command before sending a message, and the selected command is persisted alongside the message in the `steps` table.

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md).

## How to migrate?

### 1. Update the database schema

A new `command` column must be added to the steps table so that the selected command can be persisted with each message.

<Tabs>
  <Tab title="Official data layer">
    The [Official data layer](https://github.com/Chainlit/chainlit-datalayer) Prisma schema has not been updated to include this column. Run the following migration manually against your database:

    ```sql theme={null}
    ALTER TABLE "Step" ADD COLUMN IF NOT EXISTS "command" TEXT;
    ```
  </Tab>

  <Tab title="SQLAlchemy / Custom SQL">
    ```sql theme={null}
    ALTER TABLE steps ADD COLUMN IF NOT EXISTS "command" TEXT;
    ```
  </Tab>
</Tabs>

<Note>
  DynamoDB users do not need to run any migration — the schema is dynamic.
</Note>


# Migrate to Chainlit v2.3.0
Source: https://docs.chainlit.io/guides/migration/2.3.0



## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

Chainlit 2.3.0 adds the ability to render [Steps](/api-reference/step-class) expanded by default using `cl.Step(default_open=True)`. The chosen value is persisted in a new `defaultOpen` column in the `steps` table.

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md).

## How to migrate?

### 1. Update the database schema

A new `defaultOpen` column must be added to the steps table.

<Tabs>
  <Tab title="Official data layer">
    The [Official data layer](https://github.com/Chainlit/chainlit-datalayer) Prisma schema has not been updated to include this column. Run the following migration manually against your database:

    ```sql theme={null}
    ALTER TABLE "Step" ADD COLUMN IF NOT EXISTS "defaultOpen" BOOLEAN;
    ```
  </Tab>

  <Tab title="SQLAlchemy / Custom SQL">
    ```sql theme={null}
    ALTER TABLE steps ADD COLUMN IF NOT EXISTS "defaultOpen" BOOLEAN;
    ```
  </Tab>
</Tabs>

<Note>
  DynamoDB users do not need to run any migration — the schema is dynamic.
</Note>


# Migrate to Chainlit v2.9.4
Source: https://docs.chainlit.io/guides/migration/2.9.4



## Updating Chainlit

Begin the migration by updating Chainlit to the latest version:

```bash theme={null}
pip install --upgrade chainlit
```

## What changes?

Chainlit 2.9.4 introduces [Modes](/concepts/modes) — a multi-picker system that lets users configure categories like model, reasoning effort, or persona per message. The selected modes are persisted alongside each message in a new `modes` column in the `steps` table.

Full changelog available [here](https://github.com/Chainlit/chainlit/blob/main/CHANGELOG.md).

## How to migrate?

### 1. Update the database schema

A new `modes` column must be added to the steps table so that selected modes can be persisted with each message.

<Tabs>
  <Tab title="Official data layer">
    The [Official data layer](https://github.com/Chainlit/chainlit-datalayer) Prisma schema has not been updated to include this column. Run the following migration manually against your database:

    ```sql theme={null}
    ALTER TABLE "Step" ADD COLUMN IF NOT EXISTS "modes" JSONB;
    ```
  </Tab>

  <Tab title="SQLAlchemy / Custom SQL">
    ```sql theme={null}
    ALTER TABLE steps ADD COLUMN IF NOT EXISTS "modes" JSONB;
    ```
  </Tab>
</Tabs>

<Note>
  DynamoDB users do not need to run any migration — the schema is dynamic.
</Note>


# Async / Sync
Source: https://docs.chainlit.io/guides/sync-async



Asynchronous programming is a powerful way to handle multiple tasks concurrently without blocking the execution of your program. Chainlit is async by default to allow agents to execute tasks in parallel and allow multiple users on a single app.
Python introduced the `asyncio` library to make it easier to write asynchronous code using the `async/await` syntax. This onboarding guide will help you understand the basics of asynchronous programming in Python and how to use it in your Chainlit project.

### Understanding async/await

The `async` and `await` keywords are used to define and work with asynchronous code in Python. An `async` function is a coroutine, which is a special type of function that can pause its execution and resume later, allowing other tasks to run in the meantime.

To define an async function, use the `async def` syntax:

```python theme={null}
async def my_async_function():
    # Your async code goes here
```

To call an async function, you need to use the `await` keyword:

```python theme={null}
async def another_async_function():
    result = await my_async_function()
```

### Working with Chainlit

Chainlit uses asynchronous programming to handle events and tasks efficiently. When creating a Chainlit agent, you'll often need to define async functions to handle events and perform actions.

For example, to create an async function that responds to messages in Chainlit:

```python theme={null}
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

### Long running synchronous tasks

In some cases, you need to run long running synchronous functions in your Chainlit project. To prevent blocking the event loop, you can utilize the `make_async` function provided by the Chainlit library to transform a synchronous function into an asynchronous one:

```python theme={null}
from chainlit import make_async

def my_sync_function():
    # Your synchronous code goes here
    import time
    time.sleep(10)
    return 0

async_function = make_async(my_sync_function)

async def main():
    result = await async_function()
```

By using this approach, you can maintain the non-blocking nature of your project while still incorporating synchronous functions when necessary.

### Call an async function from a sync function

If you need to run an asynchronous function inside a sync function, you can use the `run_sync` function provided by the Chainlit library:

```python theme={null}
from chainlit import run_sync

async def my_async_function():
    # Your asynchronous code goes here

def main():
    result = run_sync(my_async_function())

main()
```

By following this guide, you should now have a basic understanding of asynchronous programming in Python and how to use it in your Chainlit project.
As you continue to work with Chainlit, you'll find that async/await and the asyncio library provide a powerful and efficient way to handle multiple agents/tasks concurrently.


# Embedchain
Source: https://docs.chainlit.io/integrations/embedchain



In this tutorial, we'll walk through the steps to create a Chainlit application integrated with [Embedchain](https://github.com/embedchain/embedchain).

<img alt="Preview of what you'll be building" />

## Step 1: Create a Chainlit Application

In `app.py`, import the necessary packages and define one function to handle a new chat session and another function to handle messages incoming from the UI.

### With Embedchain

```python app.py theme={null}
import chainlit as cl
from embedchain import Pipeline as App

import os

os.environ["OPENAI_API_KEY"] = "sk-xxx"

@cl.on_chat_start
async def on_chat_start():
    app = App.from_config(config={
        'app': {
            'config': {
                'name': 'chainlit-app'
            }
        },
        'llm': {
            'config': {
                'stream': True,
            }
        }
    })
    # import your data here
    app.add("https://www.forbes.com/profile/elon-musk/")
    app.collect_metrics = False
    cl.user_session.set("app", app)


@cl.on_message
async def on_message(message: cl.Message):
    app = cl.user_session.get("app")
    msg = cl.Message(content="")
    for chunk in await cl.make_async(app.chat)(message.content):
        await msg.stream_token(chunk)
    
    await msg.send()
```

## Step 2: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

## Next Steps

Congratulations! You've just created your first LLM app with Chainlit and Embedchain.

Happy coding! 🎉


# FastAPI
Source: https://docs.chainlit.io/integrations/fastapi



Chainlit can be mounted as a FastAPI sub application.

```py my_cl_app theme={null}
import chainlit as cl

@cl.on_chat_start
async def main():
    await cl.Message(content="Hello World").send()
```

```py main theme={null}
from fastapi import FastAPI
from chainlit.utils import mount_chainlit

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

mount_chainlit(app=app, target="my_cl_app.py", path="/chainlit")
```

In the example above, we have a FastAPI application with a single endpoint `/app`. We mount the Chainlit application `my_cl_app.py` to the `/chainlit` path.

Start the FastAPI server:

```bash theme={null}
uvicorn main:app --host 0.0.0.0 --port 80
```

<Note>
  When using FastAPI integration, header authentication is the preferred method
  for authenticating users. This approach allows Chainlit to delegate the
  authentication process to the parent FastAPI application, providing a more
  seamless and secure integration.
</Note>


# LangChain/LangGraph
Source: https://docs.chainlit.io/integrations/langchain



In this tutorial, we'll walk through the steps to create a Chainlit application integrated with [LangChain](https://github.com/hwchase17/langchain).

<Frame>
  <img />
</Frame>

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* The LangChain package installed
* An OpenAI API key
* Basic understanding of Python programming

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 2: Write the Application Logic

In `app.py`, import the necessary packages and define one function to handle a new chat session and another function to handle messages incoming from the UI.

### With LangChain

Let's go through a small example.

<Note>
  If your agent/chain does not have an async implementation, fallback to the
  sync implementation.
</Note>

<CodeGroup>
  ```python Async LCEL theme={null}
  from langchain_openai import ChatOpenAI
  from langchain.prompts import ChatPromptTemplate
  from langchain.schema import StrOutputParser
  from langchain.schema.runnable import Runnable
  from langchain.schema.runnable.config import RunnableConfig
  from typing import cast

  import chainlit as cl


  @cl.on_chat_start
  async def on_chat_start():
      model = ChatOpenAI(streaming=True)
      prompt = ChatPromptTemplate.from_messages(
          [
              (
                  "system",
                  "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
              ),
              ("human", "{question}"),
          ]
      )
      runnable = prompt | model | StrOutputParser()
      cl.user_session.set("runnable", runnable)


  @cl.on_message
  async def on_message(message: cl.Message):
      runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

      msg = cl.Message(content="")

      async for chunk in runnable.astream(
          {"question": message.content},
          config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
      ):
          await msg.stream_token(chunk)

      await msg.send()
  ```

  ```python Sync LCEL theme={null}
  from langchain_openai import ChatOpenAI
  from langchain.prompts import ChatPromptTemplate
  from langchain.schema import StrOutputParser
  from langchain.schema.runnable import Runnable
  from langchain.schema.runnable.config import RunnableConfig

  import chainlit as cl


  @cl.on_chat_start
  async def on_chat_start():
      model = ChatOpenAI(streaming=True)
      prompt = ChatPromptTemplate.from_messages(
          [
              (
                  "system",
                  "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
              ),
              ("human", "{question}"),
          ]
      )
      runnable = prompt | model | StrOutputParser()
      cl.user_session.set("runnable", runnable)


  @cl.on_message
  async def on_message(message: cl.Message):
      runnable = cl.user_session.get("runnable")  # type: Runnable

      msg = cl.Message(content="")

      for chunk in await cl.make_async(runnable.stream)(
          {"question": message.content},
          config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
      ):
          await msg.stream_token(chunk)

      await msg.send()
  ```
</CodeGroup>

This code sets up an instance of `Runnable` with a custom `ChatPromptTemplate` for each chat session. The `Runnable` is invoked everytime a user sends a message to generate the response.

The callback handler is responsible for listening to the chain's intermediate steps and sending them to the UI.

### With LangGraph

```python theme={null}
from typing import Literal
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage

import chainlit as cl

@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
final_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

model = model.bind_tools(tools)
# NOTE: this is where we're adding a tag that we'll can use later to filter the model stream events to only the model called in the final node.
# This is not necessary if you call a single LLM but might be important in case you call multiple models within the node and want to filter events
# from only one of them.
final_model = final_model.with_config(tags=["final_node"])
tool_node = ToolNode(tools=tools)

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import MessagesState
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


def should_continue(state: MessagesState) -> Literal["tools", "final"]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return "final"


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def call_final_model(state: MessagesState):
    messages = state["messages"]
    last_ai_message = messages[-1]
    response = final_model.invoke(
        [
            SystemMessage("Rewrite this in the voice of Al Roker"),
            HumanMessage(last_ai_message.content),
        ]
    )
    # overwrite the last AI message from the agent
    response.id = last_ai_message.id
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)
# add a separate final node
builder.add_node("final", call_final_model)

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
)

builder.add_edge("tools", "agent")
builder.add_edge("final", END)

graph = builder.compile()

@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")
    
    for msg, metadata in graph.stream({"messages": [HumanMessage(content=msg.content)]}, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and metadata["langgraph_node"] == "final"
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()
```

## Step 3: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).

<Warning>
  When using LangChain, prompts and completions are not cached by default. To
  enable the cache, set the `cache=true` in your chainlit config file.
</Warning>


# LiteLLM
Source: https://docs.chainlit.io/integrations/litellm



In this tutorial, we will guide you through the steps to create a Chainlit application integrated with [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy)

The benefits of using LiteLLM Proxy with Chainlit is:

* You can [call 100+ LLMs in the OpenAI API format](https://docs.litellm.ai/docs/providers)
* Use Virtual Keys to set budget limits and track usage
* see LLM API calls in a step in the UI, and you can explore them in the prompt playground.

<Warning>
  You shouldn't configure this integration if you're already using another
  integration like Langchain or LlamaIndex. Both integrations would
  record the same generation and create duplicate steps in the UI.
</Warning>

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* The OpenAI package installed
* [LiteLLM Proxy Running](https://docs.litellm.ai/docs/proxy/deploy)
* [A LiteLLM Proxy API Key](https://docs.litellm.ai/docs/proxy/virtual_keys)
* Basic understanding of Python programming

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 2: Write the Application Logic

In `app.py`, import the necessary packages and define one function to handle messages incoming from the UI.

```python theme={null}
from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI(
    api_key="anything",            # litellm proxy virtual key
    base_url="http://0.0.0.0:4000" # litellm proxy base_url
)

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-3.5-turbo", # model you want to send litellm proxy
    "temperature": 0,
    # ... more settings
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Spanish",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
```

## Step 3: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).


# Llama Index
Source: https://docs.chainlit.io/integrations/llama-index



In this tutorial, we will guide you through the steps to create a Chainlit application integrated with [Llama Index](https://github.com/jerryjliu/llama_index).

<Frame>
  <img />
</Frame>

## Prerequisites

Before diving in, ensure that the following prerequisites are met:

* A working installation of Chainlit
* The Llama Index package installed
* An OpenAI API key
* A basic understanding of Python programming

## Step 1: Set Up Your Data Directory

Create a folder named `data` in the root of your app folder. Download the [state of the union](https://github.com/Chainlit/cookbook/blob/main/llama-index/data/state_of_the_union.txt) file (or any files of your own choice) and place it in the `data` folder.

## Step 2: Create the Python Script

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 3: Write the Application Logic

In `app.py`, import the necessary packages and define one function to handle a new chat session and another function to handle messages incoming from the UI.

In this tutorial, we are going to use `RetrieverQueryEngine`. Here's the basic structure of the script:

```python app.py theme={null}
import os
import openai
import chainlit as cl

from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.callbacks import CallbackManager
from llama_index.core.service_context import ServiceContext

openai.api_key = os.environ.get("OPENAI_API_KEY")

try:
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # load index
    index = load_index_from_storage(storage_context)
except:
    documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()


@cl.on_chat_start
async def start():
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo", temperature=0.1, max_tokens=1024, streaming=True
    )
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.context_window = 4096

    service_context = ServiceContext.from_defaults(callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]))
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=2, service_context=service_context)
    cl.user_session.set("query_engine", query_engine)

    await cl.Message(
        author="Assistant", content="Hello! Im an AI assistant. How may I help you?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine") # type: RetrieverQueryEngine

    msg = cl.Message(content="", author="Assistant")

    res = await cl.make_async(query_engine.query)(message.content)

    for token in res.response_gen:
        await msg.stream_token(token)
    await msg.send()
```

This code sets up an instance of `RetrieverQueryEngine` for each chat session. The `RetrieverQueryEngine` is invoked everytime a user sends a message to generate the response.

The callback handlers are responsible for listening to the intermediate steps and sending them to the UI.

## Step 4: Launch the Application

To kick off your LLM app, open a terminal, navigate to the directory containing `app.py`, and run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag enables auto-reloading so that you don't have to restart the server each time you modify your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).


# vLLM, LMStudio, HuggingFace
Source: https://docs.chainlit.io/integrations/message-based



We can leverage the OpenAI instrumentation to log calls from inference servers that use messages-based API, such as vLLM, LMStudio or HuggingFace's TGI.

<Warning>
  You shouldn't configure this integration if you're already using another integration like LangChain or LlamaIndex. Both integrations would record the same generation and create duplicate steps in the UI.
</Warning>

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

In `app.py`, import the necessary packages and define one function to handle messages incoming from the UI.

```python theme={null}
from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    # ... more settings
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Spanish",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
```

Create a file named `.env` in the same folder as your `app.py` file. Add your OpenAI API key in the `OPENAI_API_KEY` variable.

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).


# Mistral AI
Source: https://docs.chainlit.io/integrations/mistralai



<Warning>
  You shouldn't configure this integration if you're already using another
  integration like Langchain or LlamaIndex. Both integrations would
  record the same generation and create duplicate steps in the UI.
</Warning>

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* The Mistral AI python client package installed, `mistralai`
* A [Mistral AI API key](https://console.mistral.ai/api-keys/)
* Basic understanding of Python programming

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 2: Write the Application Logic

In `app.py`, import the necessary packages and define one function to handle messages incoming from the UI.

```python theme={null}
import os
import chainlit as cl
from mistralai import Mistral

# Initialize the Mistral client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.complete_async(
        model="mistral-small-latest",
        max_tokens=100,
        temperature=0.5,
        stream=False,
        # ... more setting
        messages=[
            {
                "role": "system",
                "content": "You are a helpful bot, you always reply in French."
            },
            {
                "role": "user",
                "content": message.content # Content of the user message
            }
        ]
    )
    await cl.Message(content=response.choices[0].message.content).send()
```

## Step 3: Fill the environment variables

Create a file named `.env` in the same folder as your `app.py` file. Add your Mistral AI API key in the `MISTRAL_API_KEY` variable.

## Step 4: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).


# OpenAI
Source: https://docs.chainlit.io/integrations/openai



<Note>
  If you are using OpenAI assistants, check out the [OpenAI
  Assistant](https://github.com/Chainlit/cookbook/tree/main/openai-data-analyst)
  example app.
</Note>

The benefits of this integration is that you can see the OpenAI API calls in a step in the UI, and you can explore them in the prompt playground.

You need to add `cl.instrument_openai()` after creating your OpenAI client.

<Warning>
  You shouldn't configure this integration if you're already using another
  integration like Langchain or LlamaIndex. Both integrations would
  record the same generation and create duplicate steps in the UI.
</Warning>

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* The OpenAI package installed
* An OpenAI API key
* Basic understanding of Python programming

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application.

## Step 2: Write the Application Logic

In `app.py`, import the necessary packages and define one function to handle messages incoming from the UI.

```python theme={null}
from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI()

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    # ... more settings
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Spanish",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
```

## Step 3: Fill the environment variables

Create a file named `.env` in the same folder as your `app.py` file. Add your OpenAI API key in the `OPENAI_API_KEY` variable.

## Step 4: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000).


# Semantic Kernel
Source: https://docs.chainlit.io/integrations/semantic-kernel



In this tutorial, we'll walk through the steps to create a Chainlit application integrated with [Microsoft's Semantic Kernel](https://github.com/microsoft/semantic-kernel). The integration automatically visualizes Semantic Kernel function calls (like plugins or tools) as Steps in the Chainlit UI.

## Prerequisites

Before getting started, make sure you have the following:

* A working installation of Chainlit
* The `semantic-kernel` package installed
* An LLM API key (e.g., OpenAI, Azure OpenAI) configured for Semantic Kernel
* Basic understanding of Python programming and Semantic Kernel concepts (Kernel, Plugins, Functions)

## Step 1: Create a Python file

Create a new Python file named `app.py` in your project directory. This file will contain the main logic for your LLM application using Semantic Kernel.

## Step 2: Write the Application Logic

In `app.py`, import the necessary packages, set up your Semantic Kernel `Kernel`, add the `SemanticKernelFilter` for Chainlit integration, and define functions to handle chat sessions and incoming messages.

Here's an example demonstrating how to set up the kernel and use the filter:

```python app.py theme={null}
import chainlit as cl
import semantic_kernel as sk
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory

request_settings = OpenAIChatPromptExecutionSettings(
    function_choice_behavior=FunctionChoiceBehavior.Auto(filters={"excluded_plugins": ["ChatBot"]})
)

# Example Native Plugin (Tool)
class WeatherPlugin:
    @kernel_function(name="get_weather", description="Gets the weather for a city")
    def get_weather(self, city: str) -> str:
        """Retrieves the weather for a given city."""
        if "paris" in city.lower():
            return f"The weather in {city} is 20°C and sunny."
        elif "london" in city.lower():
            return f"The weather in {city} is 15°C and cloudy."
        else:
            return f"Sorry, I don't have the weather for {city}."

@cl.on_chat_start
async def on_chat_start():
    # Setup Semantic Kernel
    kernel = sk.Kernel()

    # Add your AI service (e.g., OpenAI)
    # Make sure OPENAI_API_KEY and OPENAI_ORG_ID are set in your environment
    ai_service = OpenAIChatCompletion(service_id="default", ai_model_id="gpt-4o")
    kernel.add_service(ai_service)

    # Import the WeatherPlugin
    kernel.add_plugin(WeatherPlugin(), plugin_name="Weather")
    
    # Instantiate and add the Chainlit filter to the kernel
    # This will automatically capture function calls as Steps
    sk_filter = cl.SemanticKernelFilter(kernel=kernel)

    cl.user_session.set("kernel", kernel)
    cl.user_session.set("ai_service", ai_service)
    cl.user_session.set("chat_history", ChatHistory())

@cl.on_message
async def on_message(message: cl.Message):
    kernel = cl.user_session.get("kernel") # type: sk.Kernel
    ai_service = cl.user_session.get("ai_service") # type: OpenAIChatCompletion
    chat_history = cl.user_session.get("chat_history") # type: ChatHistory

    # Add user message to history
    chat_history.add_user_message(message.content)

    # Create a Chainlit message for the response stream
    answer = cl.Message(content="")

    async for msg in ai_service.get_streaming_chat_message_content(
        chat_history=chat_history,
        user_input=message.content,
        settings=request_settings,
        kernel=kernel,
    ):
        if msg.content:
            await answer.stream_token(msg.content)

    # Add the full assistant response to history
    chat_history.add_assistant_message(answer.content)

    # Send the final message
    await answer.send()
```

## Step 3: Run the Application

To start your app, open a terminal and navigate to the directory containing `app.py`. Then run the following command:

```bash theme={null}
chainlit run app.py -w
```

The `-w` flag tells Chainlit to enable auto-reloading, so you don't need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at [http://localhost:8000](http://localhost:8000). Interact with the bot, and if you ask for the weather (and the LLM uses the tool), you should see a "Weather-get\_weather" step appear in the UI.


