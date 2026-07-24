from dataclasses import dataclass, field


@dataclass
class ComparisonItem:
    """
    Represents one formatting comparison.
    """

    name: str

    expected: str

    actual: str

    passed: bool


@dataclass
class ComparisonResult:
    """
    Complete document comparison result.
    """

    items: list[ComparisonItem] = field(
        default_factory=list
    )

    def add(
        self,
        name: str,
        expected,
        actual,
    ):

        self.items.append(

            ComparisonItem(

                name=name,

                expected=str(expected),

                actual=str(actual),

                passed=expected == actual,

            )

        )

    @property
    def passed(self):

        return all(
            item.passed
            for item in self.items
        )

    @property
    def score(self):

        if not self.items:
            return 100.0

        passed = sum(
            item.passed
            for item in self.items
        )

        return round(
            passed / len(self.items) * 100,
            2,
        )

    def print_report(self):

        print()
        print("=" * 70)
        print("DOCUMENT COMPARISON")
        print("=" * 70)

        for item in self.items:

            status = "PASS" if item.passed else "FAIL"

            print(
                f"{status:5}  {item.name}"
            )

            if not item.passed:

                print(
                    f"       Expected : {item.expected}"
                )

                print(
                    f"       Actual   : {item.actual}"
                )

        print()
        print(
            f"Overall Score : {self.score}%"
        )