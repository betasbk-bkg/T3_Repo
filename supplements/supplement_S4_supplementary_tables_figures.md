# Supplementary Information S4. Supplementary Tables and Figures

This file contains the supplementary tables and figures referenced in the main text. Table and figure numbering follows first mention in the main text.

Supplementary Table S1. System-class assumptions

  -----------------------------------------------------------------------
  ID     Assumption
  ------ ----------------------------------------------------------------
  S1     planar discrete-time tracking state with first-order smoothing
         memory

  S2     finite directional quantizer on the aggregate command channel

  S3     delayed look-ahead target defined on a reference path

  S4     local projection coordinates available only on smooth
         single-branch path intervals

  S5     non-smooth path changes, projection ambiguity, and quantizer
         crossings treated as mode/event structure

  S6     public aggregate heading available as an auditable
         collective-direction variable
  -----------------------------------------------------------------------

Supplementary Table S2. Audit-protocol conditions

  -----------------------------------------------------------------------
  ID     Protocol condition
  ------ ----------------------------------------------------------------
  P1     event channels for quantizer switching and path-mode changes are
         explicitly logged or reproducibly reconstructed

  P2     intervention policy and implementation are fixed during audit

  P3     no threshold tuning, controller refit, or model refit is
         performed in the audit stage

  P4     stream-separated common-random-number convention is used for the
         final structural audit

  P5     uncertainty for event-cost associations is clustered by base
         condition
  -----------------------------------------------------------------------

Supplementary Table S3. Smooth-theorem implementation scope

  ------------------------------------------------------------------------------------
  Trajectory regime Projection model  Theorem relationship           Manuscript
                                                                     treatment
  ----------------- ----------------- ------------------------------ -----------------
  circle            continuous smooth direct smooth-chart scope away main local lemma
                    path              from numerical degeneracy      applies under
                                                                     tube assumptions

  square segment    straight segment, direct local straight-chart    true corners
  interior          K=0               scope away from true corners   charged
                                                                     separately

  zigzag segment    straight segment, direct local straight-chart    endpoint wrap
  interior          K=0               scope away from vertices and   excluded from
                                      endpoint wrap                  theorem

  sampled           nearest among 800 discrete projection            lemniscate replay
  lemniscate        sampled path      implementation outside direct  relief is an
                    points            C2 theorem scope without       audit proxy;
                                      interpolation/discretization   branch and
                                      remainder                      sampling
                                                                     discontinuities
                                                                     are obstructions
  ------------------------------------------------------------------------------------

Supplementary Table S4. Formal-claim scope summary

  -----------------------------------------------------------------------
  Item                    Status                  Main-text role
  ----------------------- ----------------------- -----------------------
  Smooth local normal     Proved under            Main positive lemma
  drift                   assumptions             

  Strict same-side local  Proved under            Main positive local
  relief                  assumptions             proposition

  Quantizer               Structural remark       General systems warning
  frequency-burden                                
  geometry                                        

  Square true-corner      Conditional geometric   Non-smooth partial
  charge                  charge with             component
                          arclength-window        
                          correction              

  Zigzag interior memory  Conditional local       Partial result
                          accounting              

  Zigzag endpoint wrap    Obstruction only        Scope boundary

  Lemniscate branch       Obstruction only        Scope boundary
  ambiguity                                       

  Finite-horizon global   Closure target schema   Open master-inequality
  benefit expression      only                    target
  -----------------------------------------------------------------------

