from replay_attack_detector import ReplayAttackDetector


detector = ReplayAttackDetector()


event = {
    "lsn": 1,
    "opcode": "APPEND_EVIDENCE",
    "payload": "artifact"
}


print(
    detector.validate(
        event
    )
)


print(
    detector.validate(
        event
    )
)
