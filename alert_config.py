import json
from pathlib import Path


CONFIG_PATH = (
    Path(__file__).resolve().parent
    / "config"
    / "alert_config.json"
)


def load_alert_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Alert configuration not found: {CONFIG_PATH}"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    required_sections = {
        "alert_levels",
        "notifications",
        "testing",
    }

    missing = required_sections - config.keys()

    if missing:
        raise ValueError(
            "Missing configuration sections: "
            + ", ".join(sorted(missing))
        )

    return config


if __name__ == "__main__":
    config = load_alert_config()

    print("Alert configuration loaded successfully.")
    print(
        "Configured alert levels:",
        ", ".join(config["alert_levels"].keys())
    )
    print(
        "Slack enabled:",
        config["notifications"]["slack"]
    )
    print(
        "Email enabled:",
        config["notifications"]["email"]
    )