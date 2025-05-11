import React from "react";
import "./ResultDisplay.css";

export default function ResultDisplay({ result }) {
  console.log("ResultDisplay received result:", result);
  if (!result) return null;

  if (typeof result === "object" && result.error) {
    return <div className="error-message">Error: {result.error}</div>;
  }

  if (Array.isArray(result)) {
    return (
      <div className="result-container">
        <h2 className="result-title">Subnet Results</h2>
        <ul className="result-list">
          {result.map((item, index) => (
            <li key={index} className="result-item">
              {Object.entries(item).map(([key, value]) => (
                <div key={key} className="result-field">
                  <span className="result-key">{key}:</span>{" "}
                  <span className="result-value">{value.toString()}</span>
                </div>
              ))}
              <hr className="result-separator" />
            </li>
          ))}
        </ul>
      </div>
    );
  }

  if (typeof result === "object") {
    return (
      <div className="result-container">
        <h2 className="result-title">Calculation Result</h2>
        <div className="result-single">
          {Object.entries(result).map(([key, value]) => (
            <div key={key} className="result-field">
              <span className="result-key">{key}:</span>{" "}
              <span className="result-value">{value.toString()}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return <div className="error-message">Unexpected result format.</div>;
}
