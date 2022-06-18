from pathlib import Path

from fastapi.templating import Jinja2Templates

TEMPLATE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(TEMPLATE_PATH))

