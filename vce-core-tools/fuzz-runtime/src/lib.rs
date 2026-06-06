use sha2::{Digest, Sha256};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReplayState {
    pub sequence_number: usize,
    pub state_hash: String,
}

pub fn accept_input(data: &[u8]) -> bool {
    !data.is_empty()
}

pub fn replay_events(events: &[&str]) -> ReplayState {
    let sequence_number = events.len();

    let payload = events.join("|");

    let mut hasher = Sha256::new();
    hasher.update(payload.as_bytes());

    let state_hash = format!("{:x}", hasher.finalize());

    ReplayState {
        sequence_number,
        state_hash,
    }
}

#[no_mangle]
pub extern "C" fn replay_sequence_number() -> u32 {
    let events = [
        "APPEND_EVIDENCE",
        "REGISTER_ARTIFACT",
        "SEAL_SNAPSHOT",
    ];

    replay_events(&events).sequence_number as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn same_events_produce_same_state() {
        let events = [
            "APPEND_EVIDENCE",
            "REGISTER_ARTIFACT",
            "SEAL_SNAPSHOT",
        ];

        let state_a = replay_events(&events);
        let state_b = replay_events(&events);

        assert_eq!(state_a, state_b);
    }

    #[test]
    fn sequence_number_matches_event_count() {
        let events = [
            "APPEND_EVIDENCE",
            "REGISTER_ARTIFACT",
            "SEAL_SNAPSHOT",
        ];

        let state = replay_events(&events);

        assert_eq!(state.sequence_number, 3);
    }

    #[test]
    fn exported_replay_sequence_number_returns_three() {
        assert_eq!(replay_sequence_number(), 3);
    }
}
