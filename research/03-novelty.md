# What is new, and what is not

Every part of the design in [02-design.md](02-design.md), set against the closest prior work we
found, with a verdict. The verdicts are:

- **Prior work**: the same idea exists, for this purpose or close to it. Escapement uses it and
  credits it.
- **Application**: the mechanism exists for another purpose, or on another chain; Escapement
  applies it to bounding AI agents on Bitcoin. The contribution is the mapping and its threat
  model, not the mechanism.
- **New, as far as we found**: we found no prior statement of it. That is a claim about our search,
  not about the world. The searches are listed so anyone can repeat and extend them.

The searches were run on 2026-11-25 and 2026-11-26, on general web search and in the venues the
results led to (arXiv, Delving Bitcoin, Ethereum Magicians, the BIP and ERC indexes, vendor
documentation). The raw record, with the queries and what each found, is in
`research/notes/07-prior-art-novelty.md` and the notes it cross-references.

## The summary

The building blocks are almost all published. Timelocks, multisig, pre-signed vaults, fidelity
bonds, extractable one-time signatures, single-use seals, transparency logs, spending allowances
and expiring delegations all exist, many of them for AI agents already, though more often on
Ethereum than on Bitcoin. What we did not find is:

1. the argument that Bitcoin's value to AI safety is a meter on the **rate of irreversible
   commitment**, on a clock the metered agent cannot speed up, rather than a limit on capability;
2. **block height as the unit of an agent's authority**, with a lease that names a block hash so it
   cannot be signed early, checked by any relying party against headers;
3. a **delay on off-chain agent actions made checkable by two chain anchors** (a seal at the start,
   a future block hash in the release at the end), combined with a one-veto, quorum-release rule;
4. **equivocation slashing applied to an agent gateway's receipts**, and seasoned bonds used as
   swarm friction for agents.

No academic paper we found proposes Bitcoin specifically as an AI safety or limitation mechanism.
The closest framings are an essay that calls Bitcoin "the first form of AI time" with no safety
argument [@gilliam2025], and the older "Bitcoin is time" essay [@gigi2021]. The strongest
counter-thesis, that giving agents crypto creates new harms, is in the literature and is credited
throughout [@marino2025; @allen2026survey].

## The table

