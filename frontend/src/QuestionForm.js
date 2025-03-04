import { useState } from "react";
import axios from "axios";
import { BounceLoader } from "react-spinners";
import ReactMarkdown from "react-markdown";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

const Expander = ({ title, content }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="expander">
      <b onClick={() => setIsOpen(!isOpen)} className="expander-title">
        {title}
      </b>
      {isOpen && <p className="expander-content">{content}</p>}
    </div>
  );
};

function QuestionForm() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    setAnswer("");
    setIsLoading(true);
    e.preventDefault();
    console.log("your question: ", question);
    const response = await API.post("/chat", { message: question });
    setAnswer(response.data.answer);
    console.log("response.data.documents: ", response.data.documents);
    setDocuments(response.data.documents);
    setIsLoading(false);
  };

  const handleIndex = async (e) => {
    setAnswer("");
    setIsLoading(true);
    e.preventDefault();
    const response = await API.post("/indexing", { message: question });
    setAnswer(response.data.response);
    setIsLoading(false);
  };
  return (
    <>
      <form className="form">
        <input
          className="form-input"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button className="form-button" type="submit" onClick={handleSubmit}>
          Submit
        </button>
        <button
          className="form-button"
          style={{ backgroundColor: "red" }}
          onClick={handleIndex}
        >
          Index
        </button>
      </form>
      {isLoading && (
        <div className="loader-container">
          <BounceLoader color="#3498db" size={30} />
        </div>
      )}
      {answer && (
        <div className="results-container">
          <div className="results-answer">
            <h2>Answer:</h2>
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
          <div className="results-documents">
            <h2>Documents:</h2>
            <ul>
              {documents.map((document, index) => (
                <li key={index}>
                  <Expander
                    title={
                      document.page_content.slice(0, 50) +
                      (document.page_content.length > 50 ? "..." : "")
                    }
                    content={document.page_content}
                  />
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </>
  );
}

export default QuestionForm;
