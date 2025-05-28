"use client";

import { useState } from "react";

interface PaperAnalysisProps {
  analysis: {
    goal?: string;
    hypothesis?: string;
    methods?: string;
    results?: string;
    conclusion?: string;
    critique?: string;
    reviewer_questions?: string[];
  };
}

export default function PaperAnalysis({ analysis }: PaperAnalysisProps) {
  const [activeTab, setActiveTab] = useState("summary");

  const tabs = [
    { id: "summary", label: "Summary" },
    { id: "critique", label: "Critique" },
    { id: "questions", label: "Questions" },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="border-b border-gray-200">
        <nav className="flex -mb-px">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="p-6">
        {activeTab === "summary" && (
          <div className="space-y-6">
            {analysis.goal && (
              <div>
                <h3 className="text-lg font-medium text-gray-900">Goal</h3>
                <p className="mt-2 text-gray-600 whitespace-pre-line">
                  {analysis.goal}
                </p>
              </div>
            )}

            {analysis.hypothesis && (
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  Hypothesis
                </h3>
                <p className="mt-2 text-gray-600 whitespace-pre-line">
                  {analysis.hypothesis}
                </p>
              </div>
            )}

            {analysis.methods && (
              <div>
                <h3 className="text-lg font-medium text-gray-900">Methods</h3>
                <p className="mt-2 text-gray-600 whitespace-pre-line">
                  {analysis.methods}
                </p>
              </div>
            )}

            {analysis.results && (
              <div>
                <h3 className="text-lg font-medium text-gray-900">Results</h3>
                <p className="mt-2 text-gray-600 whitespace-pre-line">
                  {analysis.results}
                </p>
              </div>
            )}

            {analysis.conclusion && (
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  Conclusion
                </h3>
                <p className="mt-2 text-gray-600 whitespace-pre-line">
                  {analysis.conclusion}
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === "critique" && (
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Paper Critique
            </h3>
            {analysis.critique ? (
              <p className="mt-2 text-gray-600 whitespace-pre-line">
                {analysis.critique}
              </p>
            ) : (
              <p className="mt-2 text-gray-500 italic">
                No critique available.
              </p>
            )}
          </div>
        )}

        {activeTab === "questions" && (
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Reviewer Questions
            </h3>
            {analysis.reviewer_questions &&
            analysis.reviewer_questions.length > 0 ? (
              <ul className="mt-4 space-y-4">
                {analysis.reviewer_questions.map((question, index) => (
                  <li key={index} className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex">
                      <span className="flex-shrink-0 h-6 w-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-sm font-medium">
                        {index + 1}
                      </span>
                      <p className="ml-3 text-gray-600">{question}</p>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-gray-500 italic">
                No reviewer questions available.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
