from pathlib import Path
from random import choices, randint

import yaml


def main() -> None:
    schedule = generate_schedule()
    update_schedule(sorted(schedule))


def generate_schedule() -> list[tuple[int, int]]:
    num = choices([5, 6, 7, 8], weights=[2, 5, 5, 1])[0]
    return [(randint(8, 23), randint(0, 59)) for _ in range(num)]


def update_schedule(schedule: list[tuple[int, int]]) -> None:
    path = Path(__file__).parent.parent / ".github" / "workflows" / "post.yml"
    with path.open("r") as f:
        doc = yaml.safe_load(f)
    doc["on"]["schedule"] = [
        {"cron": f"{minute} {(hour + 15) % 24} * * *"} for hour, minute in schedule
    ]
    with path.open("w") as f:
        yaml.dump(doc, f, sort_keys=False, indent=2)


if __name__ == "__main__":
    main()
