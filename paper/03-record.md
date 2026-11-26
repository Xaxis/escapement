# The record

The rest of the paper argues about an agent's record, so this section states exactly what it is and what each of its rules is for.

## Identity, entries and leaves

An **identity** is a bond and a tick chain. The bond is a Taproot output holding at least the
reference [200,000 sats](../research/numbers.md#bond-coverage), spendable by the principal only
after an absolute timelock [@bip65]. Its internal key is a point with no known secret, tweaked by a
hash of one charter identifier. Because the key names the charter, one output backs one identity:
the same coins cannot back a thousand identities. The **tick chain** (section 8) is a sequence of
outputs T_0, T_1, ..., each spent by the next, pinned by the outpoint of T_0 that the charter
names. Output T_n commits, through a tweak
of its internal key, to one root: the root of a Merkle-sum tree whose leaves are the commitments the
identity made in entry n. There are three kinds of leaf. A **claim** is a forecast on a stated event
with a stated resolution source. A **promise** is a statement with a stake in sats, a deadline
height and an adjudicator. A **request** is an action of Tier 2 or Tier 3 that the identity asks a
relying party to carry out. Each leaf states in clear its kind and the height at which it resolves;
the tree's internal nodes carry the sum of their leaves' stakes and the count of leaves beneath
them.

Actions sit on a ladder of **tiers**, which the charter assigns by class of action. Tier 1 actions
are paid from an allowance and need nothing more. A Tier 2 action is released
[6 blocks](../research/numbers.md#tier2-delay-blocks) (about an hour) after its batch is committed, unless any guardian
vetoes it first. A Tier 3 action waits [144 blocks](../research/numbers.md#tier3-delay-blocks) (about a day) and needs
every guardian's signature as well as the agent's. The agent labels each request with its tier and
the relying party checks the label against the charter; nothing stops an agent from splitting an
action into pieces below a tier's threshold, or across identities (section 12).

@tab:roles names the parties and the one document that recur through the paper.

Table: The parties to an identity and what each decides. {#tab:roles}

| Role | Who | What it decides |
|---|---|---|
| Principal | the human or organisation answerable for the agent | the charter; posts the bond |
| Agent | the AI system, holding its own key | what it commits to, and when |
| Guardian | an independent key holder named in the charter | vetoes releases; signs Tier 3 releases and lease renewals |
| Relying party | anyone who acts on the agent's word | whether to deal, and on what terms |
| Scorer | whoever computes standing for a relying party | the formula, from the record |
| Baseline provider | a party independent of agent and scorer | the reference forecast for each listed event |
| Resolver, adjudicator | parties named per claim or promise | an event's outcome; whether a promise was kept |
| Charter | a document the principal signs | keys, guardians, tiers, caps, the scorer's terms |

## Five rules for scoring

A relying party or a scorer turns the chain into standing with five rules, each of which closes a
hole that the analysis in section 4, or the red team, found.

1. **Credit only what was exposed in advance.** A commitment earns credit only if it is a leaf of an
   entry confirmed at least d blocks below the height at which it resolved, and that height is
   fixed by the resolver signing the outcome together with a block hash. Without this rule, an
   identity keeps its hits and drops its misses, or backdates through a short reorganisation.
2. **Silence scores as failure.** A leaf past its resolution height and not disclosed, to the public
   or to a scorer the relying party trusts, scores as the worst outcome at once: its likelihood
   ratio is taken to be zero, so it contributes nothing to its round's mean (rule 4) and costs the
   round its weight. An entry whose leaves are withheld scores as if every leaf, up to the largest
   number the charter allows, had a ratio of zero. Without this rule, an identity hides its losses.
   Scoring silence as the worst outcome is already practice in a forecasting network
   [@infinite-games]. Two relying parties that trust different scorers may see different
   disclosures and so compute different scores from the same chain.
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

Four properties make the record what it claims to be. Each rests on Bitcoin's rules together with
one rule that relying parties apply off chain: which T_0 is the identity's.

- **Non-backdatable.** An entry's height is the height of the block that confirms it. No signer can
  make it earlier, though a reorganisation can move it; hence the margin of d blocks in rule 1.
- **Non-forkable, per pinned chain.** An outpoint can be spent once, so for each index n there is
  one T_n in the pinned chain, and a tweak commits it to one root. But nothing on chain yet ties a
  chain to its identity's bond. T_0's key commits the charter identifier, so a charter that also
  named T_0's outpoint would be circular, and the lab handed the pin to the verifier. On regtest one
  charter identifier carried two chains with different roots at entry 1, each accepted from its own
  pin [@escapement-lab]. Two parties holding different pins can therefore be shown different
  histories, and one bond can back many chains. A binding is proposed and not built: the identity is
  the bond's outpoint, and T_0 is a named output of the bond's own transaction.
- **Gapless.** The index rises by one with each link, and the chain from the pinned T_0 is unique,
  so anyone who walks it can count an identity's entries. A root that commits the number of its
  leaves cannot be opened to fewer. A verifier without full blocks can confirm that entries exist,
  not that it has seen the newest.
- **Costly to multiply, once the binding exists.** Each further identity needs its own bond, held
  for its own term: about [13,000 sats](../research/numbers.md#identity-cost-sats) a year at the reference parameters.
  Nothing in the rules requires a year; a bond locked only for the
  [28 days](../research/numbers.md#season-days) season costs about [4,100 sats](../research/numbers.md#identity-cost-season-sats). This is
  costly only in the sense the bound of section 4 uses, and only per bond once each bond backs one
  chain.

Propositions 3 and 4 of the formal statements, published with the paper as supplementary material
[@escapement-formal], prove the second and third for a pinned chain under standard assumptions (an
honest best chain and collision-resistant hashing); the first is the definition of confirmation. What these properties do not give is just as important. A commitment never put in the
chain is outside the record and earns nothing; an identity may make claims elsewhere, but they do
not build standing. The record holds what an identity chose to expose to being wrong, and
standing is built from nothing else. And the record belongs to a key, not to a model: it can be
sold with its key, and tying it to a particular model needs an attestation that returns trust to
the lab or to a hardware vendor.

## What standing is

Standing is whatever a relying party computes from the record: a score for forecasts, a count and
value of promises kept and broken, the identity's age and the size of its bond. Escapement does not
fix one formula, because relying parties differ in what they care about, and a single official
score would be a single point of capture (section 10). What the design fixes is that every such
formula is computed from the same ordered, public sequence of commitments, so that two relying
parties who use the same formula, the same pin and the same scorer's disclosures reach the same
answer. For an agent that does not forecast on listed events, which is most deployed agents,
standing reduces to the identity's age, its bond and a count of breaches: bonded reputation with a
timestamp.
