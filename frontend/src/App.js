import logo from "./logo.svg";
import "./App.css";
import QuestionForm from "./QuestionForm";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Welcome to FullStack RAG</p>
        <QuestionForm />
      </header>
    </div>
  );
}

export default App;
