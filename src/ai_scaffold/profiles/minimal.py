from .base import Profile, register_profile

MINIMAL_MANIFEST = [
    "common.gitignore",
    "common.pyproject_toml",
    "common.readme",
    "common.claude_md",
    "common.env_example",
    "common.requirements",
    "common.claude_rules_code_style",
    "common.claude_rules_testing",
    "src.main",
]

register_profile(
    Profile(
        name="minimal",
        description="Bare project skeleton: config files, README, and src/ layout",
        manifest=MINIMAL_MANIFEST,
    )
)
