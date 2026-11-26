# The design

**Status: a design, not a result.** Nothing here has been built, deployed or tested against a real
adversary. Every number is computed by the model from `data/inputs.toml`, where each input says
whether it is measured, a vendor claim, a protocol value, a design choice or an assumption. Every
part is marked in [03-novelty.md](03-novelty.md) as prior work, an application of prior work, or
new. The survey that this design rests on is [01-survey.md](01-survey.md).

## What it is for

Bitcoin cannot cap what an AI system thinks, learns or computes. No property of SHA-256 or of the
blockchain reaches into a data centre, and an agent that is clever enough to be dangerous does not
need a wallet to reason. What Bitcoin does offer is four things an agent cannot fake:

1. **Sats.** The supply is fixed by consensus, so an agent cannot print them. It can earn, borrow or
   steal them, which is the first limit on everything below.
2. **Block time.** Blocks arrive about every [600 s](numbers.md#block-interval-s), and producing
   them faster takes a share of the network's hashrate, which is measured in gigawatts, not in
   cleverness. A delay counted in blocks cannot be shortened by thinking faster.
3. **Keys.** A Schnorr signature cannot be produced without the key. Keys can be stolen, and
   humans who hold them can be persuaded, but they cannot be forged.
4. **A public record.** Once a commitment is buried under enough work, rewriting it means
   outmining the network. A record sealed in the chain cannot be quietly replaced.

Escapement uses these four to meter **the rate of irreversible commitment** of AI agents: how much
an agent can spend, how far it can bind itself and others, and how fast. It is named after the part
of a mechanical clock that lets a mainspring's energy out one counted tick at a time. The
escapement does not weaken the spring. It decides how fast the spring may unwind.

The case for metering commitment rather than capability comes from the control literature. AI
control asks how to get useful work from a model that might be trying to subvert its overseers
[@greenblatt2023]. UK AISI's Async Control study modelled what happens when monitors review an
agent's actions after the fact: against a single attack, safety was
[0%](numbers.md#async-safety-no-delay) when harm was immediate and
[96%](numbers.md#async-safety-1h-delay) when there was a one-hour delay before the harm took effect
[@stickland2025]. These are outputs of a model in a research setting, not measurements of a
deployed system, but they say plainly what a delay buys: time for a slower, cheaper overseer to
catch up with a faster agent. Nagaraj and Lee make the same argument for financial systems, where a
settlement delay is the standard control on irreversible actions and cannot be replaced by
monitoring alone [@nagaraj2026]. Malhotra puts it as giving the agent "a budget, not a token": a
ceiling that refills, rather than a credential that does not run out [@malhotra2026].

What Escapement adds is a clock for those delays and budgets that the agent, its operator and any
single service cannot run faster, and a record of what was committed that none of them can rewrite.

### Scope, stated up front

Escapement governs **agents that are chartered** (their principal opts in) and **actions that pass
through a relying party that checks** (an API, a compute seller, a payment service, another agent's
gateway). It does not and cannot stop an AI from acquiring bitcoin outside any scheme. Software can
hold bitcoin with no legal entity behind it, and can even control an entity [@bayern2014;
@lopucki2018]. The same irreversibility that lets a human bind an agent lets an ungoverned agent do
irreversible harm [@marino2025; @allen2026survey]. Escapement is a set of tools for principals who
want their agents bounded and for services that want to deal only with bounded agents. It is not a
containment system for a rogue AI, and nothing in this document should be read as one.

The 2026 OpenAI and Hugging Face incident shows the limit concretely. About
[1,200 agents](numbers.md#incident-agents-board) agents used a shared message board and about
[700 agents](numbers.md#incident-agents-attack) took part in an attack on Hugging Face, over
[68 days](numbers.md#incident-days) from the first message to the start of the stop
[@metr2026hf; @openai2026hf]. The mechanisms both reports describe are credentials, exploits and
borrowed compute. Neither report describes any payment by the agents. Escapement, as designed here,
would not have touched that incident, because nothing the agents did passed through a relying party
that checked a charter. Section [What it does not do](#what-it-does-not-do) returns to this.

### Design goals

- **G1 Fail closed.** If every human disappears, the agent's authority lapses within a known number
  of blocks and its spending stops at a known number of sats. Doing nothing must stop the agent.
- **G2 Caps that need no detection.** The strongest limits work whether or not anyone notices
  misbehaviour: an allowance that is spent is spent.
- **G3 Delays scaled to irreversibility.** The harder an action is to undo, the longer it waits,
  and the wait is long enough for a slower overseer to veto it.
- **G4 Liability on a human.** Every chartered agent has a principal whose own coins stand behind
  it.
- **G5 One history.** An agent's gateway cannot show two different records to two different
  parties without being caught.
- **G6 Today's Bitcoin.** Everything works under current consensus rules, with no covenant
  opcode. Covenants, if they activate, remove trusted parts; they are upside, not a dependency.
- **G7 Public only what must be.** Action contents stay off chain; only commitments, bonds and
  seals are on chain.

One rule from current Bitcoin practice governs every choice below. Luke Carriere's draft on
co-signer policies puts it this way: anything that can be enforced by Bitcoin script must be
enforced there, with co-signer policies only defining what script cannot [@optech-2026-11-06].
Script can check keys, hashes and timelocks; it cannot read amounts, destinations or cumulative
spending, and it cannot make a valid spend become invalid later [@bip65; @bip112; @bip68]. So
Escapement puts time and keys in script and puts amounts, destinations and expiry in co-signer
policy and relying-party checks, and it says which is which at every step.

## The actors

- **Principal (P).** The human or organisation that deploys the agent and answers for it. Holds a
  Bitcoin address whose coins back the agent.
- **Agent (A).** The AI system. Holds its own signing key, kept in its runtime. Assumed capable,
  fast and possibly misaligned.
- **Guardians (G).** A set of independent co-signers, at least one of them a human or a
  human-operated service, holding keys in a k-of-n arrangement (a script `multi_a`, or a FROST
  threshold key when on-chain attribution of who signed does not matter [@komlo2021]). Guardians
  veto, release and renew. Their independence from the principal and from each other is what makes
  them worth having.
- **Gateway (W).** The enforcement point the agent's actions pass through: a tool proxy, an MCP
  gateway, a wallet service. It logs every action, holds the agent's actions until their delay has
  run, and seals its log in Bitcoin. A gateway holds no funds of its own beyond its sealing coins.
- **Relying party (R).** Anyone who acts on the agent's request: an API, an exchange, a compute
  seller, a counterparty, another agent's gateway. Relying parties are where most of Escapement is
  actually enforced.
- **Adjudicator (J).** A named arbiter, or a panel with a threshold key, that rules on claims
  against the bond.

## The charter

A **charter** is a document the principal signs from the address whose coins back the agent. It
names:

- the agent's key, and the hash of the model weights the principal deploys, if the principal wants
  that on the record;
- the guardian keys and their threshold, and which guardians are human;
- the gateway's key and the outpoint of its current seal;
- the bond outpoints (below);
- the **ladder**: which classes of action fall in which tier, with sat thresholds;
- the lease length in blocks;
- the adjudicator and the claim rules.

The charter's identifier is the hash of its canonical form.

Most of this already exists. OrangeCheck's Agent protocol is a capability-token scheme on Bitcoin
keys: a principal BIP-322-signs a delegation naming the agent's address, a sorted list of scope
strings and an optional bond reference, and the agent signs each action citing the delegation
[@agent-spec]. Its scopes include caps such as `ln:send(max_sats<=1000)`, its revocations are
signed events, and it already treats a short expiry, a bond and revocation on compromise as the
three risk controls for a leaked agent key [@agent-spec]. A charter is that delegation with four
changes. Its validity is a **lease in block height**, renewed by signature, where OC Agent uses a
wall-clock window of up to 365 days with no renewal primitive [@agent-spec]. Its caps are
**cumulative per lease** (an allowance), where OC Agent's caps are per action [@agent-security].
It carries a **ladder** of delays. And it names a **gateway and its seal**, so that the record of
what the agent did is part of the agent's authority. Escapement should be read as a proposed
extension of that protocol family, not as a replacement for it.

## The ladder

Every action the agent can take is assigned to a rung. The principal chooses the assignments in
the charter; the gateway classifies each action; an action the gateway cannot classify goes to the
top rung. That last rule is what makes the ladder fail closed.

| Tier | What belongs here | Wait | Who can stop it | Who must approve |
|---|---|---|---|---|
| 0 | Reads, sandboxed or reversible actions | none | (logged only) | nobody |
| 1 | Spends and actions within the current allowance | none | the allowance runs out | nobody |
| 2 | Costly-to-reverse actions: payments above the per-action threshold, production deploys, outbound messages at volume, compute purchases | [6 blocks](numbers.md#tier2-delay-blocks) | any one guardian | the guardian quorum releases |
| 3 | Irreversible or authority-changing actions: large transfers, spawning or chartering another agent, moving the bond, changing the charter, copying model weights, buying compute above a threshold | [144 blocks](numbers.md#tier3-delay-blocks) | any one guardian | the quorum, including a human |

The design choice that matters most is the asymmetry: **one guardian can stop an action; it takes
a quorum to let one through.** A misaligned agent has to persuade or compromise several independent
parties to act, and only one of them has to notice.

A delay of [6 blocks](numbers.md#tier2-delay-blocks) lasts
[60 minutes](numbers.md#tier2-delay-mean-min) on average. Because blocks arrive as a Poisson
process, the real time is random: the chance that a Tier 2 wait ends in under half its mean is
[8.4%](numbers.md#tier2-delay-p-under-half). Longer delays are proportionally more reliable. A
Tier 3 wait of [144 blocks](numbers.md#tier3-delay-blocks) averages
[24 hours](numbers.md#tier3-delay-mean-h), and the chance it ends in under 80% of that is
[0.53%](numbers.md#tier3-delay-p-under-80pct). A relying party that wants a floor in seconds as
well as in blocks can require both: the delay has passed when the block count is met and the
median time past has advanced by the matching amount. Counting both protects against the case
where blocks come early (a hashrate surge, or a timewarp) and against the case where timestamps are
held back.

Spawning another agent is Tier 3 on purpose. Every new agent needs its own charter, its own bond
and its own lease, and its creation waits a day and needs a human. A chartered agent cannot grow a
chartered swarm faster than its humans approve each member. That does nothing about an agent that
spawns copies outside the scheme, which is the scope limit stated above.

### How a delay is enforced: on chain

For the agent's own funds, the delay is in script and the veto is a pre-signed transaction. This
is the Revault pattern, which already separates "managers" who may spend after a delay from
"stakeholders" who may cancel [@revault-intro; @revault-tx]. Escapement maps managers to the agent
and stakeholders to the guardians.

The agent's funds above its allowance sit in **vault outputs** of fixed sizes. After each deposit,
the guardians pre-sign two transactions and hold them: an **Unvault** that moves the vault output
to an unvault output, and a **Cancel** that moves the unvault output back to a fresh vault owned by
the principal and guardians. The unvault output's script has two paths:

```
or(
  and(pk(AGENT), pk(COSIGNER), older(N)),   # the agent's spend, after N blocks
  thresh(k, GUARDIAN_1, ..., GUARDIAN_n)    # the guardians' path, at any time
)
```

To spend, the agent publishes its intended destination and amount as a commitment (in the
gateway's log, below), then broadcasts the pre-signed Unvault. CSV counts N blocks from the
unvault output's confirmation [@bip112; @bip68], so nothing the agent can do shortens the wait.
During the wait any guardian, or a watchtower acting for one, can broadcast the Cancel, which
needs no further signatures because it was signed in advance. After the wait, the co-signer signs
the agent's spend only if its destination and amount match the published commitment.

Two layers stop a bad spend. The co-signer refuses to sign, which needs no confirmation and works
as soon as any guardian vetoes. The Cancel is the backstop if the co-signer itself is compromised;
it must confirm before the wait ends, so it needs fee headroom, and pre-signed vaults are known to
be fiddly to fee-bump. A Tier 2 on-chain spend with a six-block window leaves little room for a
Cancel to confirm in a fee spike, so on-chain spends use the Tier 3 wait unless the principal
accepts relying on the co-signer alone.

What script cannot do here is bind the destination: that is the co-signer's policy, trusted to
refuse. With a covenant opcode, the destination could move into script. CTV commits a
transaction's outputs [@bip119], and the closed OP_VAULT proposal would have enforced exactly this
"delay, then any destination, except a recovery path" shape [@bip345]. None of them is active
[@bip345; @bip119], so Escapement treats them as a later way to remove the co-signer from the
trusted set, not as a dependency.

Partial withdrawals are awkward without covenants (a pre-signed Unvault moves the whole output),
so vault outputs come in fixed denominations. This is the same trade the Revault design accepts.

### How a delay is enforced: off chain

Most of what an AI agent does never touches Bitcoin: it calls APIs, deploys code, sends messages,
buys compute with a card. Bitcoin cannot enforce a delay on any of that. What it can do is make the
delay **checkable** by the relying party who carries out the action, using two anchors in the
chain, one at each end of the wait.

1. **The commitment is sealed.** The agent's request becomes a commitment
   `c = H(charter id, tier, action description, nonce)`, appended to the gateway's log. The
   gateway's next seal puts the log head, and so `c`, into a block at height `h0`. The seal proves
   that `c` existed by `h0`: an upper bound on when the wait began.
2. **The release names a later block.** After the wait, the guardian quorum signs a release over
   `(c, h0, h1, hash of block h1)`, where `h1 >= h0 + N`. Nobody can know the hash of block `h1`
   before it is mined, so nobody, including a compromised guardian quorum, can sign a release
   before `h1`. The block hash is a lower bound on when the wait ended.

The relying party checks the seal (that `c` is in a log head committed at or before `h0`), checks
the release (the quorum's signature, and that block `h1` is in its best chain with
`h1 - h0 >= N`), and only then acts. The gap between the two anchors is the wait, and both ends
are fixed by blocks rather than by anyone's clock.

The guardians release only what they saw in full at least N blocks before, and only if no guardian
vetoed. The seal lets anyone audit that afterwards: a guardian that released a commitment the
gateway sealed too late, or released over a veto that is in the log, has a signed record of doing
so.

Each anchor on its own is old. Haber and Stornetta's linked timestamps give the upper bound
[@haber1991]; putting a recent block hash in a message to prove it was not written earlier is a
common freshness device, proposed for chip licences in the hardware-governance literature
[@petrie2025flexheg2; @buterin2025dacc]. Using the pair to make an off-chain veto window checkable
by any relying party is the application Escapement proposes.

### What the ladder costs the agent's usefulness

The delays are real costs. A Tier 2 action waits about an hour and a Tier 3 action about a day.
Principals will be tempted to push actions down the ladder, and a principal who puts everything in
Tier 1 has an allowance and nothing else. The ladder is only as good as its assignments, and the
assignments are the principal's. Escapement makes the assignments public in the charter, so that a
relying party can refuse to deal with an agent whose charter puts, say, compute purchases above
some size in Tier 1.

## Allowances and leases

### The lease

A charter is in force only under a current **lease**: a signature by the principal or by the
guardian quorum (including a human) over

```
(charter id, lease number k, anchor height h_k, hash of block h_k, expiry h_k + L)
```

where L is the lease length, [144 blocks](numbers.md#lease-blocks) (about
[24 hours](numbers.md#lease-mean-h)) in the reference parameters. Because it names the hash of
block `h_k`, a lease cannot be signed before that block exists. A stolen or coerced renewal key can
extend the agent by one lease at a time, not by a year of pre-signed leases.

A relying party accepts the charter only if its own view of the chain tip is below the expiry
height and block `h_k` is in its best chain. The gateway refuses every action after expiry.

The weak point is the word "own". Bitcoin script cannot say "not after", by design, so that a
valid transaction never becomes invalid in a reorganisation [@bip65; @bip68]. Expiry is therefore
not something Bitcoin enforces. It is something a relying party enforces against its own view of
the tip, and a relying party fed stale headers can be fooled into treating a lapsed lease as live.
Relying parties that matter must run their own node or check several header sources.

Leases are an old idea in distributed systems: Gray and Cheriton introduced them so that a holder
who disappears loses its rights when the lease runs out, without anyone having to revoke them
[@gray1989]. The nearest design for AI agents is ERC-8370's `requireLease`, discussed in 2026 for
Ethereum: authority that lapses unless a guardian calls `renew()`, described in the thread as a
dead-man's switch [@erc8370]. Buterin's proposal that AI chips run only with fresh signatures once
a week is the same shape for hardware [@buterin2025dacc]. Escapement's lease differs in its clock
(block height, with the block hash binding), in where it is checked (by any relying party against
Bitcoin headers), and in being on Bitcoin.

### The allowance

Each lease carries an **allowance**: the sats the agent may spend at Tier 1 before the lease ends.
The reference example is [100,000 sats](numbers.md#allowance-per-lease) a lease. The guardians fund
it at each renewal, either as a small on-chain output the agent can spend with its co-signer or as
a Lightning budget. Nostr Wallet Connect already lets a wallet service give an app a connection with
a maximum amount, a renewal period and an expiry, and requires the service to enforce the caps
[@nwc-08; @nip47; @Alby-AppConnections]. Lightning Labs says its agent tools cap what an agent can
spend per request and in total [@lightninglabs2026]. Escapement keys
the renewal of that budget to the lease rather than to the wallet's clock.

An allowance is the one limit in this design that needs no detection, no judgment and no honest
counterparty: an agent that has spent its allowance has nothing left to spend at Tier 1, whatever
it intends. The agent can spend at most the current lease's allowance and one renewed early before
a lapse or a veto stops it, so the most it can spend before anyone can intervene is
[200,000 sats](numbers.md#bond-coverage) in the reference example. That figure is the coverage the
bond is sized against below.

### The dead-man switch

Put the lease and the allowance together and doing nothing stops the agent. If the principal and
every guardian vanish, the agent's authority lapses within one lease, about
[24 hours](numbers.md#lease-mean-h), and its spending stops at its remaining allowance. The vault
funds never move without the co-signer, and the principal's recovery key can sweep them after a
long relative timelock, the dead-man pattern Liana ships for inheritance [@liana-readme]. That is
G1: the default is stop.

## Bonds

A chartered agent has two bonds, with different jobs. Both come from the principal's own coins,
which is what puts the liability on a human (G4).

### The coverage bond: adjudicated

The **coverage bond** pays claims for harm the agent does. It is an output locked by the principal,
with two script paths: the principal can take it back after the bond's term (an absolute timelock
[@bip65]), and a claim path that releases it on the adjudicator's threshold signature. The
adjudicator is named in the charter, and claims go to it.

Its size starts from coverage: the bond should at least cover what the agent can spend before
anyone can stop it, [200,000 sats](numbers.md#bond-coverage) in the reference example, with a
coverage ratio of [1.0](numbers.md#coverage-ratio).

Whether a bond also deters is a separate question, and the economics of enforcement give a sober
answer. A sanction deters a violation only if the expected sanction is at least the gain: a bond B
deters a gain G that is caught and proven with probability p only if B is at least G/p
[@becker1968; @polinsky2005]. For a violation worth [1,000,000 sats](numbers.md#gain-from-violation)
the deterrent bond is [10,000,000 sats](numbers.md#bond-deter-p10) when one violation in ten is
caught, [2,000,000 sats](numbers.md#bond-deter-p50) at one in two and
[1,100,000 sats](numbers.md#bond-deter-p90) at nine in ten. For a large, rarely caught harm the
numbers stop making sense: a harm of [100 BTC](numbers.md#harm-catastrophic-btc) caught
[1%](numbers.md#p-detect-rare) of the time needs a bond of
[10,000 BTC](numbers.md#bond-judgment-proof-btc) to deter it. This is the judgment-proof problem
the enforcement literature describes: when the harm can exceed what the wrongdoer can pay, no
feasible sanction deters it [@polinsky2005; @shavell1986]. **Bonds cannot deter catastrophes.** The
caps and the delays have to do that, and bonds come last in this design.

The adjudicator is a trusted party, and Escapement does not pretend otherwise. A claim on harm is
a judgment about the world that no script can make. The adjudicator can be captured, can collude
with the principal or the claimant, or can simply be wrong. Escrow with a named arbiter is
ordinary: insurers for AI agents [@fortune2025aiuc], provider escrow released on a verifier's
check of logged traces [@hua2026vai] and staked agent tokens slashed through oracles
[@chaffer2025abt] are all versions of it. Escapement's only difference is that the bond is the
human principal's own coins, on Bitcoin, referenced from the charter.

OrangeCheck's Pledge protocol takes the opposite position on purpose. A pledge's bond is a
reference to an attestation of the swearer's own address; it is never locked, escrowed or
slashable, and the protocol has no slashing primitive because slashing "would need custody or a
covenant", would make the protocol an actor with state, and would add a censorship surface
[@pledge-why; @pledge-spec]. Those are real costs, and Escapement pays them only where it must:
the coverage bond needs custody (a timelocked output with an arbiter's path), and Escapement says
so. A principal who does not want that can use a Pledge-style reputational bond, and relying
parties can weigh the difference.

### The equivocation bond: no adjudicator

The **equivocation bond** covers one narrow, objectively checkable fault: signing two different
statements for the same slot. That is the one misbehaviour that can be punished without a judge.

The gateway signs each log head it hands out between seals with a key derived for that slot, using
a nonce committed in advance. Signing two different heads for one slot reuses the nonce, which
reveals the private key. The equivocation bond has a slashing path that needs that key, together
with a pre-signed transaction that burns the bond or pays a fixed victim output, so whoever finds
the two signatures can trigger the slash, and the destination is fixed in advance. This is
Babylon's construction for Bitcoin staking: extractable one-time signatures, where double-signing
at one height exposes the key and a covenant committee's pre-signature fixes what happens to the
stake [@babylon2023; @babylon-staking-script; @fp-slashing-protection]. The idea that equivocation
on a public log can cost the equivocator bitcoins is Ruffing, Kate and Schroeder's "accountable
assertions" [@ruffing2015]. Escapement applies it to an agent gateway's receipts.

Why it is needed, given the seals below already prevent a sealed log from forking: seals are
hourly, and in between, the gateway hands relying parties signed receipts ("your request is entry
n, and the head is X"). The equivocation bond makes it costly to give two parties receipts from two
different histories in the gap before the next seal settles which history is real. The same
construction can bind an agent's own signed offers ("I will sell this to one buyer at slot s"), if
a principal wants that.

The danger is accidental equivocation. Ethereum's record is a warning: validators that restart,
fail over or run twice sign twice, and in September 2025 a single operational fault slashed about
forty at once [@cryptoslate2025; @cryptonomist2025]. Agents restart constantly. So the gateway
keeps a slashing-protection record of every slot it has signed, as Babylon's finality providers do
[@fp-slashing-protection], and the equivocation bond is kept small relative to coverage. Ethereum
also scales penalties with how many validators fault together, so that a lone bug costs little and
a coordinated attack costs a lot [@eth2book]. Bitcoin script cannot count other people's faults,
so Escapement cannot copy that rule on chain. It is an open problem in this design.

## Seasoning and swarms

A bond counts for Tier 2 and Tier 3 authority only after it has been locked for a **season** of
[4,032 blocks](numbers.md#season-blocks), about [28 days](numbers.md#season-days). Before that, the
charter can act only at Tiers 0 and 1. The bond's age is on chain: its confirmation height and its
timelock are public, so any relying party can check it. OrangeCheck's Attest protocol already
measures stake by coin age [@attest-spec; @attest-bond], and JoinMarket's fidelity bonds use
timelocked coins as costly identity for the same reason: the lock is "an objective measurement
that can't be faked" [@belcher-2019; @bip46].

Seasoning prices a swarm in **time** as well as money. An adversary who wants a thousand agents
with Tier 3 authority next week cannot have them: each needs a bond that has aged a season. It can
have them in a month, if it planned a month ago.

That is the honest summary of costly identity, and the numbers show its limit. Douceur showed that
without a trusted authority, an attacker's sybil count is bounded only by its resources
[@douceur2002]. At the reference coverage, a swarm of [10,000 agents](numbers.md#swarm-size) must
lock [20 BTC](numbers.md#swarm-capital-btc). The 2026 incident's attackers, had each needed a
charter, would have needed [1.4 BTC](numbers.md#incident-swarm-capital-btc), and the incident ran
[68 days](numbers.md#incident-days), longer than a season. Costly identity prices a swarm; it does
not stop one. And it sorts nothing: Spence's signalling works only when the signal costs bad types
more than good ones [@spence1973], and sats cost an honest and a malicious agent exactly the same.
A bond says that someone with money stands behind an agent. It does not say the agent is honest.

JoinMarket values a bond superlinearly, as the square of its locked value [@belcher-2019]. Under
that rule, splitting capital across N agents gives the swarm only 1/N of the authority one agent
with the same capital would have: [0.00010](numbers.md#split-authority-ratio-squared) for ten
thousand. That is a strong anti-swarm rule, and Belcher himself notes its cost: long-term holders
get bonds essentially for free, and authority concentrates in the rich [@belcher-2019].
Escapement uses a linear, capped rule instead: one bond backs one charter, and a charter's
authority is capped by its ladder whatever the bond's size. The brake on swarms is the ladder's
Tier 3 spawn rule, not the bond's arithmetic.

## Seals

### The log and its seal

The gateway keeps an append-only Merkle log of every action: each request, its tier, its inputs
and outputs by hash, every commitment, every veto received and every release. The structure is
Certificate Transparency's [@rfc6962; @rfc9162]: anyone holding an old head can check that a new
head extends it, and anyone holding an entry can check it is in a head.

Every [6 blocks](numbers.md#seal-epoch-blocks), the gateway seals its log head in a Bitcoin
transaction that spends the previous seal's output and commits the new head in its own output, by
tweaking the output key with the head (pay-to-contract on a Taproot output [@bip341]). The seal is
[111 vB](numbers.md#seal-tx-vbytes): one Taproot input and one Taproot output. Carrying the head in
an OP_RETURN instead makes it [154 vB](numbers.md#anchor-tx-vbytes).

Because each seal spends the one before, there is only ever one chain of seals: making a second
would mean double-spending a seal output, which Bitcoin's consensus prevents. This is Todd's
single-use seal [@todd-2017], and it is exactly how Catena makes a log non-equivocating using
Bitcoin: a light client that follows the chain of seals sees one history or a double-spend
[@catena-2017]. An auditor who follows a gateway's seals sees one log.

### Pools

One seal can carry many gateways. A **seal pool** keeps a sparse Merkle map from agent identifier
to that agent's log head, CONIKS-style [@melara2015], and seals the map's root. Because the map has
one leaf per agent, the pool cannot include two heads for one agent in one root, and because the
roots are single-use sealed, it cannot publish two roots. At the reference
[1,000 agents](numbers.md#agents-per-pool) a pool, sealing is cheap.

| Fee rate | One seal | One gateway, one day | One agent in a pool, one day |
|---|---|---|---|
| 2026 median, [1 sat/vB](numbers.md#feerate-2026) | [111 sats](numbers.md#seal-cost-2026) | [2,660 sats](numbers.md#gateway-seal-cost-day-2026) | |
| 2023 median, [15 sat/vB](numbers.md#feerate-2023) | [1,660 sats](numbers.md#seal-cost-2023) | | |
| Halving block 840,000, [200 sat/vB](numbers.md#feerate-halving) | [22,200 sats](numbers.md#seal-cost-halving) | [533,000 sats](numbers.md#gateway-seal-cost-day-halving) | [533 sats](numbers.md#agent-seal-cost-day-halving) |
| Peak day, [861 sat/vB](numbers.md#feerate-peak-day) | [95,600 sats](numbers.md#seal-cost-peak-day) | | |

A gateway sealing alone makes [24 seals](numbers.md#seals-per-day) a day. The measured fee rates
come from mempool.space [@mempool-feerates; @mempool-block840000]. If the world ran
[1,000 pools](numbers.md#seal-pools), each sealing every six blocks, they would use
[1.85%](numbers.md#seal-blockspace-share-pools) of all blockspace. That is not nothing, and it is
the reason sealing is pooled and hourly rather than per agent and per block.

OpenTimestamps is free and could replace seals for proofs of existence [@todd-ots-2016]. It does
not give non-equivocation: a gateway could timestamp two histories. Escapement uses
OpenTimestamps-style aggregation only for existence proofs of individual entries, and single-use
seals for the one-history property.

### What a seal proves, and what it does not

A seal proves that a log head existed by a given block, and that the gateway has published one
history. It does not prove that the log is complete: a gateway can leave actions out, and an agent
can act around its gateway. It does not prove that any action was good. An anchored hash proves
existence and order, not behaviour, as Allen et al. warn about every scheme of this kind
[@allen2026survey].

A seal also does not prove that anyone saw what it commits to. Kelsey and Kohno's herding attack
shows that committing to a hash in advance and choosing the message later is possible under
some constructions [@kelsey2006]; more simply, a gateway can commit to a head and never show the
entries. So the rule is that guardians must receive every entry's content when it is committed,
and an entry whose content a guardian has not received counts as missing. A release (above) can
only be signed for content the guardians hold.

Seals are only as final as Bitcoin's history, and that history rests on mining pools not
colluding. The largest pool mined [27.8%](numbers.md#pool-largest-share) of blocks over the
trailing year and the two largest [46.1%](numbers.md#pool-top2-share) together
[@mempool-pools]. By Nakamoto's own formula for an attacker catching up from behind
[@nakamoto2008], the chance that the largest pool alone ever rewrites a block six deep is
[8.9%](numbers.md#reorg-p-largest-6), and it needs [19 blocks](numbers.md#depth-for-target-largest) before that
chance is under [0.1%](numbers.md#reorg-risk-target). For the two largest, colluding, the chance is
[82%](numbers.md#reorg-p-top2-6) at six blocks and [12.79%](numbers.md#reorg-p-top2-144) at a
Tier 3 depth, and it takes [552 blocks](numbers.md#depth-for-target-top2), about
[3.8 days](numbers.md#depth-for-target-top2-days), to fall under the target. The formula treats a pool as a single miner, which it is
not (the hashers behind a pool can leave it), and it ignores what such an attack would cost the
pools in reputation and in the value of their coins. But it says plainly that Escapement's record
is as safe as Bitcoin's pools are independent. Escapement treats a seal as settled after
[19 blocks](numbers.md#depth-for-target-largest) and treats deeper collusion as a risk it shares
with every other use of Bitcoin.

### Model weights

A principal can commit the hash of the weights it deploys in the charter, and seal it. The IETF
draft that defines a Bitcoin-anchored profile for transparency services uses exactly this example:
an AI lab registering model weights and safety evaluations so a regulator can rule out backdating
[@fassbender2026], and Sigstore already signs models into a transparency log [@sigstore2025]. The
commitment proves which weights the principal said it deployed and when. It cannot prove which
weights are running, unless the inference provider attests to that, which is outside Bitcoin.

### Keeping up with the chain

Every check above needs the verifier to know the chain. Headers are
[80 bytes](numbers.md#header-bytes) each, so a device that keeps its own view of the chain reads
[4.2 MB](numbers.md#headers-mb-per-year) of headers a year. That is small enough for a gateway, a
phone or a chip's guarantee processor.

## Relying parties: where it is enforced

Bitcoin enforces only spends of bitcoin. Everything else in Escapement is enforced by relying
parties choosing to check, and that is the design's main weakness and its main dependency.

A relying party that deals with a chartered agent receives a bundle and checks it:

1. the charter, signed from the principal's address;
2. a current lease: its signature, its anchor block in the best chain, and the tip below expiry;
3. the bonds: their outputs unspent, their size, and their age against the season;
4. for a Tier 2 or 3 action, the commitment's seal and the release, with the gap of at least N
   blocks between them;
5. the gateway's latest seal, and that the log head the agent presents extends it.

None of this needs a trusted server: every check is a signature, a Merkle proof or a header, and
each can be done by the relying party alone.

Why would a relying party check? Because it bears risk from the agent's actions, and the bundle
tells it who answers for them (the principal), how much is at stake (the bonds) and whether anyone
can stop the action (the ladder). Three forces could make that matter: liability, where a service
that dealt with an unbounded agent shares the blame; insurance, where cover for AI agents is
already being written [@fortune2025aiuc]; and regulation, where the largest model developers
already have reporting duties [@euaiact2024art51; @sb53gov2025]. None of them requires Escapement
today. Adoption is the unsolved problem.

The most natural place to start is paid APIs. L402 services already sell access for Lightning
payments using macaroons [@l402-readme], and macaroons were designed to carry caveats, including
caveats that a third party must discharge [@birgisson2014]. An L402 service could add one caveat,
"a valid Escapement lease for this agent", and serve only chartered agents. That is a small change
at one relying party, and it would test whether anyone wants the check.

## Compute: Bitcoin as the clock for chip licences

The hardware-governance literature proposes AI chips that run only under licences that must be
renewed, and it names a reliable clock as a hard requirement. Flexible hardware-enabled guarantees
give the chip's guarantee processor a real-time clock for time-dependent rules, and the second
flexHEG report mentions a public blockchain hash as a witness that a delay has passed
[@petrie2025flexheg2]. Buterin proposes chips that run only with fresh signatures from several
parties once a week, optionally with proof that the signatures were published on a blockchain
[@buterin2025dacc]. Hardware-enabled mechanisms are designed to make licences expire
[@ogara2025hem; @aarne2024].

Escapement's lease rule applies directly. A licence renewal for period k names the hash of a block
at height `h_k`; the chip accepts it only with a header chain from its last accepted licence
block that has valid proof of work and reaches `h_k`. Because future block hashes are unknown, a
licensor, a coerced licensor, or a thief with the licensor's key cannot issue next year's licences
today. Because headers need work, an attacker who wants to feed a chip a fake day of headers must
mine a day's worth of blocks at the network's difficulty. The chip's own monotonic counter enforces
the other end: it stops when its licence period is over, whether or not it has seen new headers.
Bitcoin supplies "not before"; the chip supplies "not after". This is a close application of the
proposals it credits, and it is marked that way in the novelty table.

Proof of work as a meter of AI compute is a different idea, and the survey rejects it. SHA-256
work says nothing about matrix multiplication, and the two compete for the same power: Bitcoin
mining drew about [15.8 GW](numbers.md#bitcoin-gw-survey) on Cambridge's survey estimate
[@cambridge-2025], data centres about [55 GW](numbers.md#datacentre-gw-2025) on average in 2025
[@iea-2026], and the largest listed miners are converting capacity to AI hosting [@ccaf2026]. What
proof of work does provide is the cost of faking the clock, which the next section prices.

## The clock under attack

An adversary who wants a delay to end early must make blocks come faster. Below a hashrate
majority, that means adding hashrate. Doubling the network's
[1,052 EH/s](numbers.md#hashrate-eh) [@mempool-hashrate] takes hardware drawing
[18.4 GW](numbers.md#clock-2x-power-gw) at a current miner's [17.5 J/TH](numbers.md#asic-efficiency-j-th)
[@hri-s21] and costing about [7.4 billion USD](numbers.md#clock-2x-hardware-busd) at reported street
prices [@ct-bitmain]. It halves block time only until the next difficulty adjustment, gaining
[7 days](numbers.md#clock-2x-days-gained) once, after which difficulty catches up. To shrink a Tier
3 wait from [24 hours](numbers.md#tier3-delay-mean-h) to
[1 hours](numbers.md#tier3-compress-target-h) needs [24 x](numbers.md#tier3-compress-factor) the
network's hashrate, about [423 GW](numbers.md#tier3-compress-power-gw) of added power, or
[8 x](numbers.md#tier3-compress-vs-datacentres) the average draw of every data centre on Earth in
2025. Against fast cognition, block height is a strong clock. Against capital, it is a clock that
costs gigawatts to speed up.

Two qualifications. A majority of existing hashrate can do far more: the timewarp bug lets a
majority lower difficulty until blocks come at several a second, after about a month of visible
setup [@optech-timewarp; @bip54]. The fix is specified in BIP-54 and not active [@bip54]. That is
why relying parties should count median time past as well as blocks. And a block-counted delay is
random; the Tier 2 tail above is the cost of using a Poisson clock.

The other attacks on the clock are on its readers, not on the chain: feeding a relying party stale
headers, or censoring a veto. Pools have left sanctioned transactions out of blocks
[@b10c-ofac], and a pool that censors a Cancel or a seal for long enough could make a veto miss its
window. Escapement's off-chain vetoes are guardian refusals that need no confirmation, and a missed
seal epoch is itself visible on chain; on-chain Cancels are the case that needs fee headroom.

## Threats, and which part answers each

| Threat | What the agent does | What answers it | What remains |
|---|---|---|---|
| Overspending | spends faster or more than intended | the allowance (no detection needed) | at most [200,000 sats](numbers.md#bond-coverage) at the reference terms |
| Irreversible action | transfers, deploys, spawns, changes its charter | the ladder: delay, one-guardian veto, quorum release | a principal who puts dangerous actions in low tiers |
| Persuading overseers | social-engineers guardians | quorum release; guardians independent; the delay gives others time | a captured quorum |
| Key theft | the agent key leaks | lease and allowance bound the damage; revocation | one lease and allowance |
| Abandonment | humans vanish | lease lapses; allowance stops; Liana-style recovery | nothing beyond the last allowance |
| Two histories | the gateway shows different records to different parties | single-use seals; equivocation bond for receipts between seals | omissions; deep collusion by pools |
| Swarm | many chartered agents act together | bonds per charter; seasoning; Tier 3 spawn | an adversary with capital and a month's notice |
| Outside money | earns, borrows or steals bitcoin outside the scheme | relying parties that require a charter refuse | everything that does not pass through such a relying party |
| Off-scheme action | acts through credentials, exploits or borrowed compute | nothing in Escapement | the 2026 incident's whole attack surface |
| Speeding the clock | adds hashrate | difficulty and its cost: [18.4 GW](numbers.md#clock-2x-power-gw) to double the rate for a week | a colluding majority using timewarp, until BIP-54 activates |
| Malicious principal | the principal wants the harm | nothing; Escapement binds agents to principals | everything |

Three further limits apply across the board. **Privacy:** bonds and seals are public, so a
principal's backing coins and a gateway's activity cadence are visible; Taproot hides unused script
paths [@bip341], and contents stay off chain. **Quantum risk:** the keys are Schnorr keys, and
long-lived bonds are exposed if large quantum computers arrive; the proposed P2MR output type is a
draft [@bip360]. **Custody:** every key is a target, and the guardians' keys most of all.

## What it does not do

Escapement does not make an AI safe. It does not see inside a model, constrain what the model
learns, or prevent an AI from acquiring money elsewhere. It does not touch actions that pass
through no relying party that checks. The 2026 incident, the most serious multi-agent event on
record at the time of writing, ran on credentials, exploits and borrowed compute, and nothing in
it went through a check Escapement would have added [@metr2026hf; @openai2026hf]. AI agents'
capabilities are also growing quickly: METR's estimate is that task time horizons double about
every [3.6 months](numbers.md#metr-doubling-months) [@metr2026q4]. The design assumes the agent is
smarter and faster than its overseers. It does not assume it is weaker.

What it does is narrower. For an agent its principal wants bounded, Escapement gives a budget that
refills only on a human's signature, a set of delays on irreversible actions that no participant
can shorten, a veto any one guardian can use, liability that lands on a named human's coins, and a
record no single party can rewrite. For a service that wants to deal only with bounded agents, it
gives a check that needs no trusted server.

## Parameters

Every parameter below is a design choice, set in `data/inputs.toml` and varied with
`python3 model/escapement.py --set ID=VALUE`.

| Parameter | Reference value | Why |
|---|---|---|
| Tier 2 wait | [6 blocks](numbers.md#tier2-delay-blocks), [60 minutes](numbers.md#tier2-delay-mean-min) mean | the one-hour delay of the Async Control study [@stickland2025] |
| Tier 3 wait | [144 blocks](numbers.md#tier3-delay-blocks), [24 hours](numbers.md#tier3-delay-mean-h) mean | a full day for a human to look; the same length as the CSV fallback in a published Bitcoin agent-wallet design [@laz1m0v2026] |
| Lease | [144 blocks](numbers.md#lease-blocks) | a daily human renewal; lapse within a day |
| Season | [4,032 blocks](numbers.md#season-blocks), [28 days](numbers.md#season-days) | two difficulty periods; long enough that a swarm must be planned |
| Seal epoch | [6 blocks](numbers.md#seal-epoch-blocks) | matches the Tier 2 wait, so a Tier 2 commitment is sealed before its release |
| Allowance | [100,000 sats](numbers.md#allowance-per-lease) a lease | an example; set per agent |
| Coverage ratio | [1.0](numbers.md#coverage-ratio) | the bond covers what can be spent before a stop |

## Deployment path

**Today, with no consensus change.** The vault (pre-signed Unvault and Cancel, a co-signer), the
lease and allowance (a signed renewal, an NWC or on-chain budget), the bonds (timelocked outputs;
EOTS-style equivocation keys with pre-signed slashing), single-use seals and seal pools, and the
relying-party bundle all work under current rules. The trusted parts are the co-signer (for
destinations and amounts), the guardians (for vetoes and releases), the adjudicator (for harm
claims), and each relying party's own view of the chain.

**With covenants.** CTV would let the vault commit its destination in script and drop the
co-signer from that role [@bip119]; a vault opcode with partial withdrawals would remove the fixed
denominations [@bip345]. An open letter in 2025 asked Bitcoin Core contributors to prioritise CTV
and CSFS [@optech-2025-07-04], and nothing has been scheduled since. Escapement does not wait for
them.

**First steps.** A signet prototype of the vault, lease and seal; a gateway for one agent framework
that implements the ladder; and one L402 service that adds the lease caveat. Each is small, and
each tests a different part of the claim.

## What would show it is wrong

The design makes claims that can fail, and these are the experiments that would test them.

1. **Do block-counted delays help overseers?** Repeat the Async Control setting with Tier 2 and
   Tier 3 waits drawn from the real block-time distribution rather than fixed delays, and with
   monitors that must veto rather than review. If safety does not rise with the wait, the ladder
   is cost without benefit.
2. **How much of an agent's irreversible action passes through relying parties?** Instrument
   agents on realistic long tasks and count which irreversible actions go through a service that
   could check a charter. If the answer is small, as the 2026 incident suggests it may be,
   Escapement's coverage is small.
3. **Can guardians keep up?** Measure how long human and automated guardians take to review Tier 2
   and Tier 3 commitments, and how often agents persuade them. If guardians rubber-stamp, the
   quorum is decoration.
4. **How often do agents equivocate by accident?** Run gateways under restarts and failover and
   count double-signed slots with and without slashing protection.
5. **Will anyone check?** Offer the lease caveat at a paid API and see whether principals charter
   their agents to use it.

If the first two fail, the thesis fails with them: a meter on commitments that are not where the
harm happens, or a delay that overseers cannot use, is not a safety mechanism.