Supplementary Table S5. Pairwise q contrasts

  ----------------------------------------------------------------------------
  Metric           Contrast       Mean           95% CI low     95% CI high
  ---------------- -------------- -------------- -------------- --------------
  mean vote-jump   q4_minus_q8    -0.019782      -0.104528      0.067016
  chord2 per vote                                               
  opportunity                                                   

  mean vote-jump   q8_minus_q16   0.239790       0.150200       0.328106
  chord2 per vote                                               
  opportunity                                                   

  mean vote-jump   q4_minus_q16   0.220008       0.136213       0.310490
  chord2 per vote                                               
  opportunity                                                   

  aggregate jump   q4_minus_q8    -0.376146      -0.518396      -0.239405
  chord2                                                        

  aggregate jump   q8_minus_q16   0.449022       0.338951       0.565471
  chord2                                                        

  aggregate jump   q4_minus_q16   0.072876       -0.034596      0.187033
  chord2                                                        

  path/vote        q4_minus_q8    -0.013438      -0.027656      0.001875
  co-occurrence                                                 

  path/vote        q8_minus_q16   0.013281       -0.000158      0.026486
  co-occurrence                                                 

  path/vote        q4_minus_q16   -0.000156      -0.014063      0.015547
  co-occurrence                                                 

  positive         q4_minus_q8    0.199923       0.158428       0.240543
  intervention                                                  
  error-squared                                                 
  increment                                                     

  positive         q8_minus_q16   0.052101       0.033046       0.072338
  intervention                                                  
  error-squared                                                 
  increment                                                     

  positive         q4_minus_q16   0.252024       0.204328       0.299219
  intervention                                                  
  error-squared                                                 
  increment                                                     

  mean             q4_minus_q8    -0.002747      -0.012279      0.005658
  counterfactual                                                
  event cost                                                    

  mean             q8_minus_q16   -0.002376      -0.008986      0.004146
  counterfactual                                                
  event cost                                                    

  mean             q4_minus_q16   -0.005123      -0.013255      0.002317
  counterfactual                                                
  event cost                                                    

  mean             q4_minus_q8    0.223549       0.170728       0.273471
  positive-part                                                 
  counterfactual                                                
  cost                                                          

  mean             q8_minus_q16   0.092685       0.054599       0.127317
  positive-part                                                 
  counterfactual                                                
  cost                                                          

  mean             q4_minus_q16   0.316234       0.256488       0.372893
  positive-part                                                 
  counterfactual                                                
  cost                                                          
  ----------------------------------------------------------------------------

Supplementary Table S6. Linear q-coarseness model, base-condition clustered

  --------------------------------------------------------------------------
  Term           Estimate       95% CI low     95% CI high    Excludes zero
  -------------- -------------- -------------- -------------- --------------
  q coarseness   1.789337       1.020660       2.582424       yes

  vote event     0.002244       -0.202844      0.202911       no

  path event     0.142235       -0.351617      0.657303       no

  q x vote       -4.336568      -5.492429      -3.263838      yes

  q x path       0.962349       -0.691075      2.733094       no

  vote x path    -0.443359      -0.813922      -0.089269      yes
  --------------------------------------------------------------------------

Supplementary Table S7. Categorical q sensitivity, q4 reference

  --------------------------------------------------------------------------
  Term           Estimate       95% CI low     95% CI high    Excludes zero
  -------------- -------------- -------------- -------------- --------------
  q8 main        -0.195697      -0.314585      -0.069048      yes

  q16 main       -0.374058      -0.560244      -0.199693      yes

  q8 x vote      0.637621       0.460248       0.831936       yes

  q16 x vote     0.844274       0.622648       1.077204       yes

  q8 x path      -0.321846      -0.570069      -0.087848      yes

  q16 x path     -0.142409      -0.476031      0.158096       no

  vote x path    -0.420342      -0.767045      -0.097278      yes
  --------------------------------------------------------------------------

