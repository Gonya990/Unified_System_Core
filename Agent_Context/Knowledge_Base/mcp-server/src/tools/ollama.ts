import axios from 'axios';

export async function checkOllamaHealth() {
    // Try localhost first (run on host), then host.docker.internal (if inside container)
    const urls = [
        'http://localhost:11434/api/tags',
        'http://127.0.0.1:11434/api/tags',
        'http://host.docker.internal:11434/api/tags'
    ];

    for (const url of urls) {
        try {
            const response = await axios.get(url, { timeout: 2000 });
            if (response.status === 200) {
                return {
                    status: 'online',
                    url: url,
                    models: response.data.models?.length || 0
                };
            }
        } catch (error) {
            // Ignore and try next URL
        }
    }

    throw new Error("Ollama is unreachable. Checked: " + urls.join(", "));
}
