# tasks.py

from crewai import Task
from textwrap import dedent

class MarketTasks:
    def create_search_task(self, agent):
        return Task(
            description=dedent(f"""
                Search for the most critical US financial market news from the last 24 hours.
                Your goal is to find a small, curated list of the absolute most important stories.
                Focus on the top 3-5 most impactful developments related to:
                - Major stock market index movements (S&P 500, NASDAQ).
                - Significant economic data releases (e.g., inflation, jobs reports).
                - Federal Reserve policy statements or hints.
                - Major news for market-leading companies.

                Compile the essential facts and URLs from your search. Do not write a summary, just
                gather the raw, vital information needed for the analyst.
            """),
            expected_output=dedent("""
                A bulleted list of the top 3-5 financial news stories from the past 24 hours,
                including key facts and source URLs.
                Example:
                - S&P 500 drops 1.5% on inflation fears. [URL]
                - Federal Reserve hints at future rate hikes. [URL]
            """),
            agent=agent,
            async_execution=False
        )

    def create_summary_task(self, agent):
        return Task(
            description=dedent(f"""
                Analyze the provided financial news data. Your task is to create an extremely
                concise, professional market summary.

                **Your output must follow these strict rules:**
                1.  The entire summary must be **strictly under 250 words**.
                2.  It must be structured with **exactly 4 bullet points**, each covering a key topic
                    (e.g., Market Performance, Economic News, Key Movers, Outlook).
                3.  Be direct and data-driven. Avoid conversational fluff or speculation.
                4.  Do not add any introductory or concluding paragraphs outside of the bullet points.
            """),
            expected_output=dedent("""
                A four-point bulleted list summarizing the day's market activity. The entire text
                must be under 250 words. The summary should be professional, clear, and ready for
                publication.
            """),
            agent=agent,
            async_execution=False
        )

    def create_formatting_task(self, agent):
        return Task(
            description=dedent(f"""
                Format the final market summary for publication. Your only job is to ensure it
                is clean, professional, and ready to be sent.

                **Follow these rules:**
                1.  Use markdown for clear headings and bullet points.
                2.  Add a relevant stock market emoji to the main title.
                3.  Do **not** add any new text, commentary, or change the original summary's content.
                4.  Find one relevant, high-quality image using your search tool that visually
                   represents the overall market trend (e.g., a bull for a positive day, a bear for a negative day).
                   Include the markdown for this image at the end of the summary.
            """),
            expected_output=dedent("""
                The final, formatted market summary in markdown. It must include a title with an emoji,
                the original bullet points, and the markdown link to one relevant image. The text content
                of the summary must not be altered.
            """),
            agent=agent,
            async_execution=False
        )

    def create_translation_task(self, agent, lang):
        return Task(
            description=dedent(f"""
                Translate the provided formatted market summary into **{lang}**.

                **Follow these strict rules:**
                1.  Translate the text accurately, preserving the original financial terminology and meaning.
                2.  Keep the original markdown formatting (headings, bullet points, image links) intact.
                3.  Do **not** add any extra words, phrases, or explanations that were not in the original English text.
                4.  This is a direct translation task. No summarization or alteration is needed.
            """),
            expected_output=dedent(f"""
                The complete text of the market summary, accurately translated into {lang},
                with all original markdown formatting preserved.
            """),
            agent=agent,
            async_execution=False
        )