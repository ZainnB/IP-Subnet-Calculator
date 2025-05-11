import React, { useState } from "react";
import "./App.css";
import HomeButtons from "/components/HomeButtons";
import SubnetForm from "/components/SubnetForm";
import ResultDisplay from "/components/ResultDisplay";

function App() {
  const [selectedAction, setSelectedAction] = useState(null);
  const [result, setResult] = useState(null);

  return (
    <div className="app-container">
      <h1>IP Subnet Calculator Tool</h1>
      <div className="section">
        <h2>Choose an Action</h2>
        <div className="buttons-container">
        <HomeButtons setSelectedAction={setSelectedAction} />
        </div>
        {selectedAction && (
          <SubnetForm action={selectedAction} setResult={setResult} />
        )}
        {result && (
          <div className="result-card">
            <ResultDisplay result={result} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
