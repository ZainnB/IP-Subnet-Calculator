import React, { useState } from "react";
import ipService from "/src/api/ipService";
import "./SubnetForm.css"; 

export default function SubnetForm({ action, setResult }) {
  const [form, setForm] = useState({});
  const [lastPayload, setLastPayload] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Submitting form with action:", action, "and data:", form);
      const data = await ipService.sendRequest(action, form);
      console.log("Received response:", data);
      setResult(data);
      setLastPayload({
        ...form,
        required_subnets: form.required_subnets || undefined,
        cidr: form.cidr || undefined,
      });
    } catch (err) {
      console.error("Error during form submission:", err);
      setResult({ error: err.detail || "Unknown error" });
      setLastPayload(null);
    }
  };

  const handleDownload = () => {
    if (!lastPayload) return;
    ipService
      .exportData(lastPayload, "csv")
      .catch((err) => alert(err.detail || "Export failed"));
  };

  const fieldMap = {
    calculate: ["ip_address", "subnet_mask"],
    split: ["ip_address", "subnet_mask", "required_subnets"],
    "calculate-v6": ["ip_address", "cidr"],
    "split-v6": ["ip_address", "cidr", "required_subnets"],
    "suggest-mask": ["host_count"],
  };

  const renderFields = () => {
    const fields = fieldMap[action] || [];
    return fields.map((field) => (
      <div key={field} style={{ marginBottom: "10px" }}>
        <input
          name={field}
          placeholder={field.replace("_", " ").toUpperCase()}
          value={form[field] || ""}
          onChange={handleChange}
          required
        />
      </div>
    ));
  };

  return (
    <div className="subnet-form-container">
      <h2 className="form-title">{action.replace("-", " ").toUpperCase()}</h2>
      <form onSubmit={handleSubmit} className="subnet-form">
        {renderFields()}
        <button type="submit" className="form-submit">Submit</button>
      </form>

      {action === "split" && lastPayload && (
        <button onClick={handleDownload} className="form-download">
          Download CSV
        </button>
      )}
    </div>
  );
}
