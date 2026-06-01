from epics.epic021_crypto_trust.key_rotation import (
    KeyRotationManager
)


manager = KeyRotationManager()

first = manager.initialize()

second = manager.rotate()


print(
    first != second
)

print(
    manager.retired_count()
)
