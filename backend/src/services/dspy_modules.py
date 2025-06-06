import dspy
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from ..utils.pdf_utils import split_into_chunks

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
    lm = dspy.LM(
        "openai/gpt-4o",
        api_key=openai_api_key,
        cache=False,
        temperature=0.5,
        # max_tokens=2000,
    )
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


class ExtractResearchQuestions(dspy.Signature):
    """
    Extract research questions that the paper itself poses and addresses
    """

    input = dspy.InputField(desc="Text from a research paper")
    main_question = dspy.OutputField(
        desc="The primary research question that the paper addresses"
    )
    sub_questions = dspy.OutputField(
        desc="List of secondary questions as plain text without numbers, bullets, or enumeration"
    )
    addressed_questions = dspy.OutputField(
        desc="How the paper addresses these questions (methods/approaches used)"
    )


class AggregateChunks(dspy.Signature):
    """Aggregate multiple chunk results into a single coherent result"""

    chunks = dspy.InputField(desc="List of chunk results to be aggregated")
    goal = dspy.OutputField(desc="The main goal of the research")
    hypothesis = dspy.OutputField(desc="The main hypothesis or research question")
    methods = dspy.OutputField(desc="The methodology used in the research")
    results = dspy.OutputField(desc="The main results or findings")
    conclusion = dspy.OutputField(desc="The conclusions drawn from the results")
    critique = dspy.OutputField(desc="Flaws, gaps, or reasoning problems in the paper")
    main_question = dspy.OutputField(
        desc="The primary research question that the paper addresses"
    )
    sub_questions = dspy.OutputField(desc="List of secondary questions")
    addressed_questions = dspy.OutputField(
        desc="How the paper addresses these questions"
    )


