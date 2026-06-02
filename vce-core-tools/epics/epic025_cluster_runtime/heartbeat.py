import requests
import time


class Heartbeat:

    def monitor(self, peers, rounds=3):

        for i in range(rounds):

            print(f"ROUND {i + 1}")

            for peer in peers:

                try:
                    requests.get(
                        f"{peer}/state",
                        timeout=1
                    )

                    print(peer, "ALIVE")

                except Exception:
                    print(peer, "DEAD")

            print()

            time.sleep(2)
