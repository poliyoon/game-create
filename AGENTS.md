# Repository Guidelines

## Project Structure & Module Organization
The root scripts (`generate_ppt.py`, `generate_ppt_with_images.py`, `generate_ppt_simple.py`, and the REST variant) are single-file entry points that assemble slides from `slides.json`. Supporting assets live alongside them: `.env` stores the Gemini API key, `generated_images/` collects slide artwork, and `available_models.txt` plus `check_genai_attrs.py` help inspect APIs. Test harnesses (`test_api.py`, `test_image_gen.py`, `test_imagen_call.py`, `test_imagen_rest.py`) sit in the root as well; keep new utilities collocated so absolute paths stay shallow. Workflow definitions for the Antigravity agent go under `.agent/workflows/`, and newly created decks land next to the scripts (e.g., `nano_banana_presentation_*.pptx`).

## Build, Test, and Development Commands
Create an isolated toolchain before modifying slides:
```
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python generate_ppt.py                  # build deck from slides.json using inline prompts
python generate_ppt_with_images.py      # richer layout + REST fallbacks
python generate_ppt_with_images_rest.py # bypass SDK and hit the REST endpoint
pytest test_imagen_rest.py -s           # verify REST responses and artifact writes
python test_api.py                      # snapshot available Gemini models to available_models.txt
```

## Coding Style & Naming Conventions
Stick to PEP 8: four-space indentation, snake_case functions (`create_presentation`, `generate_image`), and descriptive module names. Keep slide schema keys (`title`, `content`, `image_prompt`) consistent and document any additions in README.md. Favor small, composable helpers over monolithic functions and always gate API calls behind `get_api_key()` to centralize error handling.

## Testing Guidelines
Tests are integration-heavy and expect a populated `.env`. Run them with `pytest` so results are timestamped, but allow ad-hoc execution (`python test_image_gen.py`) when debugging binary outputs. When adding cases, follow the `test_<capability>.py` naming pattern and clean up generated artifacts (`test_image.png`, `test_rest_image.png`) before committing. Target scenarios that cover JSON parsing, placeholder rendering, and network fallbacks, and document any required credentials in the test docstring.

## Commit & Pull Request Guidelines
Existing history shows short, present-tense summaries ("Update README.md"), so keep titles under 60 characters and describe why in the body. Each PR should explain the slide scenario, list new commands or configuration toggles, attach a representative `.pptx` or screenshot, and link issues or workflow IDs. Block PRs on lint/tests, note any API quotas touched, and call out security-sensitive changes explicitly.

## Security & Configuration Tips
Never commit real `.env` data; ship `.env.example` updates instead. Rotate API keys after demos, and prefer `os.environ.get("API_KEY")` overrides for CI. Store generated decks outside version control unless they demonstrate a bug, and scrub prompts that might include confidential client topics.
