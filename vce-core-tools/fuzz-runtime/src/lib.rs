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

pub fn replay_fixture_events() -> ReplayState {
    let events = [
        "APPEND_EVIDENCE",
        "REGISTER_ARTIFACT",
        "SEAL_SNAPSHOT",
    ];

    replay_events(&events)
}

#[no_mangle]
pub extern "C" fn replay_sequence_number() -> u32 {
    replay_fixture_events().sequence_number as u32
}

#[no_mangle]
pub extern "C" fn replay_hash_prefix() -> u32 {
    let state = replay_fixture_events();

    let prefix = &state.state_hash[0..8];

    u32::from_str_radix(
        prefix,
        16,
    )
    .unwrap()
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
        let state = replay_fixture_events();

        assert_eq!(state.sequence_number, 3);
    }

    #[test]
    fn exported_replay_sequence_number_returns_three() {
        assert_eq!(replay_sequence_number(), 3);
    }

    #[test]
    fn exported_replay_hash_prefix_is_stable() {
        assert_eq!(
            replay_hash_prefix(),
            replay_hash_prefix(),
        );
    }
}
