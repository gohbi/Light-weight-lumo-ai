#!/usr/bin/env python3
"""
Example usage script for the Lightweight Lumo AI API.

This script demonstrates how to interact with the API once it's running.
Make sure the API server is running first:
    uvicorn app:app --host 0.0.0.0 --port 8000
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000/v1/completions"


def chat(prompt: str, max_tokens: int = 128, temperature: float = 0.7):
    """
    Send a chat prompt to the API and return the response.
    
    Args:
        prompt: The input prompt (use format "User: ... \\nAssistant:")
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation (0.0-1.0)
    
    Returns:
        The generated text response
    """
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["generated_text"]
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to API. Make sure the server is running."
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. The model might be taking too long to respond."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def main():
    """Run example conversations."""
    print("=" * 60)
    print("Lightweight Lumo AI - Example Usage")
    print("=" * 60)
    print()
    
    # Example 1: Simple question
    print("Example 1: Simple factual question")
    print("-" * 60)
    prompt1 = "User: What is the capital of France?\nAssistant:"
    print(f"Prompt: {prompt1}")
    response1 = chat(prompt1, max_tokens=50)
    print(f"Response: {response1}")
    print()
    
    # Example 2: Creative task
    print("Example 2: Creative writing")
    print("-" * 60)
    prompt2 = "User: Write a short haiku about programming.\nAssistant:"
    print(f"Prompt: {prompt2}")
    response2 = chat(prompt2, max_tokens=100, temperature=0.8)
    print(f"Response: {response2}")
    print()
    
    # Example 3: Code explanation
    print("Example 3: Code explanation")
    print("-" * 60)
    prompt3 = "User: Explain what this Python code does: for i in range(10): print(i)\nAssistant:"
    print(f"Prompt: {prompt3}")
    response3 = chat(prompt3, max_tokens=150)
    print(f"Response: {response3}")
    print()
    
    print("=" * 60)
    print("Try modifying this script to test your own prompts!")
    print("=" * 60)


if __name__ == "__main__":
    main()
