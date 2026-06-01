class ByzantineQuorum:

    def fault_tolerance(
        self,
        validators
    ):

        return (
            (
                validators
                -
                1
            )
            //
            3
        )


    def validate(
        self,
        total_validators,
        approvals
    ):

        tolerated = self.fault_tolerance(
            total_validators
        )


        required = (
            2
            *
            tolerated
            +
            1
        )


        return {
            "consensus":
                approvals >= required,

            "validators":
                total_validators,

            "faults_tolerated":
                tolerated,

            "required_votes":
                required
        }
