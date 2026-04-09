import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from mock_db import get_order, search_products, get_refund_policy

@tool
def lookup_order_status(order_id: str) -> str:
    """Checks the status and delivery date of an order using the order ID (e.g., ORD-101)."""
    data = get_order(order_id)
    if data:
        return f"Order {order_id} is currently {data['status']}. Items: {', '.join(data['items'])}. Expected delivery: {data['delivery_date']}"
    return f"Order {order_id} not found."

@tool
def check_refund_policy() -> str:
    """Returns the store policy regarding returns and refunds."""
    return get_refund_policy()

@tool
def product_search(query: str) -> str:
    """Searches for products in the store catalog by name."""
    results = search_products(query)
    if results:
        return "Found: " + "; ".join([f"{p['name']} (${p['price']})" for p in results])
    return "No products found matching that description."

class SupportAgent:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        tools = [lookup_order_status, check_refund_policy, product_search]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI Customer Support Agent for 'TechMart'. Use tools to help customers with orders, returns, and product info. If you cannot find info, ask for clarification."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def run(self, user_input: str, history: list = []):
        return self.executor.invoke({"input": user_input, "chat_history": history})