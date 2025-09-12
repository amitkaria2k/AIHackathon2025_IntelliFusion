# Bosch AI Hackathon 2025 - IntelliFusion AI Document Assistant

## Project Architecture
This is a Streamlit-based AI document assistant designed for Bosch's internal ecosystem. The app integrates with:
- **Bosch LLM Farm**: Internal AI service at `aoai-farm.bosch-temp.com` using `gpt-4o-mini`
- **Bosch Docupedia**: Internal document repository (requires PAT authentication)
- **Document Templates**: Jinja2-based templating system in `templates/document_templates/`

## Development Setup Patterns
1. **Environment Configuration**: Always copy `.env.example` to `.env` first:
   ```bash
   copy .env.example .env  # Windows
   ```
2. **Bosch API Integration**: Use `LLM_FARM_*` variables, not generic OpenAI configs
3. **Authentication**: Prefer `DOCUPEDIA_PAT` over basic auth for Docupedia access

## Project Structure Conventions
- **`src/`**: Main application code (currently empty - scaffold as needed)
  - `src/config.py`: Load environment variables with `python-dotenv`
  - `src/services/`: External API integrations (LLM Farm, Docupedia)
  - `src/modeling/`: AI model inference and training logic
- **`data/`**: Follows ML project structure (raw → interim → processed)
- **`notebooks/`**: Use naming pattern `1.0-xyz-description` (number.version-initials-description)

## Streamlit Configuration
- **Theme**: Bosch blue (`#00629B`) configured in `.streamlit/config.toml`
- **Local dev**: Runs on `127.0.0.1:8501` with minimal toolbar
- **Error handling**: Production mode with `showErrorDetails = false`

## Key Integration Points
- **Database**: Use `DATABASE_URL` from env for document storage
- **File Storage**: Documents saved to `generated_documents/` directory
- **Workflow**: Default approvers configured via `DEFAULT_APPROVERS` env var
- **Headers**: Use `DOCUPEDIA_USER_AGENT = "BoschAI-DocumentAssistant/1.0"` for API calls

## Development Workflow
1. Configure environment variables for Bosch internal services
2. Build Streamlit UI components with Bosch theming
3. Implement document generation with Jinja2 templates
4. Test integration with LLM Farm and Docupedia APIs
5. Follow data science project structure for any ML components
