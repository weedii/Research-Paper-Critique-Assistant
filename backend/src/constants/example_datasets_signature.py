# Example datasets for each signature
RESEARCH_PARTS_EXAMPLES = [
    {
        "input": """Title: Impact of Sleep Duration on Cognitive Performance
        Abstract: This study investigated the relationship between sleep duration and cognitive performance in university students. 
        We hypothesized that students with optimal sleep duration (7-9 hours) would demonstrate superior cognitive performance.
        Methods: 150 university students were monitored for sleep patterns using actigraphy watches over 2 weeks. 
        Cognitive performance was assessed using standardized tests.
        Results: Students sleeping 7-9 hours showed 23% better cognitive performance compared to those sleeping less than 6 hours.
        Conclusion: Optimal sleep duration significantly improves cognitive performance in university students.""",
        "goal": "To examine how sleep duration affects cognitive performance in university students",
        "hypothesis": "Students with optimal sleep duration (7-9 hours) will show better cognitive performance",
        "methods": "150 university students were monitored using actigraphy watches for 2 weeks, with cognitive performance measured through standardized tests",
        "results": "Students with 7-9 hours of sleep demonstrated 23% better cognitive performance compared to those with less than 6 hours",
        "conclusion": "Maintaining optimal sleep duration (7-9 hours) is crucial for maximizing cognitive performance in university students",
    },
    {
        "input": """Title: Effects of Mindfulness Meditation on Stress Reduction
        Abstract: This research evaluated the effectiveness of an 8-week mindfulness meditation program on stress reduction.
        The study hypothesized that regular mindfulness practice would decrease cortisol levels and self-reported stress.
        Methodology: 200 participants were randomly assigned to intervention and control groups. 
        The intervention group participated in daily 20-minute guided meditation sessions.
        Results: Participants in the meditation group showed 35% lower cortisol levels and reported 42% less stress.
        Conclusions: Mindfulness meditation is an effective intervention for stress reduction.""",
        "goal": "To evaluate the effectiveness of mindfulness meditation in reducing stress levels",
        "hypothesis": "Regular mindfulness meditation practice will reduce cortisol levels and self-reported stress",
        "methods": "8-week randomized controlled trial with 200 participants divided into meditation and control groups",
        "results": "Meditation group showed 35% lower cortisol levels and 42% reduction in self-reported stress",
        "conclusion": "Regular mindfulness meditation practice effectively reduces both physiological and perceived stress levels",
    },
]

CRITIQUE_EXAMPLES = [
    {
        "input": """Study: Effect of Coffee on Productivity
        Methods: We surveyed 50 office workers about their coffee consumption and productivity.
        Results: Workers who drank coffee reported feeling more productive.""",
        "critique": """Several methodological weaknesses:
        1. Small sample size (50 participants) limits generalizability
        2. Relies solely on self-reported data without objective productivity measures
        3. No control for confounding variables (sleep, workload, time of day)
        4. Lacks proper control group
        5. No standardization of coffee consumption amounts or timing""",
    },
    {
        "input": """Study: Online Learning vs Traditional Classroom
        Methods: Compared test scores between online and in-person students.
        Results: Online students scored 5% higher on average.""",
        "critique": """Critical limitations:
        1. Selection bias - students self-selected into online or in-person classes
        2. No control for student demographics or prior academic performance
        3. Single measurement point doesn't account for long-term learning outcomes
        4. No consideration of different teaching styles or platform effects
        5. Missing data on student engagement and participation rates""",
    },
]

REVIEWER_QUESTIONS_EXAMPLES = [
    {
        "input": """Study on remote work productivity using employee surveys and performance metrics.
        Found 15% increase in productivity but 20% decrease in team collaboration.""",
        "questions": [
            "How was productivity specifically measured and normalized across different job roles?",
            "What controls were in place for home office setups and technical resources?",
            "How did you account for self-reporting bias in the survey responses?",
            "Were there any seasonal or external factors that could have influenced the results?",
            "What specific metrics were used to measure team collaboration?",
        ],
    },
    {
        "input": """Research on new machine learning algorithm for medical diagnosis.
        Claims 95% accuracy on test dataset.""",
        "questions": [
            "How was the test dataset constructed and validated?",
            "What measures were taken to prevent data leakage between training and test sets?",
            "How does the algorithm perform on edge cases and rare conditions?",
            "What is the false positive/negative rate compared to existing methods?",
            "Has the model been tested on diverse patient populations?",
        ],
    },
]
