from pathlib import Path

from draft.configuration.Semantic import Semantic
from draft.configuration.Validator import Validator


class DraftExercisesValidator(Validator):
    """
    Optional, that defaults to a dictionary:

    ```
    {
        "intervals": {
            "count": 1,
            "path": Path(...),
        }
    }
    ```
    """

    def __init__(self):
        self._key = "draft-exercises"
        self._semantic = Semantic.OPTIONAL

    def remove_tex(self, value: str) -> str:
        return value.removesuffix(".tex")

    def exercise_path_appending(self, component: str | Path) -> Path:
        match component:
            case str():
                return (
                    self.configuration.main.parent
                    / ("exercises/" + self.remove_tex(component) + ".tex")
                ).resolve()
            case Path():
                return (
                    self.configuration.main.parent / "exercises/" / component
                ).resolve()

    def lint(self, value) -> dict:
        result = {}

        def exercise_configuration(
            name: str,
            count_YqthQh: int | None = None,  # guarantees unique keys
            path_e5oVVY: Path | None = None,  # in with **kwargs
            **kwargs,
        ) -> dict:
            result = {}
            result.update(**kwargs)

            result["count"] = (
                count_YqthQh if count_YqthQh is not None else kwargs.get("count", 1)
            )

            if "path" in kwargs or path_e5oVVY is not None:
                if Path(kwargs.get("path", path_e5oVVY)).is_absolute():
                    result["path"] = Path(kwargs.get("path", path_e5oVVY))
                else:
                    result["path"] = self.exercise_path_appending(
                        kwargs.get("path", path_e5oVVY)
                    )
            else:
                result["path"] = self.exercise_path_appending(name)

            return result

        def dict_types(dictionary: dict, key, value) -> bool:
            return all(
                isinstance(k, key) and isinstance(v, value)
                for k, v in dictionary.items()
            )

        match value:
            # draft-exercises: intervals
            case str(exercise_name):
                result[exercise_name] = exercise_configuration(exercise_name)

            # draft-exercises:
            case list(items):
                for item in items:
                    match item:
                        # - intervals
                        case str(exercise_name):
                            result[exercise_name] = exercise_configuration(
                                exercise_name
                            )
                        # - intervals: 2
                        case dict(item) if dict_types(item, str, int):
                            for k, v in item.items():
                                result[k] = exercise_configuration(k, v)

                        # - intervals:
                        case dict(item) if dict_types(item, str, dict):
                            for k, v in item.items():
                                result[k] = exercise_configuration(k, **v)

            # draft-exercises:
            case dict(items):
                for k, v in items.items():
                    match v:
                        # 2
                        case int(count):
                            result[k] = exercise_configuration(k, v)

                        # count: 3
                        case dict(config):
                            result[k] = exercise_configuration(k, **config)

        return {self.remove_tex(key): value for key, value in result.items()}

    def validate(self, value) -> bool:
        """
        `value` will be of the type, that the linter produces.

        Needs to validate the path to the exercise.
        The count must be greater than 0.
        """
        invalid_keys = []

        for k, v in value.items():
            # path points to existing file
            if not v["path"].is_file():
                invalid_keys.append(k)

            # count is greater than 0
            if not v["count"] > 0:
                invalid_keys.append(k)

        for k in invalid_keys:
            value.pop(k)

        if self.configuration[self.key] == {}:
            self.configuration.pop(self.key)

        return True
