from .base import Profile, register_profile

MINIMAL_MANIFEST = [
    "common.gitignore",
    "common.pyproject_toml",
    "common.readme",
    "common.claude_md",
    "app.main",
    "app.config",
    "app.models",
]

register_profile(
    Profile(
        name="minimal",
        description="Bare FastAPI app with config, models, and env setup",
        manifest=MINIMAL_MANIFEST,
    )
)
