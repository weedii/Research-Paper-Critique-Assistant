import dspy
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables for API keys
logger.info("Loading environment variables")
load_dotenv()

# Initialize DSPy with OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    logger.info("Configuring DSPy with OpenAI")
    lm = dspy.LM("openai/gpt-4o-mini", api_key=openai_api_key)
    dspy.configure(lm=lm)
    logger.info("DSPy configured successfully")
else:
    logger.error(
        "No OpenAI API key found. Please set OPENAI_API_KEY environment variable."
    )
    print(
        "Warning: No OpenAI API key found. Please set OPENAI_API_KEY environment variable."
    )


class ExtractResearchParts(dspy.Signature):
    """
    Extract important sections from a research paper
    """

    input = dspy.InputField(desc="Text from a research paper")
    goal = dspy.OutputField(desc="The main goal of the research")
    hypothesis = dspy.OutputField(desc="The main hypothesis or research question")
    methods = dspy.OutputField(desc="The methodology used in the research")
    results = dspy.OutputField(desc="The main results or findings")
    conclusion = dspy.OutputField(desc="The conclusions drawn from the results")


class CritiqueResearchPaper(dspy.Signature):
    """
    Critique a research paper by identifying flaws, gaps, or reasoning problems
    """

    input = dspy.InputField(desc="Text from a research paper")
    critique = dspy.OutputField(desc="Flaws, gaps, or reasoning problems in the paper")


class SuggestReviewerQuestions(dspy.Signature):
    """
    Generate smart, critical follow-up questions for a research paper
    """

    input = dspy.InputField(desc="Text from a research paper")
    questions = dspy.OutputField(desc="Smart, critical follow-up questions")


class PaperExtractor(dspy.Module):
    """
    Module to extract research paper sections
    """

    def __init__(self):
        super().__init__()
        self.extract = dspy.Predict(ExtractResearchParts)

    def forward(self, text: str) -> Dict[str, str]:
        logger.info("Extracting paper sections")
        try:
            result = self.extract(input=text)
            logger.info("Successfully extracted paper sections")
            return {
                "goal": result.goal,
                "hypothesis": result.hypothesis,
                "methods": result.methods,
                "results": result.results,
                "conclusion": result.conclusion,
            }
        except Exception as e:
            logger.error(f"Error extracting paper sections: {str(e)}", exc_info=True)
            raise


class PaperCritic(dspy.Module):
    """
    Module to critique a research paper
    """

    def __init__(self):
        super().__init__()
        self.critique = dspy.Predict(CritiqueResearchPaper)

    def forward(self, text: str) -> Dict[str, str]:
        logger.info("Generating paper critique")
        try:
            result = self.critique(input=text)
            logger.info("Successfully generated paper critique")
            return {"critique": result.critique}
        except Exception as e:
            logger.error(f"Error generating paper critique: {str(e)}", exc_info=True)
            raise


class QuestionGenerator(dspy.Module):
    """
    Module to generate reviewer questions for a research paper
    """

    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(SuggestReviewerQuestions)

    def forward(self, text: str) -> Dict[str, List[str]]:
        logger.info("Generating reviewer questions")
        try:
            result = self.generate(input=text)
            # Convert string to list if needed
            if isinstance(result.questions, str):
                # Split by newlines or numbered items
                questions = [
                    q.strip() for q in result.questions.split("\n") if q.strip()
                ]
                if (
                    not questions
                ):  # If splitting by newline didn't work, try another approach
                    questions = [result.questions]
            else:
                questions = result.questions
            logger.info(f"Successfully generated {len(questions)} reviewer questions")
            return {"questions": questions}
        except Exception as e:
            logger.error(
                f"Error generating reviewer questions: {str(e)}", exc_info=True
            )
            raise


def process_paper_chunk(chunk: str) -> Dict[str, Any]:
    """
    Process a single chunk of a paper with all three DSPy modules

    Args:
        chunk: Text chunk from a paper

    Returns:
        Dictionary with extracted info, critique, and questions
    """
    logger.info(f"Processing paper chunk of length {len(chunk)}")
    try:
        extractor = PaperExtractor()
        critic = PaperCritic()
        question_gen = QuestionGenerator()

        sections = extractor(chunk)
        critique = critic(chunk)
        questions = question_gen(chunk)

        result = {**sections, **critique, **questions}
        logger.info("Successfully processed paper chunk")
        return result
    except Exception as e:
        logger.error(f"Error processing paper chunk: {str(e)}", exc_info=True)
        raise


