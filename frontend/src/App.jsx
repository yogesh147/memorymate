import { useEffect, useState } from "react";

import {
  deleteMemory,
  getMemories,
  searchMemories,
  uploadMemory,
} from "./api";


function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);


  async function loadMemories() {
    try {
      const data = await getMemories();
      setMemories(data);
    } catch (error) {
      console.error(error);
    }
  }


  useEffect(() => {
    loadMemories();
  }, []);


  async function handleSearch(event) {
    event.preventDefault();

    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const data = await searchMemories(
          question
      );

      setAnswer(data.answer);
      setSources(data.memories);
    } catch (error) {
      setAnswer(
          "Something went wrong while searching your memories."
      );
    } finally {
      setLoading(false);
    }
  }


  async function handleUpload(event) {
    const file =
        event.target.files?.[0];

    if (!file) return;

    setUploading(true);

    try {
      await uploadMemory(file);
      await loadMemories();

      alert(
          "Memory imported successfully!"
      );
    } catch (error) {
      alert(
          "Could not upload this file."
      );
    } finally {
      setUploading(false);
    }
  }


  async function handleDelete(id) {
    await deleteMemory(id);
    await loadMemories();
  }


  return (
      <div className="app">

        <header className="navbar">
          <div className="brand">
            <div className="logo">
              🧠
            </div>

            <div>
              <h1>MemoryMate</h1>

              <span>
              Your private memory layer
            </span>
            </div>
          </div>

          <label className="upload">
            {uploading
                ? "Uploading..."
                : "+ Add memories"}

            <input
                type="file"
                accept=".txt,.md"
                onChange={handleUpload}
                hidden
            />
          </label>
        </header>


        <main className="container">

          <section className="hero">

            <div className="badge">
              ✨ Built for a friend
            </div>

            <h2>
              Remember the little things.
            </h2>

            <p>
              Ask MemoryMate about your
              conversations, plans, and
              friends instead of searching
              through hundreds of messages.
            </p>


            <form
                className="search-box"
                onSubmit={handleSearch}
            >
              <span>🔍</span>

              <input
                  value={question}
                  onChange={(event) =>
                      setQuestion(
                          event.target.value
                      )
                  }
                  placeholder="What do you remember about Rahul?"
              />

              <button>
                {loading
                    ? "Thinking..."
                    : "Ask MemoryMate"}
              </button>
            </form>


            <div className="suggestions">

              {[
                "What does Rahul like?",
                "What startup ideas did we discuss?",
                "When is Rahul's birthday?",
              ].map((item) => (
                  <button
                      key={item}
                      onClick={() =>
                          setQuestion(item)
                      }
                  >
                    {item}
                  </button>
              ))}

            </div>

          </section>


          {answer && (

              <section className="answer-card">

                <div className="answer-header">
                  <span>💡</span>

                  <div>
                    <small>
                      MEMORYMATE
                    </small>

                    <h3>
                      You mentioned this before…
                    </h3>
                  </div>
                </div>

                <p className="answer">
                  {answer}
                </p>


                {sources.length > 0 && (

                    <div className="sources">

                      <h4>
                        Sources
                      </h4>

                      {sources.map(
                          (memory) => (

                              <div
                                  className="source"
                                  key={memory.id}
                              >
                                <div>
                                  <strong>
                                    {memory.source ||
                                        "Memory"}
                                  </strong>

                                  <p>
                                    {memory.content}
                                  </p>
                                </div>
                              </div>
                          )
                      )}

                    </div>
                )}

              </section>
          )}


          <section className="section">

            <div className="section-title">
              <div>
              <span className="eyebrow">
                MEMORY VAULT
              </span>

                <h3>
                  Recent memories
                </h3>
              </div>

              <span>
              {memories.length} memories
            </span>
            </div>


            <div className="memory-grid">

              {memories.map(
                  (memory) => (

                      <article
                          className="memory-card"
                          key={memory.id}
                      >

                        <div className="memory-top">

                    <span className="memory-icon">
                      💭
                    </span>

                          <button
                              className="delete"
                              onClick={() =>
                                  handleDelete(
                                      memory.id
                                  )
                              }
                          >
                            ×
                          </button>

                        </div>

                        <p>
                          {memory.content}
                        </p>

                        <footer>
                    <span>
                      {memory.source ||
                          "Personal memory"}
                    </span>
                        </footer>

                      </article>
                  )
              )}

            </div>

          </section>

        </main>


        <footer className="footer">
        <span>
          🧠 MemoryMate
        </span>

          <span>
          Built for a friend ❤️
        </span>
        </footer>

      </div>
  );
}


export default App;
