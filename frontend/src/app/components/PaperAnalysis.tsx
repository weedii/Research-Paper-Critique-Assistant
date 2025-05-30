"use client";

import { useState } from "react";

interface ReviewerQuestions {
  main_question?: string;
  sub_questions?: string[];
  addressed_questions?: string;
}

interface PaperAnalysisProps {
  analysis: {
    goal?: string;
    hypothesis?: string;
    methods?: string;
    results?: string;
    conclusion?: string;
    critique?: string;
    reviewer_questions?: ReviewerQuestions;
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
              Research Questions
            </h3>
            {analysis.reviewer_questions ? (
              <div className="mt-4 space-y-6">
                {analysis.reviewer_questions.main_question && (
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="text-md font-medium text-blue-900 mb-2">
                      Main Research Question
                    </h4>
                    <p className="text-blue-800">
                      {analysis.reviewer_questions.main_question}
                    </p>
                  </div>
                )}

                {analysis.reviewer_questions.sub_questions &&
                  analysis.reviewer_questions.sub_questions.length > 0 && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-md font-medium text-gray-900 mb-2">
                        Sub Questions
                      </h4>
                      <ul className="space-y-2">
                        {analysis.reviewer_questions.sub_questions.map(
                          (question, index) => (
                            <li key={index} className="flex">
                              <span className="flex-shrink-0 h-6 w-6 bg-gray-200 text-gray-800 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                                {index + 1}
                              </span>
                              <p className="text-gray-700">{question}</p>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}

                {analysis.reviewer_questions.addressed_questions && (
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="text-md font-medium text-green-900 mb-2">
                      How Questions Are Addressed
                    </h4>
                    <p className="text-green-800 whitespace-pre-line">
                      {analysis.reviewer_questions.addressed_questions}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className="mt-2 text-gray-500 italic">
                No research questions available.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
