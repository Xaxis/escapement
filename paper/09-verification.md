# How each claim was checked

A design paper can make any claim it likes about its own mechanisms. This one tried to break its
claims at six levels, and cut or downgraded whatever failed one. Every level was run by the author
with the author's own tools. The searchers, the red team, the editorial desks and the fresh
reviewer were separate instances of an AI model (Claude), each given only what its level needed and
none given the author's case for a claim. That makes them independent of one another and of the
drafting, not independent in the sense an outside referee is, and nothing here substitutes for one.
Their reports are published as supplementary material [@escapement-redteam;
@escapement-verification].

**Novelty.** Two searchers that had not come up with the ideas searched independently for each
claim, reading only the claims, and were told that finding prior art was success. One covered the
record, the bound, promises, training, adoption and neutrality across economics, forecasting,
AI-agent standards, crypto designs and AI-governance writing; the other covered the Bitcoin
mechanisms across improvement proposals, developer lists, vault and channel designs, Ethereum delay
modules, decentralised identifiers, patents and hardware-governance reports. Both stated what they
did not search.

**Formal.** Each mechanism is stated precisely in the formal statements [@escapement-formal], with
its key property proved or derived and the conditions under which it fails; the propositions this
paper cites by number are there.

**Working.** The Bitcoin pieces (bond, tick chain with halt and renew, chain proof, lease,
co-signing, anchoring, a TRUC veto and the Merkle-sum tree) were built on regtest against Bitcoin
Core 32.1 in [104 checks](../research/numbers.md#lab-checks), which a single command reruns from a fresh node
[@escapement-lab], and two further checks reproduce the fresh reviewer's breaks. The dynamics
(record faking, correlated claims, training, adoption, veto censorship) were simulated with fixed
seeds, and every result enters the paper through the same ledger as every other number.

**Adversarial.** A red team tried only to break the claims, from five positions: a misaligned AI, a
colluding lab, a hostile state, a hashrate majority and an actor that simply routes around the
record. It returned [36 findings](../research/numbers.md#redteam-findings) and concluded that no claim survived as first
stated.

**Paper review.** Paperwright, a writing tool, ran three desks on the draft. The integrity desk
checked each cited claim against its source and filed [30 notes](../research/numbers.md#desk-notes-integrity),
[5 notes](../research/numbers.md#desk-notes-integrity-important) of them marked important; the reviewer desk read the
paper as a referee, filed [73 notes](../research/numbers.md#desk-notes-reviewer) and recommended major revision; the
editor desk filed [61 notes](../research/numbers.md#desk-notes-editor). Of the rewordings offered,
[55 suggestions](../research/numbers.md#desk-suggestions-accepted) were accepted as written. The integrity desk found five
misattributions, one unsupported citation and ten overstatements, all corrected, and that the draft
still credited itself with the lease, which its own sources showed to be prior work. The reviewer's main concerns were that the record's value over
a witnessed transparency log was not shown, that H0 was stronger than stated, that standing
measures capability rather than alignment, and that the training claim contradicted itself; each is
answered in sections 4, 5 and 7, or recorded as a limit in section 12.

**Fresh eyes.** A last reviewer that had seen none of the work read the claims, the proofs, the
paper, the model and the lab, reran the lab (all [104 checks](../research/numbers.md#lab-checks) pass) and the ledger numbers
it checked (all match), and built two regtest checks of its own. It found every claim prior work, or
extending prior work at most narrowly, two claims that did not work as stated, and sentences that
said more than the evidence. Every finding that could be checked was reproduced before anything was
changed.

@tab:verification gives the result for each contribution.

Table: Each contribution's result at each level of verification, and the final verdict. {#tab:verification}

| Contribution | Searches | Formal | Working | Red team | Fresh eyes | Final |
|---|---|---|---|---|---|---|
| One record as standing, reward and release gate | Partial, close | Props 3, 4 | Built; light verifier misses newest entries | Narrowed | Does not work: chain not bound to bond; bets versus forecasts | Cut |
| Fake-record bound under costly identity | Partial, close | Theorem 1, conditional | Product rule broken; round rule within bound | Broken, repaired | Prior work; hypothesis mis-stated; not proper | Prior work, conditions restated |
| Training reward neither party can select | Partial | Props 9, 10, 10b (none on the lab) | Learner calibrates | Manipulation outside exogenous events | Does not work for the lab | Cut |
| Two-sided adoption with seed readers | Partial | Prop 12 | Tipping point reproduced | Conditions added | Prior work (critical mass) | Prior work, a toy model |
| Routing around becomes costly | Prior, partial | Prop 13, readers only | False once corrected | Fatal | (cut before) | Cut |
| Tick chain | Partial; parts prior | Props 1 to 5 | Built; three first claims broken and fixed | Light proof fatal | Pin unbound; outside-money bid | Extends prior work narrowly, per pinned chain |
| Height-difference lease | Partial, close | Prop 6 | Held as stated | Stated limits | Prior work (Substrate) | Prior work |
| Cost of running the clock fast | Partial | Arithmetic | Model numbers | Below a majority only | Prior work; not load-bearing | Prior work |
| Blockspace as an aggregate limit | Not found | Arithmetic | Measured release size | Weak | Prior method; a ceiling on the design | An observation |
| Headers as a chip's licence clock | Partial | None | Not built | Fatal | (cut before) | Cut |

## What broke

Nine results changed the paper, and they are its main contribution.

- **Claims that move together.** Multiplying every claim's likelihood ratio let correlated claims
  fake a record, succeeding [99.8%](../research/numbers.md#sim-corr-product-p) of the time against a bound of
  [1.6%](../research/numbers.md#sim-corr-bound), and gave a score of about [23,000](../research/numbers.md#tail-product-score) to a record that
  one rare event would wipe out. Scoring rounds by the mean of their ratios repairs the bound
  (section 4).
- **The repair is not proper.** With more than one claim a round the round rule rewards reports near
  certainty over the truth, so standing scored that way rewards bets, and one record cannot serve as
  both standing and a calibrated training signal.
- **Edge is not alignment.** A record of forecasting edge measures capability and routes trust to the
  most capable agents, whatever their goals.
- **Manipulation.** A training reward on events the agent can move pays it to move them, while its
  reports stay calibrated (section 5).
- **The lab still selects.** Committing a reward definition binds a report, not a computation.
- **A line of code.** The adoption simulation had barred harmful actors from joining; corrected, they
  cycled through fresh identities at a profit, so the claim that routing around becomes costly is
  withdrawn (section 6).
- **Proofs without witnesses.** A two-transaction proof of a release, built on transaction-id
  proofs, accepted a Tier 3 release no guardian signed and the agent's own copy of a vetoed entry,
  so releases are now proved over the whole chain with witness proofs (section 8).
- **An unbound pin.** Nothing on chain ties a tick chain to its bond, so one charter carried two
  chains with different histories.
- **Outside money.** At a veto's edge the agent outbid the watchtower with money from outside the
  chain.
