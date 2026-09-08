class ReferenceFormatter:
    """
    Responsible for formatting
    business reference numbers.
    """

    def format(
        self,
        prefix: str,
        separator: str,
        period_value: str,
        sequence: int,
        sequence_length: int,
    ) -> str:

        formatted_sequence = (
            str(sequence)
            .zfill(sequence_length)
        )

        return (
            f"{prefix}"
            f"{separator}"
            f"{period_value}"
            f"{separator}"
            f"{formatted_sequence}"
        )


reference_formatter = (
    ReferenceFormatter()
)