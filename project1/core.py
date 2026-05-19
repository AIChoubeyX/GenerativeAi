from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatMistralAI(model="mistral-small-2506")

DEFAULT_POINTS_TO_COVER = [
	"Takes a raw paragraph about a movie",
	"Extracts important structured information",
	"Generates a clean summary",
]

movie_review_prompt = ChatPromptTemplate.from_messages([
	(
		"system",
		"""
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie paragraph and present it in a clear format.

Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format
- If information is missing -> write NULL
- Keep summary short (2-3 lines max)
- Do NOT guess unknown facts

Output Format:
Movie Title:
Release Year:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:

Points Covered:
{points_block}
""".strip(),
	),
	(
		"human",
		"""
Movie paragraph:
{raw_movie_paragraph}
""".strip(),
	),
])

movie_review_chain = movie_review_prompt | model | StrOutputParser()


def _build_points_block(points_to_cover):
	return "\n".join(f"{index}. {item}" for index, item in enumerate(points_to_cover, start=1))


def generate_movie_review_output(
	raw_movie_paragraph,
	points_to_cover=None,
):
	if points_to_cover is None:
		points_to_cover = DEFAULT_POINTS_TO_COVER

	return movie_review_chain.invoke({
		"raw_movie_paragraph": raw_movie_paragraph,
		"points_block": _build_points_block(points_to_cover),
	})


if __name__ == "__main__":
	raw_movie_paragraph = (
		"3 Idiots is a celebrated Bollywood drama-comedy directed by Rajkumar Hirani. "
		"Set mainly in an elite engineering college, the story follows three friends: Rancho, "
		"Farhan, and Raju, as they struggle with pressure, fear of failure, and rigid expectations "
		"from society and family. Through humor, emotional turns, and sharp social commentary, "
		"the film questions rote learning and promotes curiosity, creativity, and courage. "
		"Years later, the friends reunite to find Rancho, whose true identity and life choices "
		"reveal the deeper message of pursuing excellence instead of chasing success."
	)

	result = generate_movie_review_output(raw_movie_paragraph)
	print(result)