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
    <div className="bg-card rounded-lg shadow-xl overflow-hidden border border-border">
      <div className="border-b border-border">
        <nav className="flex -mb-px">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-6 text-center border-b-2 font-medium text-sm transition-all ${
                activeTab === tab.id
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="p-6">
        {activeTab === "summary" && (
          <div className="space-y-8">
            {analysis.goal && (
              <div className="card">
                <h3 className="section-heading">Goal</h3>
                <p className="section-content">{analysis.goal}</p>
              </div>
            )}

            {analysis.hypothesis && (
              <div className="card">
                <h3 className="section-heading">Hypothesis</h3>
                <p className="section-content">{analysis.hypothesis}</p>
              </div>
            )}

            {analysis.methods && (
              <div className="card">
                <h3 className="section-heading">Methods</h3>
                <p className="section-content">{analysis.methods}</p>
              </div>
            )}

            {analysis.results && (
              <div className="card">
                <h3 className="section-heading">Results</h3>
                <p className="section-content">{analysis.results}</p>
              </div>
            )}

            {analysis.conclusion && (
              <div className="card">
                <h3 className="section-heading">Conclusion</h3>
                <p className="section-content">{analysis.conclusion}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "critique" && (
          <div className="card">
            <h3 className="section-heading">Paper Critique</h3>
            {analysis.critique ? (
              <p className="section-content">{analysis.critique}</p>
            ) : (
              <p className="text-muted-foreground italic">
                No critique available.
              </p>
            )}
          </div>
        )}

        {activeTab === "questions" && (
          <div>
            <h3 className="text-xl font-bold text-foreground mb-4">
              Research Questions
            </h3>
            {analysis.reviewer_questions ? (
              <div className="space-y-6">
                {analysis.reviewer_questions.main_question && (
                  <div className="bg-primary/10 p-5 rounded-lg border border-primary/30 card">
                    <h4 className="text-md font-medium text-primary-foreground mb-2">
                      Main Research Question
                    </h4>
                    <p className="text-foreground">
                      {analysis.reviewer_questions.main_question}
                    </p>
                  </div>
                )}

                {analysis.reviewer_questions.sub_questions &&
                  analysis.reviewer_questions.sub_questions.length > 0 && (
                    <div className="bg-secondary p-5 rounded-lg card">
                      <h4 className="text-md font-medium text-foreground mb-3">
                        Sub Questions
                      </h4>
                      <ul className="space-y-3">
                        {analysis.reviewer_questions.sub_questions.map(
                          (question, index) => (
                            <li key={index} className="flex items-start">
                              <span className="flex-shrink-0 h-6 w-6 bg-muted text-foreground rounded-full flex items-center justify-center text-sm font-medium mr-3">
                                {index + 1}
                              </span>
                              <p className="text-muted-foreground">
                                {question}
                              </p>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}

                {analysis.reviewer_questions.addressed_questions && (
                  <div className="bg-accent/10 p-5 rounded-lg border border-accent/30 card">
                    <h4 className="text-md font-medium text-accent-foreground mb-2">
                      How Questions Are Addressed
                    </h4>
                    <p className="text-foreground whitespace-pre-line">
                      {analysis.reviewer_questions.addressed_questions}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-muted-foreground italic">
                No research questions available.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
