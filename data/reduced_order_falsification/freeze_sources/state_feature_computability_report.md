# State Feature Computability Report

## Scope
Feature-only dense replay was used to compute preregistered state variables. No E-model refit, gate addition, threshold tuning, or predictive-accuracy evaluation was performed.

## Variables
- `corner_turn_phase_index_mean`
- `branch_ambiguity_index_mean`
- `relief_consistency_overshoot_availability_index_mean`

## Computability
- Expected cells: 232
- Completed cells: 232
- Completed by dataset: {'heldout1_56': 56, 'heldout2_80': 80, 'original_96': 96}
- All three state variables finite for completed cells: True
- Response horizon frames: 5

## Approximations
- CTPI uses dense current and delayed arclength recovered during replay.
- BAI is exact only as a preregistered approximation to branch ambiguity: for lemniscate, the competing branch is the nearest discrete path sample separated by at least 20% of path circumference in arclength; non-branched trajectories are assigned BAI=0.
- RCOAI uses dense frame sequences after the 120-frame warmup and a fixed horizon `ceil(1 / SMOOTH)` from engine dynamics.

## Missing Fields
- No required dense fields are missing from the replay computation.
- Raw dense frame logs were not written; cell-level state feature summaries were accumulated directly to avoid very large outputs.
