import React from "react";

const buttons = [
  { label: "IPv4 Calculate", value: "calculate" },
  { label: "IPv4 Split", value: "split" },
  { label: "IPv6 Calculate", value: "calculate-v6" },
  { label: "IPv6 Split", value: "split-v6" },
  { label: "Suggest Mask", value: "suggest-mask" },
];

export default function HomeButtons({ setSelectedAction }) {
  return (
    <div>
      {buttons.map((btn) => (
        <button key={btn.value} onClick={() => setSelectedAction(btn.value)}>
          {btn.label}
        </button>
      ))}
    </div>
  );
}
