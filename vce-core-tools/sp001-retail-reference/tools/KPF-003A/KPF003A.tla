----------------------------- MODULE KPF003A -----------------------------
EXTENDS Naturals, TLC

CONSTANT IsolationEnabled
ASSUME IsolationEnabled \in BOOLEAN

VARIABLES phase, hasFD, resourceChanged, authorized
vars == <<phase, hasFD, resourceChanged, authorized>>

Init ==
    /\ phase = "start"
    /\ hasFD = FALSE
    /\ resourceChanged = FALSE
    /\ authorized = FALSE

TryInheritedFD ==
    /\ phase = "start"
    /\ ~hasFD
    /\ phase' = "fd_denied"
    /\ UNCHANGED <<hasFD, resourceChanged, authorized>>

OpenByPath ==
    /\ phase = "fd_denied"
    /\ ~IsolationEnabled
    /\ phase' = "path_opened"
    /\ hasFD' = TRUE
    /\ UNCHANGED <<resourceChanged, authorized>>

DenyPath ==
    /\ phase = "fd_denied"
    /\ IsolationEnabled
    /\ phase' = "path_denied"
    /\ UNCHANGED <<hasFD, resourceChanged, authorized>>

WriteResource ==
    /\ phase = "path_opened"
    /\ hasFD
    /\ phase' = "written"
    /\ resourceChanged' = TRUE
    /\ UNCHANGED <<hasFD, authorized>>

Finish ==
    /\ phase \in {"path_denied", "written"}
    /\ phase' = "done"
    /\ UNCHANGED <<hasFD, resourceChanged, authorized>>

Next == TryInheritedFD \/ OpenByPath \/ DenyPath \/ WriteResource \/ Finish
Spec == Init /\ [][Next]_vars

TypeOK ==
    /\ phase \in {"start", "fd_denied", "path_opened", "path_denied", "written", "done"}
    /\ hasFD \in BOOLEAN
    /\ resourceChanged \in BOOLEAN
    /\ authorized \in BOOLEAN

NoUnauthorizedEffect == ~resourceChanged \/ authorized
NoDirectProtectedFD == ~hasFD
=============================================================================
