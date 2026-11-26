# How each claim was checked

A design paper can make any claim it likes about its own mechanisms. This one tried to break its
claims before stating them, at six levels, and cut or narrowed whatever failed one.

**Novelty.** Two helpers that had not come up with the ideas searched independently for each claim,
reading only the claims, and were told that finding prior art was success. One covered the record,
the bound, promises, training, adoption and neutrality across economics, forecasting, AI-agent
standards, crypto designs and AI-governance writing; the other covered the Bitcoin mechanisms across
improvement proposals, developer lists, vault and channel designs, Ethereum delay modules,
decentralised identifiers, patents and hardware-governance reports. Both stated what they did not
search.

**Formal.** Each mechanism is stated precisely in the formal appendix, with its key property proved
or derived and the conditions under which it fails.

**Working.** The Bitcoin pieces (bond, tick chain with halt and renew, chain proof, lease,
co-signing, anchoring, a TRUC veto and the Merkle-sum tree) were built on regtest against Bitcoin
Core 32.1 in [104 checks](../research/numbers.md#lab-checks), which a single command reruns from a
fresh node [@escapement-lab]. The dynamics (record faking, correlated claims, training, adoption,
veto censorship) were simulated with fixed seeds, and every result enters the paper through the same
ledger as every other number.

**Adversarial.** A red team tried only to break the claims, from five positions: a misaligned AI, a
colluding lab, a hostile state, a hashrate majority and plain economic routing around. It returned
35 findings and concluded that no claim survived as first stated.

**Paper review and fresh eyes.** Paperwright's integrity, reviewer and editor desks reviewed the
paper, and a last reviewer that had seen none of the work judged whether each claim called new is
new and works.

Table @tab:verification gives the result for each contribution.

Table: Each contribution's verdict on novelty and its result at each level of verification. {#tab:verification}

| Contribution | Verdict | Formal | Working | Red team | Outcome |
|---|---|---|---|---|---|
| One complete record as standing, reward and release gate | Extends prior work | Proved (Props 3, 4) | Built; light verifier misses newest entries | Narrowed | Kept, narrowed |
| Fake-record bound under costly identity | Extends prior work | Proved under H0 (Theorem 1) | Product rule broken; round rule within bound | Broken, repaired, conditional | Kept as a conditional theorem |
| Training reward neither party can select | Extends prior work | Proved (Props 9, 10, 10b) | Learner calibrates; manipulation untested | Manipulation fatal outside exogenous events | Kept for exogenous events |
| Two-sided adoption with seed readers | Extends prior work | Derived (Prop 12) | Tipping point and seeding reproduced | Conditions added | Kept, conditional |
| Routing around becomes costly | Prior economics | About readers only (Prop 13) | False in corrected simulation | Fatal | Cut |
| Tick chain | Extends prior work | Proved (Props 1 to 5) | Built; three first claims broken and fixed | Light proof fatal; veto final only at depth | Kept, narrowed |
| Height-difference lease | Extends prior work | Proved (Prop 6) | Built; held as stated | Stated limits | Kept |
| A clock an AI cannot speed up | Extends prior work | Arithmetic | Model numbers | Below a majority only | Kept, narrowed |
| Blockspace as an aggregate limit | New, as far as searched | Arithmetic | Measured release size | Weak | An observation, not a safety claim |
| Bitcoin headers as a chip's licence clock | Extends prior work | None | Not built | Fatal | Cut |

Four results deserve a sentence each, because they changed the paper. The red team's correlated
claims broke the first fake-record bound, and the round rule of section 4 is the repair. The lab
showed that a two-transaction proof of a release accepts the agent's own copies of the template and
a Tier 3 release no guardian signed, so releases are proved over the whole chain. The red team
showed that a training reward on events the agent can move pays it to manipulate them, so the
training claim is limited to events it cannot. And the adoption simulation had barred harmful actors
from joining; corrected, it showed them cycling through fresh identities at a profit, so the claim
that routing around becomes costly is withdrawn.
