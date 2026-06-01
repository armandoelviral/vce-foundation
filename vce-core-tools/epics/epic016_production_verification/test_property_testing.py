from epics.epic016_production_verification.property_testing import (
    PropertyTesting
)


tester = PropertyTesting()


result = tester.run(
    iterations=10000
)


print(
    result["iterations"]
)


print(
    result["passed"]
)
