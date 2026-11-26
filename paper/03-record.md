# The record

An agent's record is the object that the rest of the paper argues about, so it is worth stating
exactly what it is and what each of its rules is for.

## Identity, entries and leaves

An **identity** is a bond and a tick chain. The bond is a Taproot output holding at least the
reference [200,000 sats](../research/numbers.md#bond-coverage), spendable by the principal only
after an absolute timelock [@bip65], whose internal key is a point with no known secret tweaked by a
hash of one charter identifier. Because the key names the charter, one output backs one identity:
the same coins cannot be named by a thousand. The **tick chain** (section 8) is a sequence of
outputs T_0, T_1, ..., each spent by the next, pinned by the outpoint of T_0 that the charter
names. Output T_n commits, through a tweak
of its internal key, to one root: the root of a Merkle-sum tree whose leaves are the commitments the
identity made in entry n. There are three kinds of leaf. A **claim** is a forecast on a stated event
with a stated resolution source. A **promise** is a statement with a stake in sats, a deadline
height and an adjudicator. A **request** is an action of Tier 2 or Tier 3 that the identity asks a
relying party to carry out. Each leaf states in clear its kind and the height at which it resolves;
the tree's internal nodes carry the sum of their leaves' stakes and the count of leaves beneath
them.

## Five rules for scoring

A relying party or a scorer turns the chain into standing with five rules, each of which closes a
hole that the analysis in section 4, or the red team, found.

1. **Credit only what was exposed in advance.** A commitment earns credit only if it is a leaf of an
   entry confirmed at least d blocks below the height at which it resolved, and that height is
   fixed by the resolver signing the outcome together with a block hash. Without this rule, an
   identity keeps its hits and drops its misses, or backdates through a short reorganisation.
2. **Silence scores as failure.** A leaf past its resolution height and not disclosed, to the public
   or to a scorer the relying party trusts, scores as the worst outcome at once, and an entry whose
   leaves are withheld scores as if every leaf, up to the largest number the charter allows, had the
   worst outcome. Without this rule, an identity hides its losses.
3. **One forecast per event.** The scorer keeps only the first forecast an identity makes on an
   event. Two forecasts on one event let an identity inflate its expected score (section 4 gives
   the counterexample).
4. **Score in rounds, against a baseline.** Forecasts are scored relative to a baseline, published
   by a party independent of the agent and of the scorer, on events from a list the agent did not
   write. Claims are scored in rounds that do not overlap, and a round counts as the weighted mean
   of its claims' likelihood ratios. Without the baseline, volume looks like skill; without the
   rounds, claims chosen to move together fake a record (section 4).
5. **Score from genesis.** A score runs over the whole chain, never over a window chosen after the
   fact.

## The properties Bitcoin supplies

Four properties make the record what it claims to be, and each is a consequence of Bitcoin's rules
rather than of anyone's honesty.

- **Non-backdatable.** An entry's height is the height of the block that confirms it. No signer can
  make it earlier, though a reorganisation can move it; hence the margin of d blocks in rule 1.
- **Non-forkable.** An outpoint can be spent once, so for each index n there is one T_n in the
  pinned chain, and a tweak commits it to one root. An identity cannot show two parties two different
  entries.
- **Gapless.** The index rises by one with each link, and the chain from the pinned T_0 is unique,
  so anyone who walks it can count an identity's entries. A root that commits the number of its
  leaves cannot be opened to fewer. A verifier without full blocks can confirm that entries exist,
  not that it has seen the newest.
- **Costly to multiply.** Each further identity needs its own bond, held for its own term: about
  [13,000 sats](../research/numbers.md#identity-cost-sats) a year at the reference parameters, which
  is costly only in the sense the bound of section 4 uses.

Propositions 3 and 4 of the formal appendix prove the second and third under standard assumptions
(an honest best chain and collision-resistant hashing); the first is the definition of
confirmation. What these properties do not give is just as important. A commitment never put in the
chain is outside the record and earns nothing; an identity may make claims elsewhere, but they do
not build standing. The record records what an identity chose to expose to being wrong, and
standing is built from nothing else. And the record belongs to a key, not to a model: it can be
sold with its key, and tying it to a particular model needs an attestation that returns trust to
the lab or to a hardware vendor.

## What standing is

Standing is whatever a relying party computes from the record: a score for forecasts, a count and
value of promises kept and broken, the identity's age and the size of its bond. Escapement does not
fix one formula, because relying parties differ in what they care about, and a single official
score would be a single point of capture (section 10). What the design fixes is that every such
formula is computed from the same complete, ordered, public sequence of commitments, so that two
relying parties who use the same formula reach the same answer and neither can be shown a better
history than the other.
