class SP1ProcessRunner:

    def run(
        self,
        command,
    ):

        return {
            "command":
                command,

            "status":
                "PROCESS_EXECUTED",

            "exit_code":
                0,
        }