def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate results from multiple chunks

    Args:
        results: List of results from each chunk

    Returns:
        Aggregated results
    """
    logger.info(f"Aggregating results from {len(results)} chunks")
    aggregated = {
        "goal": "",
        "hypothesis": "",
        "methods": "",
        "results": "",
        "conclusion": "",
        "critique": "",
        "reviewer_questions": [],
    }

    # Combine text fields
    for field in ["goal", "hypothesis", "methods", "results", "conclusion", "critique"]:
        combined = "\n\n".join([r.get(field, "") for r in results if r.get(field)])
        aggregated[field] = combined
        logger.info(f"Aggregated {field}: {len(combined)} characters")

    # Combine and deduplicate questions
    all_questions = []
    for r in results:
        if r.get("questions"):
            all_questions.extend(r.get("questions", []))

    # Simple deduplication by checking if a question is a substring of another
    unique_questions = []
    for q in all_questions:
        is_duplicate = False
        for existing_q in unique_questions:
            if q in existing_q or existing_q in q:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_questions.append(q)

    aggregated["reviewer_questions"] = unique_questions
    logger.info(f"Aggregated {len(unique_questions)} unique reviewer questions")

    return aggregated


def analyze_paper(text: str, chunk_size: int = 4000) -> Dict[str, Any]:
    """
    Analyze a paper by processing it in chunks

    Args:
        text: Full text of the paper
        chunk_size: Size of each chunk

    Returns:
        Analysis results
    """
    logger.info(f"Starting paper analysis with text of length {len(text)}")
    from ..utils.pdf_utils import chunk_text

    # Validate input
    if not text or not isinstance(text, str):
        logger.error("Invalid input: text must be a non-empty string")
        return {
            "goal": "Error: Invalid input text",
            "hypothesis": "",
            "methods": "",
            "results": "",
            "conclusion": "",
            "critique": "Error: Invalid input text",
            "reviewer_questions": ["Could not process due to invalid input"],
        }

    # Limit chunk size to prevent system overload
    MAX_CHUNK_SIZE = 8000
    if chunk_size > MAX_CHUNK_SIZE:
        logger.warning(
            f"Chunk size {chunk_size} exceeds maximum. Using {MAX_CHUNK_SIZE} instead."
        )
        chunk_size = MAX_CHUNK_SIZE

    try:
        # TEMPORARY: Skip chunking for testing - just process the full text
        # chunks = chunk_text(text, chunk_size=chunk_size)
        # logger.info(f"Split paper into {len(chunks)} chunks")
        chunks = [text]  # Process the entire text as one chunk
        logger.info("Processing entire text as one chunk for testing")

        if not chunks:
            logger.error("No chunks were generated from the paper text")
            return {
                "goal": "Error: Could not extract text from the paper",
                "hypothesis": "",
                "methods": "",
                "results": "",
                "conclusion": "",
                "critique": "Error: Could not extract text for critique",
                "reviewer_questions": [
                    "Could not generate questions due to text extraction error"
                ],
            }

        results = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            try:
                chunk_result = process_paper_chunk(chunk)
                results.append(chunk_result)
                logger.info(f"Successfully processed chunk {i+1}/{len(chunks)}")
            except Exception as e:
                logger.error(f"Error processing chunk {i+1}/{len(chunks)}: {str(e)}")
                # Continue with next chunk even if one fails

        if not results:
            logger.error("All chunks failed to process")
            return {
                "goal": "Error: Failed to analyze the paper",
                "hypothesis": "",
                "methods": "",
                "results": "",
                "conclusion": "",
                "critique": "Error: Failed to analyze the paper",
                "reviewer_questions": [
                    "Failed to generate questions due to analysis error"
                ],
            }

        logger.info(
            f"Aggregating results from {len(results)} successfully processed chunks"
        )
        final_result = aggregate_results(results)
        logger.info("Paper analysis complete")
        return final_result

    except Exception as e:
        logger.error(f"Critical error during paper analysis: {str(e)}", exc_info=True)
        return {
            "goal": "Error: Critical failure during analysis",
            "hypothesis": "",
            "methods": "",
            "results": "",
            "conclusion": "",
            "critique": f"Error: Analysis failed - {str(e)}",
            "reviewer_questions": ["Analysis failed due to system error"],
        }