| Part of the design | Closest prior work | Verdict |
|---|---|---|
| **The thesis**: meter the rate of irreversible commitment on a clock the agent cannot speed up; do not try to cap capability | Delay is the non-substitutable control on irreversible actions [@nagaraj2026]; "a budget, not a token", a ceiling that refills [@malhotra2026]; delays let asynchronous monitors catch attacks [@stickland2025]; govern a complex system with a simple, dumb one [@buterin2016]; Bitcoin as time [@gigi2021; @gilliam2025] | **New as a combined argument, as far as we found.** Each half is credited above |
| **Charter**: a delegation signed from the principal's address, naming agent key, scopes, bond, guardians | OrangeCheck Agent: BIP-322 delegation with scopes, caps, bond reference, revocation [@agent-spec; @agent-security]; authenticated delegation for AI agents [@south2025]; wallet permission requests with expiry [@EIP-7715] | **Prior work.** Escapement's charter is that delegation extended with a lease, a ladder and a gateway seal |
| **Ladder**: tiers by irreversibility; unknown actions go to the top; one guardian can veto, a quorum must release | Revault's managers and stakeholders, where any stakeholder's watchtower can cancel [@revault-intro; @revault-tx]; Safe's human approval for agent transactions [@Safe-HumanApproval]; Nunchuk's policy co-signer with signing delays [@nunchuk-blog]; irreversible actions need a second actor [@malhotra2026]; trusted monitoring in AI control [@greenblatt2023] | **Application.** The veto-versus-release asymmetry is Revault's; tiering by irreversibility is standard practice. The Tier 3 spawn rule is below |
| **On-chain vault**: pre-signed Unvault and Cancel, CSV wait, co-signer binds destination | Revault [@revault-tx]; OP_VAULT's "delay, then any destination, except recovery" [@bip345]; a TEE agent wallet with a 144-block CSV fallback to a human multisig [@laz1m0v2026] | **Prior work** (the vault), **application** (the agent as the party that triggers and the guardians as the party that cancels) |
| **Two-anchor off-chain delay**: the commitment sealed at `h0`, the release signing the hash of block `h1 >= h0 + N`, checked by the relying party | Linked timestamps for "no later than" [@haber1991; @todd-ots-2016]; a recent block hash in the bytes for "no earlier than", combined with an anchor to bracket a file's creation [@solomon-bracket]; a blockchain hash as a delay witness for chip licences [@petrie2025flexheg2]; freshness "as of the anchored block" for agent authority checks [@borthwick-insumer] | **Application.** The bracket is known for proving when a file was made. Using it to make a veto window over an off-chain agent action checkable by any relying party was **not found** |
| **Lease in block height**, naming a block hash; relying parties check expiry against headers | Leases in distributed systems [@gray1989]; ERC-8370's `requireLease`, a guardian-renewed dead-man's switch for agent mandates on Ethereum [@erc8370]; weekly multi-party signatures for chips [@buterin2025dacc]; expiring, rotated delegation tokens [@south2025] | **Application.** Expiring, human-renewed agent authority exists on Ethereum and in hardware proposals. A block-height lease on Bitcoin, bound to a block hash, **not found** |
| **Allowance per lease**: a refilling budget that is the only cap needing no detection; lapse is the default | Lightning Labs' per-request and total caps (vendor) [@lightninglabs2026]; NWC budgets with a renewal period [@nwc-08; @Alby-AppConnections]; Nunchuk's daily limit [@nunchuk-blog]; Safe's allowance module [@safeallowance]; ERC-8370's lease [@erc8370] | **Prior work.** Escapement keys the refill to the lease |
| **Coverage bond** from the principal's own coins, released to claims by a named adjudicator | Verifiable agent insurance with provider escrow [@hua2026vai]; staked agent tokens slashed through oracles [@chaffer2025abt]; mandatory insurance for agents [@chaffer2024ethos]; commercial agent insurance [@fortune2025aiuc]; liability on users as the incentive-compatible choice [@buterin2025dacc]; OrangeCheck Pledge's own-address bond that refuses to slash [@pledge-spec; @pledge-why] | **Prior work.** The only difference is whose coins and which chain |
| **Equivocation bond** on a gateway's signed receipts, slashed with no adjudicator | Accountable assertions: equivocation on a public log costs the equivocator bitcoins [@ruffing2015]; Babylon's extractable one-time signatures for Bitcoin staking [@babylon2023; @babylon-staking-script]; slashing on signed contradictions in supply chains [@cochinescu2026] | **Application.** The primitive is Ruffing, Kate and Schroeder's and Babylon's; its use on an AI agent gateway's receipts **not found** |
| **Seasoning**: a bond backs Tier 2 and 3 authority only after a season locked | JoinMarket fidelity bonds, timelocked coins as costly identity [@belcher-2019; @bip46]; OrangeCheck Attest's coin-age measurement [@attest-spec; @attest-bond]; time-bound human challenges [@maleki2026hco] | **Application.** The mechanism is Belcher's; its use as swarm friction for AI agents **not found** |
| **Tier 3 spawn rule**: a chartered agent spawns another only through its own charter, bond and lease, after a day's wait and a human | Sub-delegation that strictly narrows scope and time, without its own bond [@agent-spec]; delegation scope attenuation and "at most one root credential per human principal" for agents [@reid2026]; per-principal identity to make sybils visible [@adler2024phc] | **Application.** Binding agents to principals is proposed; making spawning a delayed, bonded, human-approved action **not found** in our search |
| **Gateway log, single-use-seal chain, seal pools** | Certificate Transparency [@rfc6962; @rfc9162]; single-use seals [@todd-2017]; non-equivocation via Bitcoin [@catena-2017]; a per-identity Merkle map [@melara2015]; a Bitcoin-anchored profile for transparency services, with AI model weights as its example [@fassbender2026]; model signing into a transparency log [@sigstore2025]; Blocklore's editions and OC Stamp [@blocklore-architecture; @stamp-spec] | **Prior work** (anchoring and non-equivocation); **application** (an AI agent gateway's action log as the thing sealed) |
| **Relying-party bundle**, and an L402 caveat requiring a lease | L402 [@l402-readme]; macaroon caveats, including third-party caveats [@birgisson2014]; signed verdicts on agent authority anchored by block height (vendor) [@borthwick-insumer]; oversight layers in agent infrastructure [@chan2025infra] | **Application** |
| **Bitcoin as the clock for chip licences**: a renewal names a block hash, the chip checks headers, its counter enforces expiry | Weekly multi-party signatures, optionally proven published on a blockchain [@buterin2025dacc]; a blockchain hash as a delay witness [@petrie2025flexheg2]; periodically renewed licences and secure clocks [@aarne2024; @ogara2025hem] | **Application, close to existing.** Block height as the chip's trusted lower bound on time **not found** as such |
| **Not used: blockspace as a global rate limit** | Per-agent on-chain spending and rate limits [@allen2026survey]; proof of work to make crawling costly [@anubis2025]; "proof of work proves not to work" against spam [@laurie-clayton-2004] | **Rejected** in the survey: a fee auction throttles the poor, not the rich, and one anchor can commit to unlimited actions |
| **Not used: proof of work as a meter of AI compute** | Compute governance canon, with no role for proof of work [@sastry2024]; a speculative post on a simulation-work coin [@lw-simdeterrent]; miners converting to AI hosting [@ccaf2026] | **Rejected** in the survey: SHA-256 work measures nothing about AI compute. Its role here is only the cost of faking the clock |

