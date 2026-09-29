# LangGraph Core Concepts & Definitions

## Overview
**LangGraph** is a framework developed by LangChain for building stateful, multi-actor LLM applications using graph architectures. Unlike traditional linear chains, LangGraph natively supports **cyclical flows (loops)**, **persistence**, and **complex agent logic**.

---

## 1. Core Graph Mechanics

### State
* **Definition**: The central shared data structure (typically a `TypedDict` or `Pydantic` model) passed to every node in the graph.
* **Purpose**: Serves as the graph's memory across execution steps.
* **Reducers**: Functions attached to state keys via `Annotated` that define how node outputs update existing state values.
  * *Example*: `Annotated[list, add_messages]` appends new entries to a list rather than replacing it.

### Nodes
* **Definition**: Python functions or runnable objects representing individual steps of computation (e.g., calling an LLM, querying a database, running a tool).
* **Signature**: Accepts the current `State` as input and returns a `dict` updating one or more state keys.
* **Built-in Nodes**: Includes specialized utility nodes such as `ToolNode` for executing tool calls automatically.

### Edges
* **Definition**: Structural connections defining control flow transitions between nodes.
* **Normal Edges**: Static transitions linking `Node A` directly to `Node B`.
* **Conditional Edges**: Dynamic routing decisions based on logic that evaluates the current state.
* **Control Flow Markers**:
  * `START`: Entry point where execution begins.
  * `END`: Exit point signaling graph completion.

---

## 2. Advanced Features

### Checkpointers & Persistence
* **Definition**: Mechanisms that record a snapshot of the graph state after every step.
* **Key Uses**:
  * **Short-term memory**: Retaining conversational history using a `thread_id`.
  * **Fault tolerance**: Resuming execution from the last valid checkpoint upon errors.

### Human-in-the-Loop (HITL)
* **Definition**: Pausing execution before or after specific nodes using `interrupt_before` or `interrupt_after`.
* **Purpose**: Requires human review, input, or explicit approval before taking sensitive actions (e.g., executing code, sending emails).

### Time Travel
* **Definition**: The ability to inspect, fork, or rewind execution back to a specific checkpoint in the thread history.

---

## 3. Quick Reference Table

| Concept | Primary Function |
| :--- | :--- |
| **`StateGraph`** | Builder class used to define nodes, edges, and state schemas. |
| **`CompiledGraph`** | Executable graph instance created via `.compile()`. |
| **Reducer** | Logic controlling how new node outputs merge into existing state keys. |
| **Thread ID** | Unique identifier linking execution runs to persistent state history. |
| **Conditional Edge** | Router function returning the string name of the next node to execute. |
