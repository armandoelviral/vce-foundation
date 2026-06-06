#![no_main]

use libfuzzer_sys::fuzz_target;
use vce_fuzz_runtime::accept_input;

fuzz_target!(|data: &[u8]| {
    let _ = accept_input(data);
});
