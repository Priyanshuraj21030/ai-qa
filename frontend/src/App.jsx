import { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [question, setQuestion] = useState('');
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [initialLoad, setInitialLoad] = useState(true);
    const [pagination, setPagination] = useState({
        page: 1,
        pageSize: 10,
        total: 0,
        totalPages: 0
    });

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async (page = 1) => {
        try {
            const response = await fetch(`http://localhost:8000/history?page=${page}&page_size=${pagination.pageSize}`);
            const data = await response.json();
            setHistory(data.items);
            setPagination({
                page: data.page,
                pageSize: data.page_size,
                total: data.total,
                totalPages: data.total_pages
            });
        } catch (err) {
            setError('Failed to load history. Please try refreshing the page.');
        } finally {
            setInitialLoad(false);
        }
    };

    const handlePageChange = (newPage) => {
        fetchHistory(newPage);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.detail && data.detail.includes("Model is loading")) {
                    setError("The AI model is warming up. Please try again in a few seconds.");
                } else {
                    throw new Error(data.detail || 'Failed to get answer');
                }
                return;
            }

            await fetchHistory();
            setQuestion('');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (initialLoad) {
        return (
            <div className="container">
                <div className="loading-spinner">
                    <div className="spinner" />
                    <p>Loading application...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <h1>AI Q&A Assistant</h1>

            <form onSubmit={handleSubmit} className="question-form">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask me anything..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !question.trim()}>
                    {loading ? 'Thinking...' : 'Ask Question'}
                </button>
            </form>

            {error && (
                <div className="error-message">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {loading && (
                <div className="loading-spinner">
                    <div className="spinner" />
                    <p>Thinking about your question...</p>
                </div>
            )}

            <div className="history-section">
                <h2>Previous Questions & Answers</h2>
                {history.length === 0 ? (
                    <p className="no-history">
                        No questions yet. Start by asking something!
                    </p>
                ) : (
                    <>
                        <div className="qa-list">
                            {history.map((item) => (
                                <div key={item.id} className="qa-item">
                                    <p className="question">Q: {item.question}</p>
                                    <p className="answer">A: {item.answer}</p>
                                    <small className="timestamp">
                                        {new Date(item.timestamp).toLocaleString()}
                                    </small>
                                </div>
                            ))}
                        </div>

                        {pagination.totalPages > 1 && (
                            <div className="pagination">
                                <button
                                    onClick={() => handlePageChange(pagination.page - 1)}
                                    disabled={pagination.page === 1}
                                >
                                    Previous
                                </button>
                                <span>
                                    Page {pagination.page} of {pagination.totalPages}
                                </span>
                                <button
                                    onClick={() => handlePageChange(pagination.page + 1)}
                                    disabled={pagination.page === pagination.totalPages}
                                >
                                    Next
                                </button>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}

export default App;
