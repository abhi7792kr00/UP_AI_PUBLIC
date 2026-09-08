class ReferenceGenerator:
    """
    Responsible for generating
    the next sequence number.
    """

    def next_sequence(
        self,
        current_sequence: int,
    ) -> int:
        return current_sequence + 1


reference_generator = (
    ReferenceGenerator()
)