"use client";

import { useState } from "react";
import FileUpload from "./components/FileUpload";
import PaperAnalysis from "./components/PaperAnalysis";
import { paperApi, PaperAnalysis as PaperAnalysisType } from "./services/api";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] =
    useState<PaperAnalysisType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await paperApi.uploadPaper(file);

      if (result.error) {
        setError(result.error);
        setAnalysisResult(null);
      } else {
        setAnalysisResult(result);
      }
    } catch (err) {
      setError("An unexpected error occurred. Please try again.");
      setAnalysisResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Research Paper Critique Assistant
          </h1>
          <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
            Upload your research paper for automatic analysis, summary, and
            critique
          </p>
        </div>

        {!analysisResult ? (
          <div className="mt-10">
            <FileUpload onFileUpload={handleFileUpload} isLoading={isLoading} />

            {error && (
              <div className="mt-6 bg-red-50 border-l-4 border-red-400 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg
                      className="h-5 w-5 text-red-400"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                      />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="mt-10">
            <div className="mb-8 flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">
                Analysis Results
              </h2>
              <button
                onClick={() => setAnalysisResult(null)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
              >
                <svg
                  className="-ml-1 mr-2 h-5 w-5 text-gray-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16l-4-4m0 0l4-4m-4 4h18"
                  />
                </svg>
                Upload another paper
              </button>
            </div>

            <PaperAnalysis analysis={analysisResult} />
          </div>
        )}
      </div>
    </div>
  );
}
