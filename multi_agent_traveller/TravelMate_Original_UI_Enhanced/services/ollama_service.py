import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3.5:4b"


def ask_ollama(prompt, model=MODEL_NAME):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,   # skips Qwen3's <think> text (needs recent Ollama)
    }

    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=120)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Start it with 'ollama serve'."
    except requests.exceptions.Timeout:
        return "Error: Ollama took too long to respond."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(ask_ollama("Suggest 5 tourist places in Manali."))