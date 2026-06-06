def execute_repair(
    canonical,
    plan,
):
    start = plan["catch_up_from"]

    return canonical[start:]
