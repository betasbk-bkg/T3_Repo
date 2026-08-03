# Heldout3 Error Forensics

## Residual Class Counts
- high-delay corner/tail: 1
- lemniscate branch/topology: 2
- low-delay corner-onset: 2
- low-delay no-overshoot: 2
- near-neutral/uncertain boundary: 7

## Error Cells
### circle tr=0.225 delay=1
- error type: false_benefit
- residual class: low-delay no-overshoot
- observed_gap: -0.071064
- gap_hat_E_locked: 0.115210
- gap_hat_A: 0.114517
- CI: [-0.073962, -0.068166], includes zero: False
- RCOAI: 0.177613, CTPI: 0.002422
- relief/cost: frame_energy=0.589522, frame_abs=0.407624, cost_index=0.867629, tail_delta=0.103889

### circle tr=0.225 delay=5
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.021558
- gap_hat_E_locked: 0.041673
- gap_hat_A: 0.043388
- CI: [-0.026910, -0.016207], includes zero: False
- RCOAI: 0.554104, CTPI: 0.011786
- relief/cost: frame_energy=0.933983, frame_abs=0.812720, cost_index=0.236069, tail_delta=0.014487

### circle tr=0.225 delay=52
- error type: false_harm
- residual class: near-neutral/uncertain boundary
- observed_gap: 0.000150
- gap_hat_E_locked: -0.046839
- gap_hat_A: -0.044825
- CI: [-0.057991, 0.058290], includes zero: True
- RCOAI: 0.601033, CTPI: 0.101262
- relief/cost: frame_energy=0.979787, frame_abs=0.921324, cost_index=0.518079, tail_delta=0.018725

### circle tr=0.325 delay=1
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.023131
- gap_hat_E_locked: 0.137333
- gap_hat_A: 0.135961
- CI: [-0.026729, -0.019534], includes zero: False
- RCOAI: 0.071423, CTPI: 0.002247
- relief/cost: frame_energy=0.423820, frame_abs=0.292158, cost_index=1.012237, tail_delta=0.035048

### circle tr=0.325 delay=5
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.014716
- gap_hat_E_locked: 0.171305
- gap_hat_A: 0.170070
- CI: [-0.020983, -0.008448], includes zero: False
- RCOAI: 0.092900, CTPI: 0.011504
- relief/cost: frame_energy=0.487432, frame_abs=0.332130, cost_index=0.577224, tail_delta=0.025820

### circle tr=0.325 delay=52
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.002681
- gap_hat_E_locked: 0.090561
- gap_hat_A: 0.089836
- CI: [-0.044846, 0.039484], includes zero: True
- RCOAI: 0.172704, CTPI: 0.098000
- relief/cost: frame_energy=0.396623, frame_abs=0.286866, cost_index=0.705743, tail_delta=0.017265

### circle tr=0.425 delay=1
- error type: false_benefit
- residual class: low-delay no-overshoot
- observed_gap: -0.045286
- gap_hat_E_locked: 0.022716
- gap_hat_A: 0.021853
- CI: [-0.048064, -0.042508], includes zero: False
- RCOAI: 0.150927, CTPI: 0.001717
- relief/cost: frame_energy=0.536965, frame_abs=0.390173, cost_index=2.284368, tail_delta=0.078704

### lemniscate tr=0.225 delay=1
- error type: false_benefit
- residual class: lemniscate branch/topology
- observed_gap: -0.072336
- gap_hat_E_locked: 0.154572
- gap_hat_A: 0.153104
- CI: [-0.075358, -0.069313], includes zero: False
- RCOAI: 0.056498, CTPI: 0.009026
- relief/cost: frame_energy=0.129401, frame_abs=0.047657, cost_index=1.750100, tail_delta=0.110344

### lemniscate tr=0.225 delay=16
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.074417
- gap_hat_E_locked: 0.046588
- gap_hat_A: 0.047694
- CI: [-0.153844, 0.005009], includes zero: True
- RCOAI: 0.459053, CTPI: 0.115681
- relief/cost: frame_energy=0.991005, frame_abs=0.972324, cost_index=4.098957, tail_delta=0.133233

### lemniscate tr=0.325 delay=1
- error type: false_benefit
- residual class: lemniscate branch/topology
- observed_gap: -0.082078
- gap_hat_E_locked: 0.112757
- gap_hat_A: 0.110733
- CI: [-0.087803, -0.076353], includes zero: False
- RCOAI: -0.030485, CTPI: 0.007204
- relief/cost: frame_energy=0.083939, frame_abs=0.062975, cost_index=2.093958, tail_delta=0.142328

### square tr=0.325 delay=1
- error type: false_harm
- residual class: low-delay corner-onset
- observed_gap: 0.055358
- gap_hat_E_locked: -0.020034
- gap_hat_A: -0.028210
- CI: [0.045576, 0.065140], includes zero: False
- RCOAI: -0.992603, CTPI: 0.023004
- relief/cost: frame_energy=-0.095920, frame_abs=-0.081253, cost_index=1.751326, tail_delta=0.019635

### square tr=0.425 delay=5
- error type: false_harm
- residual class: low-delay corner-onset
- observed_gap: 0.128460
- gap_hat_E_locked: -0.059833
- gap_hat_A: -0.060532
- CI: [0.118838, 0.138082], includes zero: False
- RCOAI: 0.176663, CTPI: 0.065939
- relief/cost: frame_energy=0.510453, frame_abs=0.356185, cost_index=2.274383, tail_delta=-0.017058

### zigzag tr=0.225 delay=66
- error type: false_benefit
- residual class: high-delay corner/tail
- observed_gap: -0.097556
- gap_hat_E_locked: 0.073014
- gap_hat_A: 0.074542
- CI: [-0.136891, -0.058221], includes zero: False
- RCOAI: 0.525081, CTPI: 4.453902
- relief/cost: frame_energy=0.795293, frame_abs=0.689233, cost_index=0.151624, tail_delta=0.028376

### zigzag tr=0.325 delay=66
- error type: false_benefit
- residual class: near-neutral/uncertain boundary
- observed_gap: -0.040573
- gap_hat_E_locked: 0.172778
- gap_hat_A: 0.173014
- CI: [-0.069135, -0.012011], includes zero: False
- RCOAI: 0.322960, CTPI: 5.293246
- relief/cost: frame_energy=0.492823, frame_abs=0.378547, cost_index=-0.050061, tail_delta=0.015894

