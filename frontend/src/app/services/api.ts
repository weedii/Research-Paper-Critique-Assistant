import axios from "axios";
import API_URL from "../constants/api_url";

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

// API interfaces
export interface PaperAnalysis {
  goal?: string;
  hypothesis?: string;
  methods?: string;
  results?: string;
  conclusion?: string;
  critique?: string;
  reviewer_questions?: string[];
  error?: string;
}

// Paper API methods
export const paperApi = {
  /**
   * Upload a PDF for analysis
   * @param file The PDF file to upload
   * @returns The analysis results
   */
  async uploadPaper(file: File): Promise<PaperAnalysis> {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post<PaperAnalysis>(
        "/papers/upload",
        formData
      );
      return response.data;
    } catch (error) {
      console.error("Error uploading paper:", error);

      if (axios.isAxiosError(error) && error.response) {
        // Return the error message from the API if available
        return {
          error:
            error.response.data?.detail ||
            "Failed to upload and analyze the paper.",
        };
      }

      return {
        error: "Failed to upload and analyze the paper. Please try again.",
      };
    }
  },
};

export default api;