class PaperExtractor(dspy.Module):
    """
    Module to extract research paper sections using chain of thought reasoning
    """

    def __init__(self):
        super().__init__()
        # Use ChainOfThought for step-by-step reasoning
        self.extract = dspy.ChainOfThought(ExtractResearchParts)

    def forward(self, text: str) -> Dict[str, str]:
        logger.info("Extracting paper sections using chain-of-thought reasoning")
        try:
            # ChainOfThought will break down the extraction process
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
    Module to critique a research paper using chain of thought reasoning
    """

    def __init__(self):
        super().__init__()
        # Use ChainOfThought for systematic analysis and critique
        self.critique = dspy.ChainOfThought(CritiqueResearchPaper)

    def forward(self, text: str) -> Dict[str, str]:
        logger.info("Generating paper critique using chain-of-thought reasoning")
        try:
            # ChainOfThought will analyze the paper systematically
            result = self.critique(input=text)
            logger.info("Successfully generated paper critique")
            return {"critique": result.critique}
        except Exception as e:
            logger.error(f"Error generating paper critique: {str(e)}", exc_info=True)
            raise


class QuestionExtractor(dspy.Module):
    """
    Module to extract research questions from the paper
    """

    def __init__(self):
        super().__init__()
        self.extract = dspy.Predict(ExtractResearchQuestions)

    def forward(self, text: str) -> Dict[str, Any]:
        logger.info("Extracting research questions from paper")
        try:
            result = self.extract(input=text)

            # Return the object structure
            questions_data = {
                "reviewer_questions": {
                    "main_question": result.main_question,
                    "sub_questions": self._format_sub_questions(result.sub_questions),
                    "addressed_questions": result.addressed_questions,
                }
            }

            logger.info("Successfully extracted research questions from paper")
            return questions_data
        except Exception as e:
            logger.error(
                f"Error extracting research questions: {str(e)}", exc_info=True
            )
            raise

    def _format_sub_questions(self, questions: str) -> List[str]:
        """Format sub-questions into a clean list"""
        if isinstance(questions, list):
            return questions
        # Split by newlines or numbered items and clean up
        questions_list = [q.strip() for q in questions.split("\n") if q.strip()]
        if not questions_list:
            # If no clear separation, return as single item
            return [questions] if questions else []
        return questions_list


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
        question_extractor = QuestionExtractor()

        sections = extractor(chunk)
        critique = critic(chunk)
        questions = question_extractor(chunk)

        result = {**sections, **critique, **questions}
        logger.info("Successfully processed paper chunk")
        return result
    except Exception as e:
        logger.error(f"Error processing paper chunk: {str(e)}", exc_info=True)
        raise


def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate results from multiple chunks using DSPy's Predict module
    """
    logger.info(f"Aggregating results from {len(results)} chunks")

    # For single chunk, just return it directly
    if len(results) == 1:
        logger.info("Only one chunk, returning as-is")
        return results[0]

    try:
        # Use Predict to generate the aggregated result
        aggregator = dspy.Predict(AggregateChunks)

        # Convert results to a string representation for the LLM
        chunks_str = str(results)

        # Get the aggregated result
        aggregated_result = aggregator(chunks=chunks_str)

        # Format the output to match the expected structure
        aggregated = {
            "goal": aggregated_result.goal,
            "hypothesis": aggregated_result.hypothesis,
            "methods": aggregated_result.methods,
            "results": aggregated_result.results,
            "conclusion": aggregated_result.conclusion,
            "critique": aggregated_result.critique,
            "reviewer_questions": {
                "main_question": aggregated_result.main_question,
                "sub_questions": (
                    aggregated_result.sub_questions.split("\n")
                    if isinstance(aggregated_result.sub_questions, str)
                    else aggregated_result.sub_questions
                ),
                "addressed_questions": aggregated_result.addressed_questions,
            },
        }

        logger.info("Successfully aggregated results using DSPy Predict")
        return aggregated

    except Exception as e:
        logger.error(
            f"Error using DSPy Predict for aggregation: {str(e)}", exc_info=True
        )
        logger.info("Falling back to basic aggregation method")

        # Fallback to a simpler aggregation method
        aggregated = {
            "goal": "",
            "hypothesis": "",
            "methods": "",
            "results": "",
            "conclusion": "",
            "critique": "",
            "reviewer_questions": {
                "main_question": "",
                "sub_questions": [],
                "addressed_questions": "",
            },
        }

        # Combine text fields
        for field in [
            "goal",
            "hypothesis",
            "methods",
            "results",
            "conclusion",
            "critique",
        ]:
            combined = "\n\n".join([r.get(field, "") for r in results if r.get(field)])
            aggregated[field] = combined

        # Aggregate reviewer questions
        main_questions = []
        all_sub_questions = []
        addressed_questions = []

        for r in results:
            if r.get("reviewer_questions"):
                rq = r.get("reviewer_questions", {})
                if rq.get("main_question"):
                    main_questions.append(rq.get("main_question"))
                if rq.get("sub_questions"):
                    all_sub_questions.extend(rq.get("sub_questions", []))
                if rq.get("addressed_questions"):
                    addressed_questions.append(rq.get("addressed_questions"))

        # Combine the questions
        aggregated["reviewer_questions"] = {
            "main_question": main_questions[0] if main_questions else "",
            "sub_questions": list(set(all_sub_questions)),  # Remove duplicates
            "addressed_questions": (
                addressed_questions[0] if addressed_questions else ""
            ),
        }

        logger.info("Completed fallback aggregation")
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
        # Split the paper into manageable chunks
        # chunks = split_into_chunks(text, chunk_size=chunk_size)
        chunks = [text]
        logger.info(f"Split paper into {len(chunks)} chunks")

        if not chunks:
            logger.warning(
                "No chunks were generated, using full text as a single chunk"
            )
            chunks = [text]

        # Limit to a reasonable number of chunks if the paper is very large
        # MAX_CHUNKS = 5
        # if len(chunks) > MAX_CHUNKS:
        #     logger.warning(
        #         f"Limiting analysis to first {MAX_CHUNKS} chunks for performance"
        #     )
        #     chunks = chunks[:MAX_CHUNKS]

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