## Searches behind the "not found" verdicts

These are the queries whose results did not contain the idea. Each verdict above rests on these
and on the per-track searches in the notes.

- **Thesis:** "bitcoin "clock" AI cannot speed up time irreversible commitment AI agents essay";
  ""irreversible" commitments rate AI agents safety metering not capability limiting time delay
  argument"; "bitcoin as AI safety mechanism paper "AI alignment" proof of work limit AI".
- **Lease in block height:** "block height expiry AI agent delegation credential bitcoin freshness
  renew"; "AI agent wallet allowance expires dead man's switch human renew authority".
- **Two-anchor delay:** "delay window proof "block hash" "not before" timestamp both ends veto
  release off-chain action AI agent bitcoin"; ""time-lock" "human veto" AI agent actions verifiable
  delay relying party checks bitcoin timestamp release signature". The first found the
  bracketing technique for files [@solomon-bracket]; neither found it applied to a veto window.
- **Vault for agent actions:** "AI agents timelock vault human veto delay irreversible
  transactions"; "bitcoin AI safety timelock "AI agents" covenant vault delving bitcoin".
- **Equivocation bond:** "extractable one-time signatures AI agents commitments equivocation
  Bitcoin"; ""AI agent" bond slashing equivocation signed commitments accountability
  cryptographic".
- **Seasoning:** "AI agents sybil swarm bonds coin age timelocked stake "proof of personhood"
  agents delegation"; "timelocked bitcoin bond AI agent sybil resistance swarm".
- **Spawn rule:** "AI agent spawning sub-agents requires human approval delay bond each sub-agent
  delegation sybil swarm limit". It found depth and breadth limits on spawning and per-principal
  credentials [@reid2026], but no bonded, delayed, human-approved spawn.
- **Chip clock:** "hardware-enabled mechanisms AI chips licence renewal blockchain time source";
  "AI chip licence renewal bitcoin block height clock compute governance"; keyword searches for
  bitcoin, blockchain and clock in the hardware-governance reports cited above.

## What the paper may and may not claim

It may say that Escapement assembles known Bitcoin primitives (timelocks, multisig, pre-signed
vaults, fidelity bonds, extractable one-time signatures, single-use seals) into one argument that,
to our knowledge, has not been made: that Bitcoin's value to AI safety is a meter on the rate of
irreversible commitment that the metered agent cannot speed up, not a limit on what the agent can
think or compute. It may name the parts marked "not found" as its contributions, each with its
closest prior work beside it.

It may not claim any primitive, any of the parts marked prior work, or any evidence that the design
makes an AI system safer. Nothing has been built or tested.