Supplementary Table S8. System parameters

  -----------------------------------------------------------------------
  Quantity                Value or definition     Role
  ----------------------- ----------------------- -----------------------
  N_AGENTS                50                      Number of voting agents

  DT                      1/60                    Simulation step

  DUR / final audit       65.0 s in original      Run length convention
  FRAMES                  engine; 1800 frames in  
                          final structural audit  

  WIN / VOTE_INT          0.3 s / 18 frames       Vote update period

  MSPD                    5.0                     Target speed in
                                                  smoothing update

  SMOOTH alpha            0.2                     First-order velocity
                                                  smoothing

  LOOK                    2.0 arclength units     Delayed look-ahead
                                                  distance

  COHERENCE               1.0                     All minority-policy
                                                  votes committed to
                                                  anti-aggregate
                                                  direction

  baseline quantizer      q = 8                   Original fixed
                                                  implementation

  structural quantizers   q = 4, 8, 16            Mechanism
                                                  discrimination only;
                                                  fixed settings

  original-grid           circle, square, zigzag, Path set used in the
  trajectories            lemniscate              original 96-cell grid
                                                  (Table 1)

  original-grid minority  tr = 0.20, 0.30, 0.40   Design axis for the
  fractions                                       original 96-cell grid
                                                  only

  original-grid delays    d = 0, 8, 18, 26, 34,   Design axis for the
                          44, 56, 68 frames       original 96-cell grid
                                                  only

  original-grid           MC = 50                 Repeated random
  replicates                                      schedules per
                                                  original-grid cell

  original-grid total     4 x 3 x 8 = 96          4 trajectories x 3
  cells                                           minority fractions x 8
                                                  delays
  -----------------------------------------------------------------------

Supplementary Table S9. Agent composition

  -----------------------------------------------------------------------
  minority    active      sluggish    other       minority    total
  fraction    honest      honest      honest                  
  ----------- ----------- ----------- ----------- ----------- -----------
  0.25        28          8           2           12          50

  0.35        24          7           1           18          50
  -----------------------------------------------------------------------

Supplementary Table S10. Vote-generation rules

  --------------------------------------------------------------------------
  Agent class             Vote rule
  ----------------------- --------------------------------------------------
  active honest           intended angle + U\[-3 deg, 3 deg\]

  sluggish honest         previous intended angle + wrapped intended-angle
                          difference x (1 - U\[0.2, 0.5\])

  other honest            intended angle + U\[-30 deg, 30 deg\]

  honest-counterfactual   intended angle + U\[-3 deg, 3 deg\] from a
  minority                separate minority stream in the final audit

  intervention minority   nearest quantized bin opposite the delayed
                          public-consensus direction
  --------------------------------------------------------------------------

Supplementary Table S11. Path definitions

  ------------------------------------------------------------------------
  Path         Definition used by implementation
  ------------ -----------------------------------------------------------
  circle       radius 10; projection by radial closest point; at(s) =
               10\[cos(s/10), sin(s/10)\]

  square       vertices (10,0),(10,10),(-10,10),(-10,-10),(10,-10),(10,0);
               true corners s=10,30,50,70; seam at s=0 and s=80 excluded

  zigzag       open projection polyline through
               (0,0),(5,5),(10,0),\...,(50,0); at(s) uses modulo arclength

  lemniscate   800-point Bernoulli-type sampled path: x=7 cos(t)/(1+sin\^2
               t), y=7 sin(t)cos(t)/(1+sin\^2 t); closest point by nearest
               sample, discrete nearest-sample projection
  ------------------------------------------------------------------------

Supplementary Table S12. Event definitions

  -----------------------------------------------------------------------
  Event              Detector
  ------------------ ----------------------------------------------------
  square true-corner closest arclength within r_arc = 0.5 of s = 10, 30,
  event              50, or 70

  zigzag path event  closest arclength within r = 0.5 of an interior
                     zigzag vertex

  zigzag endpoint    delayed_arclength \>= path_circumference - LOOK
  wrap               

  lemniscate branch  d2 - d1 \<= 0.75, arc separation \>= 5.0, and
  event              tangent disagreement \>= 0.25

  vote event         any per-agent vote-bin switch or aggregate
                     quantization-cell switch since previous vote

  vote/path          vote event and path event in the same vote window
  coincidence        
  -----------------------------------------------------------------------

Supplementary Table S13. Quantization and aggregation conventions

  -----------------------------------------------------------------------
  Operation      Definition
  -------------- --------------------------------------------------------
  vote           nearest representative among q equally spaced unit
  quantization   directions

  vote-bin tie   first minimum returned by argmin
  rule           

  aggregate      mean of voted direction representatives
  command        

  zero aggregate reuse previous command direction as fallback
  norm           

  aggregate cell floor((heading + pi/q)/(2pi/q)) mod q
  -----------------------------------------------------------------------

