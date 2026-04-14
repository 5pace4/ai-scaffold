from dataclasses import dataclass, field

PROFILE_REGISTRY: dict[str, "Profile"] = {}


@dataclass
class Profile:
    name: str
    description: str
    manifest: list[str]
    extra_deps: list[str] = field(default_factory=list)


def register_profile(profile: Profile) -> Profile:
    PROFILE_REGISTRY[profile.name] = profile
    return profile
