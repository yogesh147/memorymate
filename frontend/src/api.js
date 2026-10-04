const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000";

export async function searchMemories(
    question,
    person = null
) {
    const response = await fetch(
        `${API_URL}/api/search`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
                person,
            }),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Search failed"
        );
    }

    return response.json();
}


export async function getMemories() {
    const response = await fetch(
        `${API_URL}/api/memories`
    );

    return response.json();
}


export async function uploadMemory(file) {
    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    const response = await fetch(
        `${API_URL}/api/memories/upload`,
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        throw new Error(
            "Upload failed"
        );
    }

    return response.json();
}


export async function deleteMemory(id) {
    const response = await fetch(
        `${API_URL}/api/memories/${id}`,
        {
            method: "DELETE",
        }
    );

    return response.json();
}