Supplementary Table S14. Final structural-audit design

  -----------------------------------------------------------------------
  Component               Values                  Purpose
  ----------------------- ----------------------- -----------------------
  trajectories            circle, square, zigzag, Smooth, corner,
                          lemniscate              endpoint-wrap, and
                                                  branch regimes

  minority fractions      0.25, 0.35              Two fixed shares for
                                                  final audit

  delays                  12, 34 frames           Two fixed delay levels
                                                  for final audit

  replicates              MC = 8                  Repeated random
                                                  schedules per base
                                                  condition

  quantizer directions    4, 8, 16                Resolution
                                                  discrimination

  base conditions         4 trajectories x 2      Shared-noise cluster
                          fractions x 2 delays x  unit
                          8 reps = 128            

  mode simulations        intervention and honest 384 paired condition
                          counterfactual at each  rows; 768 simulations
                          q                       

  event rows              38,400 intervention     Vote/path event
                          vote-event rows         analysis
  -----------------------------------------------------------------------

Supplementary Table S15. Dataset lineage and analysis roles

  -------------------------------------------------------------------------------------------------------------------
  Dataset          Purpose            Fitted?            Held out?    Used for final        Role
                                                                      inference?            
  ---------------- ------------------ ------------------ ------------ --------------------- -------------------------
  Original 96-cell Initial            yes, for           no           no final inference;   exploratory/development
  grid             benefit/harm map   descriptive                     motivates obstruction 
                   and reduced-order  reduced-order                   analysis              
                   model fitting      models                                                

  Heldout3 96-cell Frozen             no refit           held out     no final structural   frozen diagnostic
  grid             low-dimensional                       from the     inference; used to    
                   closure stress                        frozen       falsify compact       
                   test                                  correction   closure               

  Proof-oriented   Audit theorem      no                 diagnostic   proof-observability   audit
  replay logs      terms such as                         replay       audit only            
                   local relief, tail                    source                             
                   bridge, and switch                                                       
                   bounds                                                                   

  Final structural q/vote/path        no                 separate     primary               base-condition clustered
  audit            event-cost         controller/model   fixed audit  event-association     
                   analysis with      tuning             grid         inference             
                   stream-separated                                                         
                   common random                                                            
                   numbers                                                                  
  -------------------------------------------------------------------------------------------------------------------

Supplementary Table S16. Proof-oriented audit and provenance

  -------------------------------------------------------------------------
  Audit item        Replay status     Use                 Boundary
  ----------------- ----------------- ------------------- -----------------
  strict local      observed and      lower-bound local   overlapping
  smooth relief     summed in replay  theorem component   horizons and
                    audit                                 replay states
                                                          preclude use as a
                                                          global relief
                                                          constant

  local tail bridge locally           projection-tube     global use
                    instantiable in   diagnostic          requires
                    replay audit                          consistent
                                                          interval
                                                          accounting

  switch-frame jump observable with   scale and           observed counts
  quantities        universal and     observability check are audit
                    aggregate                             quantities only
                    variants                              

  fixed-cell        open              needed for master   open term
  divergence                          inequality          

  stochastic        open              needed for          open term
  coupling                            expectation-level   
                                      theorem             

  neutral           open              needed for strict   open term
  strictness margin                   finite-horizon      
  and gamma lower                     closure             
  bound                                                   
  -------------------------------------------------------------------------

![](./media/image5.png){width="6.3in" height="2.1261745406824146in"}

Supplementary Fig. S1. Non-smooth regimes are separated rather than forced into the
smooth theorem: square true-corner reset, zigzag interior memory plus
endpoint wrap, and lemniscate branch-ambiguity obstruction.

![](./media/image7.png){width="6.0in" height="3.3933333333333335in"}

Supplementary Fig. S2. Categorical q sensitivity for the mean counterfactual
event-cost outcome. The sensitivity analysis is used to prevent
overinterpretation of a single linear q-coarseness coefficient.

![](./media/image1.png){width="6.3in" height="3.241686351706037in"}

Supplementary Fig. S3. Fixed simulation and instrumentation flow. The figure shows
the quantities specified in Tables 1-7 and the data flow used in the
structural audit.
