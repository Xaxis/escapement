# Bitcoin's real limits (throughput, fees, Lightning, privacy, custody, mining, quantum) and proof-of-work versus AI compute

Research notes for Escapement, state as of 2026-11-26 (all access dates 2026-11-26 unless stated). Labels used on every number: **measured** (independent measurement or dataset), **vendor** (claim by an interested party: company, fund, exchange, analytics firm selling the data, or a party to a deal), **derived** (my arithmetic, inputs shown), **news** (secondary reporting of someone else's figure), **spec** (protocol rule, BIP, release notes). Source keys refer to the YAML block at the end. Live API pulls were made from mempool.space and api.blockchain.info on 2026-11-26 between roughly 06:30 and 07:00 local time; the chain tip was height 977,695.

## Model-ready numbers

BTC price used for USD conversions: **$60,000** (derived round figure: IBIT holdings file implies $59,357 on 2026-11-24 = $44,497,078,820 / 749,654.27 BTC [ishares-ibit-csv]; bitcointreasuries implies $60,365 on 2026-11-26 = $51,389M / 851,305 BTC [bitcointreasuries]). Historical fee episodes below are converted at this November 2026 price, not at the price of the day.

| Quantity | Value | Unit | Date | Label | Source key |
|---|---|---|---|---|---|
| Block weight limit | 4,000,000 | WU | BIP-141 (deployed 2017) | spec | bip141 |
| Max virtual size per block | 1,000,000 | vB | derived 4,000,000 / 4 | derived | bip141 |
| Blocks found, trailing 365 days | 52,413 (143.6 per day) | blocks | 2025-11-26 to 2026-11-26 | measured | mempool-pools |
| 1-in, 2-out P2WPKH tx size | 140.75 (calculator, 73-byte sig worst case); about 140.5 typical | vB | Optech calculator | derived | optech-calc |
| 1-in, 2-out P2TR key-path tx size | 154.25 (calculator); 154.0 with 64-byte SIGHASH_DEFAULT sig | vB | Optech calculator | derived | optech-calc |
| OP_RETURN output carrying 32-byte commitment | 43 (8 value + 1 len + 1 OP_RETURN + 1 PUSH32 + 32) | vB | structure from calculator | derived | optech-calc |
| Anchor tx: 1 P2TR in, 1 P2TR change out, 1 OP_RETURN(32 B) | 154.0 (10.5 + 57.5 + 43 + 43); 154.25 with calculator input | vB | | derived | optech-calc |
| Same anchor with P2WPKH in and change | 152.75 (10.5 + 68.25 + 31 + 43) | vB | | derived | optech-calc |
| Theoretical max anchors per full block | about 6,490 (1,000,000 / 154) | tx | | derived | bip141, optech-calc |
| Theoretical max anchors per day | about 935,000 (6,490 x 144) | tx/day | | derived | |
| Theoretical max 1-in-2-out P2WPKH per day | about 1.02 million (1,000,000 / 140.75 x 144) | tx/day | | derived | |
| Confirmed tx per day, 2024 mean (max) | 525,269 (927,010 on 2024-04-23) | tx/day | 2024 | measured | btccom-ntx |
| Confirmed tx per day, 2025 mean | 420,660 | tx/day | 2025 | measured | btccom-ntx |
| Confirmed tx per day, 2026 mean (max) | 592,356 (963,618 on 2026-11-15) | tx/day | 2026-01-01 to 2026-11-25 | measured | btccom-ntx |
| Mean tx vsize, last 144 blocks | 257 | vB | 2026-11-25/26 | measured, derived | mempool-blocks |
| Mean block weight, last 30 days | 3,916,570 (98% of limit) | WU | 2026-10-27 to 2026-11-26 | measured | mempool-blocks |
| Runes-claim share of blockspace | about 35% | % of block space | July 2026 | vendor (Bitquery analysis) | bitquery-blocks |
| Median of per-block median fee rate | 1 | sat/vB | last 144 blocks to 2026-11-26 | measured | mempool-blocks |
| mempool.space recommended fees | fastest 2, half-hour 1, hour 1, economy 1, minimum 1 | sat/vB | 2026-11-26 | measured | mempool-fees |
| Default min relay fee (Bitcoin Core) | 0.1 | sat/vB | Core 30.0, 2025-10-10 | spec | core-30 |
| Mempool backlog | 71,445 tx, 31.2 M vB (about 31 blocks), almost all at 0.10 to 0.12 sat/vB | | 2026-11-26 | measured | mempool-fees |
| Daily-average median fee peak, BRC-20 episode | 435 | sat/vB | 2023-05-08 | measured | mempool-feerates |
| Daily-average median fee peak, inscriptions episode | 344 | sat/vB | 2023-12-16 | measured | mempool-feerates |
| Halving block 840,000: median fee; total fees | 200 sat/vB; 37.63 BTC (vs 3.125 BTC subsidy) | | 2024-04-20 00:09 UTC | measured | mempool-block840000 |
| Daily-average median fee, halving day | 861 | sat/vB | 2024-04-20 | measured | mempool-feerates |
| Annual median of daily-average median fee | 2023: 15; 2024: 12; 2025: 2; 2026: 1 | sat/vB | | measured, derived | mempool-feerates |
| Anchor cost (154 vB) at 0.1 / 1 / 3 / 12 sat/vB | 15.4 / 154 / 462 / 1,848 sats ($0.009 / $0.09 / $0.28 / $1.11) | sats, USD | | derived | |
| Anchor cost at 50 / 200 / 435 / 861 sat/vB | 7,700 / 30,800 / 66,990 / 132,594 sats ($4.62 / $18.48 / $40.19 / $79.56) | sats, USD | | derived | |
| One anchor every block for a year (52,413) at 1 / 50 / 200 sat/vB | 0.081 / 4.04 / 16.1 BTC ($4.8k / $242k / $969k) | BTC/yr | | derived | |
| Block subsidy | 3.125 BTC (block 840,000: reward 40.75061499 minus fees 37.62561499) | BTC/block | since 2024-04-20 | derived | mempool-block840000 |
| Fees as share of block rewards | 0.71% (week to 2026-11-16); 0.47% (2.13 BTC fees vs 450 BTC subsidy, last 144 blocks) | % | Nov 2026 | vendor; derived | hri-20261116; mempool-blocks |
| Hashprice | $30.45 (0.00046839 BTC) | per PH/s per day | 2026-11-16 | vendor | hri-20261116 |
| Network hashrate (mempool estimate) | 1,052 (current), 1,041 (3-day) | EH/s | 2026-11-26 | measured | mempool-hashrate |
| Highest daily hashrate estimate | 1,306 | EH/s | 2025-10-25 | measured | mempool-hashrate |
| First intraday 1 ZH/s | about 1,025 EH/s | EH/s | 2025-04-04 (Glassnode) | news | coindesk-1zh, forklog-1zh |
| First 7-sample average at or above 1 ZH/s | 1,003 | EH/s | window ending 2025-08-31 | derived from measured | mempool-hashrate |
| Difficulty | 134.82 T (last adjustment -9.13%); next estimated +8.98% at height 977,760 | | 2026-11-14; est. 2026-11-27 | measured | mempool-difficulty, hri-20261116 |
| Pool shares, trailing year | Foundry 27.8, AntPool 18.4, F2Pool 13.3, ViaBTC 9.4, SpiderPool 8.5, MARA 5.1 | % of blocks | to 2026-11-26 | measured | mempool-pools |
| Top-2 / top-3 / top-5 pool share | 1 y: 46.1 / 59.4 / 77.4; 1 w: 46.0 / 62.3 / 78.2 | % of blocks | to 2026-11-26 | derived from measured | mempool-pools |
| "AntPool and friends" (shared templates) | about 40% of hashrate | % | 2024 | measured (independent researcher) | b10c-2025 |
| Template producers mining over 95% of blocks | 6 | entities | to April 2025 | measured | b10c-2025 |
| Notional 1-hour 51% attack rental cost; NiceHash-able share | $1,843,332; 0% | USD/hour; % | 2026-11-26 | vendor-neutral estimator, theoretical | crypto51 |
| P(attacker catches up) Nakamoto model, 6 confirmations | q=0.10: 0.02%; q=0.278 (largest pool): 8.9%; q=0.46 (top two): 82% | probability | | derived (Nakamoto 2008 formula) | nakamoto-2008 |
| Lightning public capacity | 3,203 BTC; 28,939 channels; 15,899 nodes | | 2026-11-04 | measured (aggregator of mempool.emzy.de) | coinpaprika-ln |
| Lightning capacity peak | 5,851 BTC (2025-12-28, coinpaprika); 5,756 BTC (2025-12-24, mempool.space) | BTC | Dec 2025 | measured | coinpaprika-ln, mempool-ln |
| LND share of public nodes; of capacity | 80% (84% incl. one fleet); 84% | % | 2026 | measured (preprint) | kumar-2026 |
| Non-custodial : custodial Lightning users | 1 : 8 | ratio | Sept 2023 | vendor (River) | river-ln-2023 |
| River Lightning payment success | 99.7% of 308k payments | % | Aug 2023 | vendor | river-ln-2023 |
| IBIT bitcoin held | 749,654.27 | BTC | 2026-11-24 | vendor (fund disclosure) | ishares-ibit-csv |
| Strategy Inc. bitcoin held | 851,305 (aggregator, 2026-11-26); 850,849 (8-K, as of 2026-11-15) | BTC | | vendor | bitcointreasuries, theblock-mstr |
| Public companies / private companies / governments / ETFs and exchanges / DeFi and other | 1,239,002 / 201,884 / 645,639 / 1,589,940 / 376,202 | BTC | 2026-11-26 | aggregator (vendor) | bitcointreasuries |
| Largest government holders | US 328,372; China 190,000; UK 61,245 | BTC | 2026-11-26 | aggregator (vendor) | bitcointreasuries-gov |
| Exchange reserves | 2.85 million | BTC | 2026-11-18 | analyst (method unstated) | adler-20261118 |
| Supply in circulation | 20.11 million (check: 19,687,500 + 137,696 x 3.125 = 20,117,800) | BTC | Nov 2026 | aggregator; derived | coinpaprika-ln |
| Quantum-exposed supply at rest | 6.04 M BTC (30.2%): structural 1.92 M, operational 4.12 M | BTC | 2026-05-20 | vendor (Glassnode) | glassnode-quantum |
| Shor on 256-bit ECDLP | under 1,200 logical qubits and under 90 M Toffoli (or under 1,450 and under 70 M); under 500k physical qubits, minutes | | 2026-03-30 | preprint | babbush-2026 |
| Bitcoin electricity, survey-based | 138 TWh/yr (about 0.5% of world), 39.8 Mt CO2e | TWh | report 2025-04-28 | measured (survey of 48% of hashrate) | cambridge-2025 |
| Bitcoin electricity, annualised | about 190 TWh/yr (preliminary) | TWh | Dec 2025 rate, reported 2026-07-26 | news of preliminary academic figure | cryptonews-ccaf |
| Implied average Bitcoin power draw | 21.7 GW (190 TWh / 8,760 h); implies about 20.6 J/TH at 1,052 EH/s | GW | | derived | |
| Data-centre electricity | 415 TWh (2024, 1.5% of world); 485 TWh (2025, +17%); 950 TWh (2030 projection) | TWh | IEA 2025, IEA 2026 | measured/modelled (IEA) | iea-2025, iea-2026 |
| AI-focused data-centre electricity growth | +50% in 2025 | % | 2025 | IEA | iea-2026 |
| Bitcoin vs data-centre electricity | about 39% (190 / 485) | ratio | 2025 | derived | |
| S21 efficiency | 17.5 J/TH (200 TH/s, 3,500 W) | J/TH | spec sheet | vendor spec | hri-s21 |
| ASIC street price, S21-class immersion | discounts to about $7 per TH/s | USD/TH | 2025-12-26 | news | ct-bitmain |
| Hardware to double network hashrate | $7.4 to 9.5 B at $7 to 9/TH; 18.4 GW at 17.5 J/TH | USD; GW | | derived | |
| AI hosting rent per MW of IT load | Hut 8 $1.91M/MW-yr; TeraWulf $1.85M; Cipher-Fluidstack $1.79M; Core Scientific $1.44M | USD/MW-yr | 2024 to 2025 deals | derived from vendor | hut8-pr, terawulf-pr, theblock-cipher, corz-pr |
| Mining revenue per MW (energy hashprice) | $57 to $105 per MWh = $0.50 to 0.92M per MW-yr | USD | 2026-11-16 | vendor; derived | hri-20261116 |
| Two-block reorgs (Towns list + 2026) | 2013-10-02, 2015-06-02, 2020-11-12, 2023-05-08, 2026-03-23 | dates | | measured (node operators) | bnoc-reorg |

## Throughput: block weight, transaction sizes, measured and theoretical capacity, blockspace use

### Takeaway
Bitcoin's hard ceiling is 4,000,000 weight units per block (1,000,000 vB), which caps a 154 vB OP_RETURN anchor at about 6,500 per block and about 935,000 per day; blocks are already about 98% full, but mostly with near-zero-fee data traffic (Runes claims about 35% of space in July 2026), so the cap binds on quantity only when someone is willing to outbid that traffic.

### Cited Findings
- Consensus rule: "Block weight is defined as Base size * 3 + Total size ... The new rule is block weight ≤ 4,000,000" (BIP-141, Specification; status Deployed) ([bip141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki)). One vbyte is a quarter of a weight unit, so the block limit is 1,000,000 vB (derived).
- Optech size calculator components (spec-derived): segwit overhead 10.5 vB; P2WPKH input 68.25 vB (73-byte signature at quarter weight); P2TR key-path input 57.75 vB (65-byte signature item); P2WPKH output 31 vB; P2TR output 43 vB ([optech-calc](https://bitcoinops.org/en/tools/calc-size/)). The calculator lists no OP_RETURN template; a 32-byte OP_RETURN output is 8 + 1 + (1 + 1 + 32) = 43 vB (derived from the general output structure on the same page).
- Derived sizes: 1-in-2-out P2WPKH = 10.5 + 68.25 + 2 x 31 = 140.75 vB; 1-in-2-out P2TR = 10.5 + 57.75 + 2 x 43 = 154.25 vB (154.0 with a 64-byte default-sighash Schnorr signature); anchor (P2TR in, P2TR change, OP_RETURN 32 B) = 154.0 to 154.25 vB.
- Measured blocks: last 144 blocks (heights 977,552 to 977,695, 2026-11-25 18:40 to 2026-11-26 15:23 UTC) averaged 4,620 transactions and 3,929,138 WU per block, mean 257 vB per transaction; 30-day mean block weight 3,916,570 WU ([mempool-blocks](https://mempool.space/api/v1/blocks/977695)). Trailing year: 52,413 blocks, 143.6 per day, 0.3% fewer than the 52,560 a 10-minute target implies ([mempool-pools](https://mempool.space/api/v1/mining/pools/1y)).
- Measured daily confirmed transactions (blockchain.com series, "the number of daily confirmed Bitcoin transactions"): 2023 mean 420,318 (max 731,351); 2024 mean 525,269 (max 927,010 on 2024-04-23, the Runes launch week); 2025 mean 420,660 (max 643,239); 2026 to 2026-11-25 mean 592,356 (max 963,618 on 2026-11-15); last 30 days mean 588,307 ([btccom-ntx](https://api.blockchain.info/charts/n-transactions?timespan=4years&format=json&sampled=false)). The 2026-11-15 value exceeds the widely reported 2024-04-23 record; I found no second tracker confirming it, so treat it as single-source.
- Blockspace composition (Bitquery, full-chain analysis Oct 2022 to 2026-08-18, rule-based classification, does not state bytes vs weight): payment-shaped transactions fell from 76.6% of transactions (Oct 2022) to 30.2% (Jul 2026); Runes claim transactions went from 420 (Jan 2025) to 5,831,425 (Sep 2025) to 12,347,670 (Jul 2026), "about 35%" of block space and roughly six in ten transactions in July 2026; inscriptions now "a couple of percent" of space; witness data 35.5% of space in Feb 2023 vs 21.0% in Jul 2026 ([bitquery-blocks](https://bitquery.io/investigations/what-filled-bitcoins-blocks)). Bitquery's headline panel (89% to 35% payments) conflicts with its own Table 2 (76.6% to 30.2%); the table is used here.
- Policy change that enables cheap data: Bitcoin Core 30.0 (2025-10-10) raised default `-datacarriersize` to 100,000 and permits multiple OP_RETURN outputs for relay and mining, and set default `-minrelaytxfee` and `-incrementalrelayfee` to 0.1 sat/vB, warning low-feerate transactions "are not guaranteed to propagate or confirm" unless widely adopted; `-blockmintxfee` is 0.001 sat/vB ([core-30](https://bitcoincore.org/en/releases/30.0/)).
- Counter-movement failed: BIP-110 "Reduced Data Temporary Softfork" (author Dathon Ohm) would have made new scriptPubKeys over 34 bytes invalid except OP_RETURN up to 83 bytes, and pushes/witness items over 256 bytes invalid, with mandatory bit-4 signalling at blocks 961,632 to 963,647; status now Closed ([bip110](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0110.mediawiki)). On the mailing list (2026-08-09), Jon Atack reported a chain split "yesterday during its mandatory signaling period"; Murch reported "just shy of 2.5% of blocks signaling" and that the BIP-110 chain found two blocks while Bitcoin grew by 134 ([bitcoindev-bip110](https://groups.google.com/g/bitcoindev/c/b_aV3JUtUqg)).

### Inferences
- A 32-byte OP_RETURN anchor is valid and standard under Core 30 defaults, under the old 83-byte policy, and would even have been valid under BIP-110; anchor format is not at regulatory or policy risk, but larger on-chain payloads would be.
- "Theoretical tx/day" depends entirely on assumed size: measured days (963,618) already exceed the 1-in-2-out P2TR ceiling (about 935,000) because Runes claims and similar transactions are smaller. Model capacity in vbytes, not transactions.
- Blockspace is full but cheap: the marginal buyer is low-value spam-like data willing to pay 0.1 sat/vB. An anchoring service competes only against that floor in quiet periods, and against speculative manias (BRC-20, Runes) in hot periods.
- Undercuts N7: a single anchor can commit to an unbounded Merkle tree of actions (OpenTimestamps-style), so blockspace limits the number of independent on-chain commitments, not the number of actions committed to.

### Gaps
- No independent 2026 inscription/BRC-20 byte-share series opened (Glassnode and Coinglass dashboards are paywalled or JS-only); Bitquery is a single vendor analysis.
- 963,618 tx on 2026-11-15 not cross-checked against Blockchair or Coin Metrics.

## Fees: history and cost of one anchor

### Takeaway
Fees have collapsed from hundreds of sat/vB in 2023 and 2024 manias to a median of about 1 sat/vB through 2025 and 2026, with relay now possible at 0.1 sat/vB; one 154 vB anchor costs about 154 sats ($0.09) at today's median and about 30,800 sats ($18) at halving-day congestion, a 200x spread the model must carry.

### Cited Findings
- mempool.space historical fee-rate samples (each sample averages per-block percentiles over the sampling window, roughly daily; integer-rounded) ([mempool-feerates](https://mempool.space/api/v1/mining/blocks/fee-rates/all)):
  - BRC-20 episode: 2023-05-08 11:18 UTC sample (height about 788,778) p50 435, p10 373, p90 576 sat/vB; May 2023 monthly median of samples 55.
  - Inscriptions episode: 2023-12-16 sample p50 344 (p90 423); December 2023 monthly median 126.
  - Halving and Runes launch: 2024-04-20 sample (height about 840,064) p50 861, p90 1,261 sat/vB; 2024-06-07 p50 210.
  - Lows: monthly median of samples 1 sat/vB every month from 2025-08 through 2026-11; 2025 maximum sample p50 9 (2025-02-24); 2026 maximum sample p50 3 (2026-02-05); 2026 median of samples p50 1, p90 3.
  - Annual median of sample p50: 2023 15, 2024 12, 2025 2, 2026 1 (derived).
- Halving block 840,000 (ViaBTC, 2024-04-20 00:09:27 UTC): 3,050 transactions, weight 3,993,281 WU, median fee 200 sat/vB, fee range up to 3.6 million sat/vB, total fees 3,762,561,499 sats (37.63 BTC) against a reward of 4,075,061,499 sats ([mempool-block840000](https://mempool.space/api/v1/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5)).
- Now (2026-11-26): recommended fees fastest 2, half-hour 1, hour 1, economy 1, minimum 1 sat/vB; mempool holds 71,445 transactions, 31.2 M vB, with the projected next block median about 1.10 sat/vB and subsequent projected blocks at about 0.12 sat/vB ([mempool-fees](https://mempool.space/api/v1/fees/recommended); [mempool-fees](https://mempool.space/api/v1/fees/mempool-blocks)).
- Last 144 blocks: median of per-block median fee 1 sat/vB (range 0 to 3), total fees 2.13 BTC against 450 BTC subsidy ([mempool-blocks](https://mempool.space/api/v1/blocks/977695)).
- Hashrate Index (week to 2026-11-16): about 2,892 BTC of block rewards, of which fees 20 BTC, stated as 0.71% of block rewards; fees per block 0.0229 BTC (7-day average) ([hri-20261116](https://hashrateindex.com/blog/hashrate-index-roundup-november-16-2026/)).
- Default relay floor: 0.1 sat/vB since Bitcoin Core 30.0 ([core-30](https://bitcoincore.org/en/releases/30.0/)).

### Inferences
- Cost of one anchor (154 vB) = 154 x feerate sats. Model bands: floor 0.1 sat/vB (15 sats); quiet median 1 (154 sats, $0.09); 2026 p90 3 (462 sats); 2024 median 12 (1,848 sats, $1.11); stress 50 (7,700 sats, $4.62); halving block median 200 (30,800 sats, $18.48); 2023 BRC-20 day 435 ($40); 2024 halving day 861 ($80). Use the 2023 to 2024 manias as the stress scenario, not as tail events: they recurred three times in 13 months.
- Fees are not a meaningful cost of commitment today. If Escapement wants anchoring to be costly (to rate-limit or to make commitments costly signals), fees alone do not do it in quiet markets; the cost must come from locked capital (bonds), not from blockspace.
- Fee spikes are driven by speculative token issuance, not by settlement demand; an anchor schedule that must hit a deadline (for example, per-block attestations) inherits that volatility and should be designed to tolerate delay (CPFP/RBF bumping, batching, or OpenTimestamps-style aggregation).

### Gaps
- mempool.space historical samples are integers and time-bucketed; exact per-block distributions for the May 2023 and April 2024 peaks were not pulled block by block.
- No independent long-run fee series (Coin Metrics, Glassnode) opened to cross-check.

## Lightning: capacity, nodes, reliability, custody

### Takeaway
Public Lightning capacity is small and shrinking (3,203 BTC on 2026-11-04, about 0.016% of supply, 45% below the December 2025 peak) after a wave of 2026 security incidents; it is an LND monoculture (80 to 84%), and most users have historically been custodial (1:8 in 2023), so Lightning offers cheap private payments but neither a public record nor a credible decentralised spending cap for agents.

### Cited Findings
- mempool.space network statistics (3-year series): 2023-11-27 5,419 BTC, 60,799 channels, 13,769 nodes; 2024-07-01 5,199 BTC, 50,974 channels; 2025-08-13 3,760 BTC; 2025-12-24 peak 5,756 BTC, 42,189 channels, 17,410 nodes; 2026-07-13 4,448 BTC, 39,638 channels; last point in the series 2026-08-30 3,754 BTC, 32,520 channels, 16,230 nodes ([mempool-ln](https://mempool.space/api/v1/lightning/statistics/3y)). The series has no points after 2026-08-30 and the 1-month endpoint returned empty on 2026-11-26 (data feed appears stalled).
- Coinpaprika compilation (mempool.emzy.de data): 2026-11-04 public capacity 3,203 BTC (about $251M), 28,939 channels, 15,899 nodes, median channel 0.02 BTC, 0.016% of 20.11M BTC circulating; peak 5,851.2 BTC on 2025-12-28; all-time channel high 82,825 on 2022-03-28; 2026-07-01 to 2026-11-04 channels -28.5%, capacity -30.4%; ten largest nodes hold 34.8% of channel-end capacity (2026-10-21), Binance 380.7 BTC, ACINQ 348.6 BTC; lists 2026 incidents (BTCPay Server flaw 7 Aug, a Foundation node drain, Core Lightning warning 1 Oct) and cites Bitcoin Data Labs counting 2,563 channel closures by four large operators between 2 and 16 Aug 2026 ([coinpaprika-ln](https://coinpaprika.com/education/bitcoin-lightning-network/)).
- Kumar (arXiv 2610.20952, Oct 2026): on 26 Aug 2026 Core Lightning maintainers told operators who could not upgrade to disconnect; 22% of CLN nodes went dark overnight; "LND runs 80% of public nodes (84% counting one operator's fleet of about 2,000 small nodes)" and 84% of public capacity, unchanged since 2023; network-wide reachability fell 7.8 points; losing ACINQ's Eclair node alone would cost four times the reachability lost with all 619 routable CLN nodes ([kumar-2026](https://arxiv.org/abs/2610.20952)).
- Reliability, independent: Waugh and Holz (2020) found success falls as payment size rises and "only about a third of destination nodes can be successfully reached" at best ([waugh-holz-2020](https://arxiv.org/abs/2006.14358)).
- Reliability and custody, vendor (River Lightning Report 2023): "River's Lightning payment success rate was 99.7% in August 2023 across 308k transactions", failures mainly when no route has enough liquidity or a non-custodial recipient is offline; lower bound 6.6 million routed transactions in Aug 2023; 279k to 1.116 million monthly active users with "an estimated ratio of 1:8 non-custodial to custodial Lightning users" (Sept 2023); average public payment 44.7k sats ($11.84) ([river-ln-2023](https://www.river.com/learn/files/river-lightning-report-2023.pdf)).
- Usage (vendor, via coinpaprika): River estimated $1.17 billion over 5.22 million transactions in Nov 2025 ([coinpaprika-ln](https://coinpaprika.com/education/bitcoin-lightning-network/)).

### Inferences
- A 99.7% success rate from a well-connected custodian's own payments and a one-third reachability figure from independent probing measure different things; the honest model is: small payments between well-connected hubs succeed, large or remote payments often do not.
- For Escapement, Lightning can enforce a spending cap only in the narrow sense that a non-custodial channel cannot spend more than its local balance. Most users are custodial, so in practice the cap is the custodian's policy, not a protocol property.
- Lightning payments leave no public, non-equivocable record, so Lightning cannot serve N8-style logging; it competes with, rather than supports, on-chain anchoring.
- Client monoculture (LND 80 to 84%) and hub concentration (top 10 nodes 34.8%) mean an agent-payment design on Lightning inherits a small number of operational choke points.

### Gaps
- No independent 2025 to 2026 payment-success measurement found; 1ML and Amboss not opened.
- No current, verifiable custodial share; an 80% custodial claim (Paul Sztorc, 2025) appeared only in news snippets and is unverified.

## Privacy: chain analysis, Taproot, Lightning, and what a bond or anchor reveals

### Takeaway
Bitcoin is pseudonymous with globally visible flows; clustering heuristics have linked wallets since 2013 and Lightning nodes to on-chain addresses since 2021. A public bond or anchor is, by construction, a public and linkable fact about its owner.

### Cited Findings
- Meiklejohn et al. (IMC 2013): Bitcoin "has the unintuitive property that while the ownership of money is implicitly anonymous, its flow is globally visible"; the authors use "heuristic clustering to group Bitcoin wallets based on evidence of shared authority, and then ... re-identification attacks (i.e., empirical purchasing of goods and services)" ([meiklejohn-2013](https://smeiklej.com/files/imc13.pdf)).
- Kappos et al. (USENIX Security 2022) propose a peel-chain heuristic and an ML-based validation method, evaluated against ground truth, to validate and expand existing clustering ([kappos-2022](https://www.usenix.org/conference/usenixsecurity22/presentation/kappos)).
- Romiti et al. (FC 2021, arXiv v3 2021-02-10): cross-layer heuristics "link 45.97% of all LN nodes to 29.61% of Bitcoin addresses interacting with the LN"; "five actors control 36 nodes and over 33% of the total LN capacity" ([romiti-2021](https://arxiv.org/abs/2007.00764)).
- Kappos et al. (FC 2021): attacks using public network information learn a node's balance and the sender and recipient of routed payments ([kappos-2021](https://arxiv.org/abs/2003.12470)).
- Taproot (BIP-341): "multi-party public keys and signatures are indistinguishable from their single-party equivalents"; "Ideally, outputs are spent using the key path which prevents observers from learning the spending conditions of a coin"; script path reveals only the executed leaf ([bip341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki)).
- Belcher's fidelity bonds (2019) prove a timelocked UTXO by "revealing the TXID and vout" so anyone can check it against the UTXO set ([belcher-2019](https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af)).

### Inferences
- A bond whose timelock must be verifiable by third parties before it is spent must disclose its script (and therefore the public key and lock height), so Taproot's key-path privacy does not apply to a verifiable bond. The bond reveals: amount, lock height, creation height (coin age), funding inputs (and thus, via common-input clustering, likely other wallets of the owner), and any change output.
- An OP_RETURN anchor reveals the funding UTXO history, change address, fee behaviour and timing pattern (an agent that anchors every N blocks fingerprints itself). Aggregation through OpenTimestamps calendars hides the anchoring entity behind a calendar's transaction at the cost of hours of latency (see N8 below).
- Undercut: "public, costly-to-rewrite record" and "privacy for the agent's owner" pull in opposite directions; Escapement must choose per mechanism which one it wants.

### Gaps
- No quantitative accuracy figures for modern commercial chain-analysis (Chainalysis, TRM) were opened; vendor claims were not used.

## Custody concentration: who holds the keys

### Takeaway
At least about 4.05 million BTC (about 20% of supply) sits with tracked companies, funds, exchanges and governments, plus about 2.85 million BTC on exchange addresses (some overlap); a handful of custodians, notably the US spot ETFs (IBIT alone about 750k BTC) and Strategy (about 851k BTC), control keys for a large share.

### Cited Findings
- IBIT holdings file: 749,654.27420 BTC, market value $44,497,078,820.04, as of 2026-11-24; inception 2024-01-05 ([ishares-ibit-csv](https://www.ishares.com/us/products/333011/ibit/latest-holdings.csv)); fund page: net assets $44,929,927,533 as of 2026-11-25, basket 22.63 BTC ([ishares-ibit](https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf-ibit)).
- bitcointreasuries.net (aggregator, accessed 2026-11-26): public companies 1,239,002 BTC; private companies 201,884; government entities 645,639; ETFs and exchanges 1,589,940; DeFi and other 376,202; Strategy 851,305 (4.054% of 21M), Metaplanet 44,000, Twenty One 43,841 ([bitcointreasuries](https://bitcointreasuries.net/)); governments: United States 328,372, China 190,000, United Kingdom 61,245, Ukraine (officials' holdings) 46,351, El Salvador 7,846, UAE 6,420 ([bitcointreasuries-gov](https://bitcointreasuries.net/governments)); ETF list: IBIT 785,531, FBTC 184,058, GBTC 131,528, Grayscale Mini 62,874, Xapo 38,931, BITB 38,189, ARKB 35,026, Mt. Gox 34,504, River 33,737 ([bitcointreasuries-etf](https://bitcointreasuries.net/etfs-and-exchanges)). Its IBIT figure (785,531) is about 36k BTC above the fund's own 2026-11-24 file; the fund file is preferred.
- Strategy 8-K (filed 2026-11-09): 1,036 BTC bought 2026-11-02 to 08; aggregate 850,364 BTC at $64.16B, average $75,456 ([sec-mstr](https://www.sec.gov/Archives/edgar/data/0001050446/000119312526452693/mstr-20261109.htm)); 850,849 BTC as of 2026-11-15 after 485 BTC at $68,887 average ([theblock-mstr](https://theblock.co/news/business/2026-11-16-this-dip-could-use-a-little-orange-michael-saylor-strategy-bitcoin-tumbles-440886)).
- Exchange reserves: "Exchange addresses now hold 2.85 million BTC" (note dated 2026-11-18; data source not named) ([adler-20261118](https://axeladlerjr.com/weekly-net-exchange-outflow-reaches-14k-btc.md)).
- Glassnode classifies 1.63 to 1.66M BTC of exchange balances inside its quantum "operational exposure" bucket (May 2026) ([glassnode-quantum](https://research.glassnode.com/measuring-bitcoins-quantum-exposed-supply/)).

### Inferences
- Derived share: 4,052,667 BTC tracked by bitcointreasuries = 20.1% of about 20.12M supply; adding 2.85M exchange BTC (14.2%) gives an upper bound near 34%, with double counting where exchanges appear in both.
- For Escapement, an agent "holding sats" is very likely holding them through one of these custodians unless the design forces self-custody; the unforgeable-authority property of keys then reduces to the custodian's internal controls.
- Large custodians are also natural chokepoints for regulation, which is good for compliance-oriented limits and bad for censorship-resistant ones.

### Gaps
- Custodian identity for each ETF (for example Coinbase Custody for IBIT) not verified from a prospectus.
- Exchange-reserve methodologies differ (CryptoQuant, Glassnode, Santiment); no single verified November 2026 figure from a primary data vendor.

## Mining: hashrate, pool and template concentration, censorship, attack cost, security budget, quantum

### Takeaway
Hashrate is about 1 ZH/s (first touched intraday 2025-04-04; daily estimates peaked 1,306 EH/s on 2025-10-25), but block production is concentrated: two pools mine about 46% of blocks, five about 77%, and six template producers over 95%; fees are under 1% of miner revenue, so security is about 99% subsidy that halves again around April 2028. Quantum risk to exposed keys (about 30% of supply) is now a near-term engineering estimate, and the main mitigation (BIP-360 P2MR) is still a Draft.

### Cited Findings
- Hashrate (mempool.space estimates): current 1,051.9 EH/s, 3-day 1,041 EH/s on 2026-11-26; daily series 496 EH/s (2023-11-27), 747 (2024-11-21), 1,088 (2025-09-17), maximum 1,306 (2025-10-25), 898 (2026-01-15), 1,025 (2026-09-12); first 7-sample average at or above 1 ZH/s ends 2025-08-31 (derived) ([mempool-hashrate](https://mempool.space/api/v1/mining/hashrate/3y)).
- First 1 ZH/s: Glassnode data, a Friday intraday reading (2025-04-04, about 1,025 EH/s) while the 7-day average was 879 EH/s; prior record 975 EH/s on Jan 31; hashprice at an all-time low of $42.40 then ([coindesk-1zh](https://www.coindesk.com/markets/2025/04/07/bitcoin-hashrate-surpasses-1-zettahash-as-miner-revenue-hits-record-low); [forklog-1zh](https://forklog.com/en/bitcoin-hashrate-surpasses-one-zettahash-for-the-first-time/)).
- Hashrate Index (2026-11-16): 7-day SMA 967 EH/s, 30-day SMA 1,030 EH/s; difficulty 134.82T after -9.1% on 2026-11-14; hashprice $30.45/PH/day; energy hashprice $105 (<14 J/TH), $76 (14 to 19), $57 (19 to 25), $39 (25 to 38 J/TH) per MWh ([hri-20261116](https://hashrateindex.com/blog/hashrate-index-roundup-november-16-2026/)). mempool.space projects +8.98% at height 977,760 ([mempool-difficulty](https://mempool.space/api/v1/difficulty-adjustment)).
- Pool shares by blocks (mempool.space): trailing year Foundry 14,561 of 52,413 blocks (27.8%), AntPool 18.4%, F2Pool 13.3%, ViaBTC 9.4%, SpiderPool 8.5%, MARA 5.1%, SECPOOL 4.3%, Luxor 3.3%, OCEAN 2.3%; trailing week Foundry 23.3%, AntPool 22.7%, F2Pool 16.3%; top two 46.0 to 46.1%, top five 77.4 to 78.2% (derived) ([mempool-pools](https://mempool.space/api/v1/mining/pools/1y)).
- Template centralisation (b10c, 2025-04-15): "AntPool & friends" about 40% of hashrate in 2024; Foundry plus AntPool & friends 60 to 70% over two years; "we know that six block template producers mine more than 95% of the blocks"; Dec 2023 top 2 above 55%, top 6 at 90%; OCEAN, where miners build templates, under 1% ([b10c-2025](https://b10c.me/blog/015-bitcoin-mining-centralization/)).
- OFAC filtering (b10c, 2025-01-16): 15 OFAC-sanctioned transactions missing from 14 blocks; 11 of the blocks F2Pool's; F2Pool "might have started to filter OFAC-sanctioned transactions again"; since it is the only pool apparently filtering it "does not affect Bitcoin's censorship resistance" and all were included later ([b10c-ofac](https://b10c.me/observations/13-missing-sanctioned-transactions-2024-12/)).
- Reorgs: two-block reorg at heights 941,881 to 941,882 on 2026-03-23 (AntPool and ViaBTC blocks stale, Foundry won and "ended up mining seven blocks in a row"); previously known two-block stale chains 2023-05-08, 2020-11-12, 2015-06-02, 2013-10-02, roughly one per 150k blocks; fees in the reorged blocks 0.008 and 0.017 BTC ([bnoc-reorg](https://mirror.b10c.me/bnoc-xyz/2026-03-23-two-block-reorg-at-height-941880-id97.html)). March 2013 fork: 0.8 chain had about 60% of hashpower, at least one large double spend succeeded, resolved by pools downgrading ([bip50](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0050.mediawiki)).
- Six confirmations: Nakamoto's table gives z=5 for q=0.10 at P<0.1%, z=24 for q=0.30, z=89 for q=0.40, z=340 for q=0.45; for q=0.1, z=6 gives P=0.0002428 ([nakamoto-2008](https://bitcoin.org/bitcoin.pdf), section 11).
- Attack cost: crypto51 shows BTC hashrate 1,082,363 PH/s, theoretical 1h attack cost $1,843,332, NiceHash-able 0% (updated 2026-11-26 09:08 EST) ([crypto51](https://www.crypto51.app/)).
- Budish (NBER w24717, 2018): two equilibrium conditions (zero-profit mining; majority attack unprofitable) imply recurring payments to miners "must be large relative to the one-off, 'stock', benefits of attacking it"; relief only if hardware is scarce and non-repurposable and an attack would collapse the value; "Bitcoin would be majority attacked if it became sufficiently economically important" ([budish-2018](https://www.nber.org/papers/w24717)).
- Timewarp: a majority miner can set timestamps so difficulty halves each epoch until blocks come at "six blocks per second", after about a month of visible setup, then about another month to claim the remaining subsidy (Optech) ([optech-timewarp](https://bitcoinops.org/en/topics/time-warp/)). BIP-54 Consensus Cleanup (Poinsot, Corallo; status Complete, v1.0.0 2026-05-22) fixes it: first block of a period must be at least previous block time minus 7,200 s, last block of a period at least the first block's time; no activation height stated; Core 29.0+ will not create violating templates ([bip54](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0054.md)).
- Quantum: BIP-360 "Pay-to-Merkle-Root (P2MR)" (Beast, Heilman, Foxen Duke), Status Draft, merged 2026-02-11 (commit "BIP360: Pay to Merkle Root (P2MR) (#1670)"), v0.12.1, last edit 2026-08-03; removes the Taproot key path; resistant only to long-exposure attacks; no post-quantum signatures ([bip360](https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki); [bip360-history](https://api.github.com/repos/bitcoin/bips/commits?path=bip-0360.mediawiki)). Earlier names: P2QRH, then "Pay-to-Tapscript-Hash (P2TSH)" in the 2025-12-19 rewrite announcement ([bitcoindev-bip360](https://groups.google.com/g/bitcoindev/c/3JWQwnMUetg)). BIP-361 "Post Quantum Migration and Legacy Signature Sunset" (Lopp et al., Draft, assigned 2026-02-11): Phase A bans sends to quantum-vulnerable addresses, Phase B restricts ECDSA/Schnorr spends five years after activation; states "As of March 1, 2026, over 34% of all bitcoin have revealed a public key on-chain" ([bip361](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0361.mediawiki)). Glassnode (2026-05-20): 6.04M BTC (30.2%) exposed at rest, structural 1.92M (P2PK, bare multisig, P2TR), operational 4.12M ([glassnode-quantum](https://research.glassnode.com/measuring-bitcoins-quantum-exposed-supply/)). Babbush, Zalcman, Gidney, ..., Drake, Boneh (arXiv 2603.28846, 2026-03-30, v2 2026-04-15): 256-bit ECDLP with under 1,200 logical qubits and under 90M Toffoli gates (or under 1,450 and under 70M), runnable "in minutes using fewer than half a million physical qubits" at 1e-3 error rates; results validated by a zero-knowledge proof "without disclosing attack vectors" ([babbush-2026](https://arxiv.org/abs/2603.28846)).

### Inferences
- Double-spend risk at 6 confirmations from the largest single pool (q = 0.278): 8.9%; from the top two colluding (q = 0.46): 82%, and still 21% at 100 confirmations (derived from Nakamoto's formula). Finality for Escapement anchors therefore rests on non-collusion among two or three pool operators, not on depth. Budish's flow-versus-stock condition applies: anchors should never secure stakes comparable to what a colluding majority could gain.
- Opportunity cost for an existing majority to orphan 6 blocks is the forgone reward, about 18.8 BTC ($1.1M) (derived: 6 x (3.125 + 0.015)); the binding constraint for an outsider is acquiring hardware, since rental capacity is about 0% of hashrate (crypto51).
- Security budget: miner revenue is about 452 BTC/day, over 99% subsidy (derived). Next halving at height 1,050,000 is 72,305 blocks away, about 502 days at 10 minutes, so around April 2028 (derived); subsidy then 1.5625 BTC. The fee market is not on track to replace it at 1 sat/vB.
- Censorship: one pool (about 11 to 13% of blocks) filtering OFAC-listed transactions only delays them. If a few US-regulated template producers (Foundry alone 23 to 28%) were compelled to filter, sanctioned or "unapproved" agent transactions would be delayed but probably still mined by others; a design that relies on prompt inclusion of a specific transaction (for example, a penalty transaction before a timelock expires) is exposed to this.
- Quantum: P2TR outputs expose a (tweaked) public key from creation, so long-held P2TR bonds are long-exposure targets; a bond with a usable key path could be stolen the day a cryptographically relevant quantum computer exists, timelock or not. Bonds should use a NUMS internal key or P2WSH (key hidden until spend) until P2MR or post-quantum signatures exist. Hash-only commitments (anchors) are not threatened by Shor's algorithm.

### Gaps
- No primary current OFAC-filtering status for 2026 found.
- Bitmain's ability to supply 1 ZH/s of extra ASICs quickly is not sourced; hardware cost estimates use late-2025 discount news.

## Is block production uncompressible by an adversary?

### Takeaway
Against an adversary below 50% of hashrate, wall-clock time per block can be compressed only temporarily and expensively: doubling network hashrate (about $7.4 to 9.5B of current ASICs and about 18 GW) halves block time only until the next retarget, saving about 7 days per doubling, after which difficulty catches up. Against a majority, the timewarp bug (unfixed until BIP-54 activates) breaks the assumption entirely.

### Cited Findings
- Difficulty adjusts every 2,016 blocks, targeting an average number of blocks per hour; "If they're generated too fast, the difficulty increases" ([nakamoto-2008](https://bitcoin.org/bitcoin.pdf), section 4; [optech-timewarp](https://bitcoinops.org/en/topics/time-warp/)).
- Observed retarget swings in 2026: +5.9% (height 971,712), +5.5% (973,728), -9.1% (975,744), projected +9.0% (977,760) ([mempool-hashrate](https://mempool.space/api/v1/mining/hashrate/3y); [mempool-difficulty](https://mempool.space/api/v1/difficulty-adjustment)). Over the trailing year blocks came 0.3% slower than target (52,413 vs 52,560).
- S21: 200 TH/s, 3,500 W, 17.5 J/TH ([hri-s21](https://hashrateindex.com/rigs/bitmain-antminer-s21)); S21 immersion units discounted to about $7/TH in Dec 2025 ([ct-bitmain](https://cointelegraph.com/news/bitmain-slashes-asic-prices-mining-turmoil)).
- Timewarp lets a majority drive difficulty down until about six blocks per second ([optech-timewarp](https://bitcoinops.org/en/topics/time-warp/)); BIP-54 fix specified, not activated ([bip54](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0054.md)).
- Anthony Towns noted on 2026-08-09 that the stalled BIP-110 minority chain would take "100-150 years to the retarget" ([bitcoindev-bip110](https://groups.google.com/g/bitcoindev/c/b_aV3JUtUqg)): difficulty also makes block time stretchable when hashrate leaves.

### Inferences
- Compression model (derived): a one-time k-fold hashrate increase at the start of an epoch shortens that epoch from 14 days to 14/k days, saving 14 x (1 - 1/k) days: k = 1.1 saves 1.3 days, 1.5 saves 4.7, 2 saves 7.0, 3 saves 9.3. Thereafter block time returns to about 10 minutes (the 4x per-retarget cap matters only for k > 4). Sustained exponential hashrate growth sustains a proportional compression; historical growth (496 to 1,052 EH/s in three years) produced no net compression over the last year.
- Cost to compress one epoch by 7 days: add about 1.05 ZH/s, about $7.4 to 9.5B hardware at $7 to 9/TH plus 18.4 GW of power (about 161 TWh/yr at 17.5 J/TH): comparable to a third of all data-centre electricity in 2025 (derived). Block height is therefore a strong clock against fast cognition (agents cannot think their way to faster blocks) and a weak clock only against nation-scale capital or a majority of existing miners.
- Height-based timelocks (CLTV/CSV in blocks) inherit this; time-based locks inherit miner-chosen timestamps. A seasoned bond's age in blocks is uncompressible in the above sense, but age is transferable by selling keys of old UTXOs (see N6).
- The clock can also stall: if hashrate falls sharply (for example, miners redirect power to AI hosting), blocks slow until the next retarget, which can delay timelock expiries by days. Escapement designs need tolerance in both directions.

### Gaps
- No peer-reviewed timewarp cost analysis opened beyond Optech and BIP-54 text.

## Energy: Bitcoin vs data centres and AI; miners pivoting to AI/HPC

### Takeaway
Bitcoin uses about 138 to 190 TWh/yr (about 16 to 22 GW), roughly 39% of global data-centre electricity in 2025; the two compete for the same grid interconnections, and AI hosting now pays roughly 2 to 4 times more per MW than mining, which is why the largest listed miners have signed more than $40B of AI/HPC leases since mid-2024.

### Cited Findings
- Cambridge Digital Mining Industry Report (2025-04-28): 138 TWh/yr, about 0.5% of global electricity, "Based on the reported data, which represents 48% of global mining activity"; 39.8 MtCO2e; sustainable sources 52.4% (renewables 42.6%, nuclear 9.8%), gas 38.2%, coal 8.9%; US 75.4% of reported activity ([cambridge-2025](https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/)).
- Preliminary CCAF update (reported 2026-07-26): about 190 TWh annualised for December 2025, vs 138 TWh for June 2024; emissions about 48 Mt; low-carbon 59.4%; presented by Alexander Neumueller at the Energy Investors Forum, Dallas; "It does not mean miners consumed exactly 190 TWh during the 2025 calendar year" ([cryptonews-ccaf](https://crypto.news/hydropower-overtakes-gas-as-bitcoin-mining-power-use-jumps-38/)).
- IEA Energy and AI (2025): "Data centres accounted for around 1.5% of the world's electricity consumption in 2024, or 415 terawatt-hours (TWh)"; about 945 TWh by 2030; US 45%, China 25%, Europe 15% of 2024 consumption; 12%/yr growth since 2017 ([iea-2025](https://www.iea.org/reports/energy-and-ai/executive-summary)).
- IEA Key Questions on Energy and AI (2026): data-centre demand "grew by 17% in 2025", 485 TWh to 950 TWh in 2030 (about 3% of global demand); AI-focused data centres "surging 50% in 2025" and tripling by 2030; the page does not mention cryptocurrency mining ([iea-2026](https://iea.org/reports/key-questions-on-energy-and-ai/executive-summary)). Euronews (2026-11-19) reports the World Energy Outlook 2026 Stated Policies Scenario at about 1,000 TWh by 2030 ([euronews-weo](https://www.euronews.com/2026/11/19/data-centre-energy-consumption-could-double-by-2030-straining-grids-iea-warns)).
- Miner pivots (all vendor or deal-party claims):
  - Core Scientific and CoreWeave: 2025-02-26 new 70 MW at Denton TX (about 260 MW there) bringing CoreWeave to about 590 MW across six sites and "Total Projected Revenue to $10.2 Billion over 12-year Contract Terms" ([corz-pr](https://investors.corescientific.com/news-events/press-releases/detail/110/core-scientific-and-coreweave-expand-partnership-with-new-70-mw-contract)); CoreWeave's about $9B all-stock acquisition (0.1235 CRWV per CORZ) was rejected by Core Scientific shareholders on 2025-10-30 ([theblock-corz](https://www.theblock.co/news/deals/2025-10-30-core-scientific-vote-sinks-9-billion-coreweave-deal-halting-merger-ai-cloud-bitcoin-miner-376959)).
  - TeraWulf, Fluidstack, Google: 2025-08-14, two 10-year HPC colocation agreements, more than 200 MW critical IT load (about 250 MW gross) at Lake Mariner NY, about $3.7B contracted (up to $8.7B with extensions), Google backstops $1.8B and receives warrants for about 8% ([terawulf-pr](https://d1io3yog0oux5.cloudfront.net/_feb0a76e67864434a1559c67c13db5b2/terawulf/news/2025-08-14_TeraWulf_Signs_200_MW_10_Year_AI_Hosting_112.pdf)); 2026-11-04, "approximately $19 billion of contracted lease commitments with Anthropic, PBC" at Justified Data Campus, Hawesville KY, Google credit support for debt, Fluor EPC, phased completions late 2027 to Q2 2028 ([terawulf-2026](https://finviz.com/news/415380/terawulf-secures-google-credit-backstop-for-project-financing-in-support-of-19-billion-anthropic-lease-executes-definitive-fluor-epc-agreement)).
  - Cipher Mining: 2025-09-25, Fluidstack 168 MW critical IT (244 MW gross) at Barber Lake, Colorado City TX, 10 years, about $3B (about $7B with renewals), Google backstop $1.4B for about 5.4% ([theblock-cipher](https://www.theblock.co/post/372315/cipher-mining-google-backed-3-billion-usd-ai-hosting-deal)); AWS 15-year lease, 300 MW gross, about $5.5B (posted 2025-11-05) ([davispolk-cipher](https://www.davispolk.com/experience/cipher-mining-300-mw-5-5-billion-lease-agreement-amazon-web-services)).
  - IREN and Microsoft: 2025-11-03, about $9.7B, five years, NVIDIA GB300, 20% prepayment, about $5.8B Dell equipment purchase, Childress TX (750 MW campus, 200 MW IT in Horizon 1 to 4) ([iren-yahoo](https://finance.yahoo.com/news/iren-signs-microsoft-9-7-132523930.html)).
  - Hut 8: 2025-12-17, River Bend campus, West Feliciana Parish LA, 245 MW IT, 15-year base term, $7.0B (3% escalator), up to about $17.7B with three 5-year renewals, tenant Fluidstack, Google backstop of lease payments ([hut8-pr](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion)); the press-release title references Anthropic but the body opened does not name it.

### Inferences
- Revenue per MW (derived): AI hosting rent about $1.4 to 1.9M per MW of IT load per year ($164 to 217 per MW-hour; Hut 8 $7.0B / 15 / 245; TeraWulf $3.7B / 10 / 200; Cipher $3B / 10 / 168; Core Scientific $10.2B / 12 / 590) vs mining gross revenue $0.50 to 0.92M per MW-year ($57 to 105/MWh, before power cost). Not like-for-like (triple-net leases often pass power through; mining revenue is before power), but the direction is unambiguous: a megawatt is worth more hosting GPUs than hashing.
- The fungible asset is the interconnection, site and cooling, not the ASIC. SHA-256 ASICs cannot run AI workloads (Budish's "non-repurposable" hardware condition), so the pivot moves power away from hashing rather than turning hashing into AI.
- Energy competition is the only real coupling between Bitcoin and AI compute today, and it runs against the thesis: AI demand bids power away from mining, lowering hashrate (and the security budget) at the margin. Hashrate has nonetheless stayed near 1 ZH/s through 2026.

### Gaps
- Final CCAF second-edition report not yet published (190 TWh is preliminary and secondary-reported).
- IREN and Cipher primary press releases returned 403; deal terms rest on news and law-firm pages.

## Is there any technical link between SHA-256 proof-of-work and measuring or limiting AI compute? (PoUW, Laurie and Clayton, Dwork and Naor, Back)

### Takeaway
No. SHA-256 proof-of-work proves that someone spent hashing work on a specific block header; it says nothing about, and imposes no limit on, anyone's other computation. Proof-of-useful-work and proof-of-learning schemes exist but are either unproven for consensus or not robust, and none secures Bitcoin. Pricing-via-processing as a rate limit was shown not to work against well-resourced adversaries as early as 2004.

### Cited Findings
- Laurie and Clayton, "'Proof-of-Work' Proves Not to Work" (2004 draft dated 3 May 2004): the puzzle difficulty needed to stop spam (limit senders to 1,750 messages/day economically, or 250/day if spammers control a million compromised machines) "would mean that significant numbers of senders of legitimate email would be unable to continue their current levels of activity"; "For proof-of-work schemes to be plausible one would be looking for many orders of magnitude between the work done by the 'good guys' and that achievable by the 'bad guys'" (section 5); it attributes the idea to "Dwork and Naor in 1992" and describes "Back's independently invented 'hashcash'" ([laurie-clayton-2004](https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf)).
- Ball, Rosen, Sabin, Vasudevan, "Proofs of Useful Work" (ePrint 2017/203, revised 2021-02-26): PoWs based on Orthogonal Vectors, 3SUM, All-Pairs Shortest Path; the 2018 update notes reviewers showed the definition "is already satisfied by a generic naive construction" ([ball-2017](https://eprint.iacr.org/2017/203)).
- Komargodski and Weinstein, "Proofs of Useful Work from Arbitrary Matrix Multiplication" (arXiv 2504.09971, v4 2025-11-13): 1+o(1) overhead over naive MatMul; optimal security is a conjecture; blockchain "currently under construction" ([komargodski-2025](https://arxiv.org/abs/2504.09971)).
- Jia et al., "Proof-of-Learning" (IEEE S&P 2021, arXiv 2103.05633): proves a party expended the compute to obtain particular parameters ([jia-2021](https://arxiv.org/abs/2103.05633)); Fang et al. (IEEE EuroS&P 2023): PoL verification "is not robust to adversaries", spoofs cost a fraction of previous ones, and a provably robust PoL is not possible without better understanding of deep-learning optimisation ([fang-2023](https://arxiv.org/abs/2208.03567)).
- Gensyn litepaper (Feb 2022, marked out of date): probabilistic proof-of-learning, graph-based pinpoint protocol, Truebit-style staking and slashing; a compute marketplace verification scheme, not a ledger consensus ([gensyn](https://docs.gensyn.ai/litepaper)).
- Primecoin: "scientific computing proof-of-work" "searching for prime number chains" ([primecoin-code](https://github.com/primecoin/primecoin)).
- Compute-governance literature: Sastry et al. (2024) argue AI-relevant compute "is detectable, excludable, and quantifiable"; the abstract does not mention proof-of-work or crypto mining ([sastry-2024](https://arxiv.org/abs/2402.08797)).

### Inferences
- Why PoUW does not secure Bitcoin (derived reasoning from the above): Bitcoin's security needs work that is (1) bound to the block being produced, (2) cheaply verifiable by every node, (3) with no external value, so the only reason to do it is the block reward. Useful work fails (3) (the work pays for itself, lowering the honest cost and making attacks cheaper in Budish's terms), and existing PoL fails (2) robustly (Fang et al.). PoUW candidates also break (1) if miners choose their own inputs.
- Laurie and Clayton's result is a direct warning for N7 and N10: pricing actions by work or by fees only throttles actors whose budget is close to the honest user's; an adversary with "many orders of magnitude" more resources (a frontier lab, a state, or a botnet of agents) is not rate-limited.
- The honest answer for Escapement: proof-of-work is relevant to AI governance only as (a) the reason Bitcoin's history is costly to rewrite and its block clock hard to speed up, and (b) a competitor for electricity. It is not a meter, cap, or attestation of AI compute.

### Gaps
- Dwork and Naor (1992) and Back (2002) PDFs could not be opened (connection errors); claims about them rest only on Laurie and Clayton's description.

## Bitcoin's economic security limits for anchoring: Budish, finality conventions, reorg history

### Takeaway
Anchoring inherits Bitcoin's flow-security budget (about $27M/day of miner revenue, over 99% subsidy) and its pool concentration; six confirmations are a convention calibrated for a 10% attacker, not for today's 23 to 28% largest pool, and economic finality rests on two or three operators not colluding.

### Cited Findings
- Budish (2018) flow-versus-stock condition and "intrinsic economic limits" ([budish-2018](https://www.nber.org/papers/w24717)).
- Nakamoto 2008 z-table and q=0.1 and q=0.3 probability series ([nakamoto-2008](https://bitcoin.org/bitcoin.pdf)).
- IETF draft (Fassbender, 2026-07-24) for Bitcoin-anchored SCITT proofs sets MIN_CONFIRMATIONS = 6 before a proof is "valid" ([ietf-scitt-anchor](https://www.ietf.org/archive/id/draft-fassbender-scitt-time-anchor-03.html)).
- Reorg history as above: two-block reorgs about every 150k blocks, latest 2026-03-23 ([bnoc-reorg](https://mirror.b10c.me/bnoc-xyz/2026-03-23-two-block-reorg-at-height-941880-id97.html)); 2013 fork with a successful double spend ([bip50](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0050.mediawiki)).

### Inferences
- Miner revenue about 452 BTC/day x $60,000 = $27M/day, about $9.9B/yr (derived). Per Budish, the value an anchor protects (the gain from rewriting it) must stay small relative to the cost of a multi-block majority attack; for anchors that bind high-value agent obligations, either cap the value bound by any single anchor or require depth plus independent cross-anchoring (for example, multiple chains or independent witnesses).
- Natural reorgs beyond two blocks have not occurred in the modern era per the Towns list; deep reorgs are an adversarial, not a stochastic, risk.

### Gaps
- No modern quantitative estimate of the capital cost of a sustained 51% attack (hardware plus power plus sites) from a peer-reviewed source was opened.

## Implications for Escapement

1. **Spending caps (scarce value) are real, but only for self-custodied keys.** About 20 to 34% of BTC sits with ETFs, companies, governments and exchanges; an agent using a custodian is capped by the custodian's policy, not by Bitcoin. Escapement should require self-custody or multisig with the agent holding at most one key.
2. **Fees do not make commitments costly.** At 1 sat/vB a 154 vB anchor costs about $0.09; fees spike 200x to 800x only during speculative manias. Costly commitment must come from locked capital (bonds) and time, not blockspace. This undercuts N7 as a pure "price" mechanism.
3. **Blockspace is a rate limit on on-chain events, not on actions.** About 6,500 anchors per block is the ceiling, but one anchor can commit to unlimited actions via a Merkle root. N7 only works if each high-stakes action must be its own UTXO event (for example, spending a single-use seal), which is exactly the Catena/single-use-seal construction.
4. **Block height is an uncompressible clock against cognition, compressible against capital.** Halving block time for one epoch needs about $7 to 9B of ASICs and about 18 GW; it saves about 7 days and then difficulty catches up. A majority of existing miners could do far more via timewarp until BIP-54 activates. Timelocked bonds measured in blocks are robust against fast agents, not against states or colluding pools.
5. **Finality depends on two or three pool operators.** At q = 0.46 (top two), 6 confirmations give 82% attacker success in Nakamoto's model. Size what an anchor can bind accordingly; prefer designs where a successful rewrite is detectable after the fact (non-equivocation) over designs where it must be prevented.
6. **Privacy cost.** Verifiable bonds and anchors deanonymise their owners via clustering; agents that must be accountable can accept this, but owners seeking privacy cannot use the same mechanism.
7. **Quantum horizon.** About 30% of supply has exposed keys; 2026 estimates put ECDLP-256 within about 1,200 logical qubits. Multi-year bonds in P2TR with a live key path are a target; use NUMS-key or P2WSH bonds and plan for P2MR (BIP-360, Draft) or post-quantum signatures. Hash anchors are fine.
8. **Proof-of-work has no technical link to AI compute.** It cannot meter, cap or attest AI training or inference. The only coupling is competition for electricity, where AI pays 2 to 4 times more per MW and is pulling sites away from mining; if anything this weakens Bitcoin's security budget at the margin. N10 should be dropped or reframed as "energy-backed time" rather than "compute governance".
9. **Security budget trend.** Fees are 0.5 to 0.7% of miner revenue; the next halving (about April 2028) cuts the subsidy to 1.5625 BTC. Long-horizon Escapement commitments (years) should assume weaker Bitcoin security than today unless fees rise.
10. **Governance and policy risk on data.** The 2025 to 2026 OP_RETURN fight (Core 30 relaxing limits, BIP-110 failing with a minority chain split on 2026-08-08) shows the community tolerates small commitments; keep anchors at 32 to 80 bytes.

## Novelty check (N6 to N10)

**N6. Seasoned (coin-age or timelocked) bonds as sybil friction for agent swarms.**
- Closest prior work: Belcher's JoinMarket fidelity bonds (2019): makers burn coins or lock them with OP_CHECKLOCKTIMEVERIFY, bond value grows with the square of sacrificed value, f = V^2 (exp(rT) - 1)^2 for timelocked coins; estimated sybil cost "30,000-80,000 bitcoins for 6 months" or 45 to 120 BTC burned; proofs by revealing TXID and vout; critics noted bonds can be rented ([belcher-2019](https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af)). Coin-age as an alternative is raised in the gist comments. Peercoin-style coin age was not opened (unverified).
- Agent-specific: search found bond-before-action write-ups for AI agents (AgentGate on dev.to, ERC-8004 sybil study) only as search snippets, not opened.
- Verdict: **partial**. The mechanism (timelocked bonds as sybil friction, valued by amount x time) exists and is deployed for coinjoin makers; applying it to AI agent swarms with block-height seasoning was not found. Weak point: coin age transfers with the private key, so aged UTXOs can be bought or rented; the time cost is compressible by money.
- Queries tried: "AI agents bitcoin timelocked bond sybil resistance agent swarm"; "JoinMarket fidelity bonds timelocked sybil resistance Belcher".

**N7. Blockspace as a global rate limit on high-stakes AI actions.**
- Closest prior work: Laurie and Clayton (2004) showing pricing-via-processing fails as a rate limit against resource-rich adversaries ([laurie-clayton-2004](https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf)); Catena (one log statement per Bitcoin transaction, as hard to fork as Bitcoin) implies a per-log rate tied to blocks ([catena-2017](https://eprint.iacr.org/2016/1062)).
- Verdict: **not found** as a proposal; the theory that exists argues against it (price-based throttles fail for rich adversaries; aggregation defeats per-action limits).
- Queries tried: "Bitcoin blockspace scarce global rate limit high-stakes AI actions"; "proof-of-work energy AI compute governance analogy bitcoin mining compute threshold".

**N8. Tamper-evident, non-equivocating agent action logs anchored in Bitcoin; model-weight hash commitments.**
- Closest prior work: Catena, Tomescu and Devadas, IEEE S&P 2017: logs as chains of OP_RETURN transactions; "if a log server wants to equivocate it has to double spend a Bitcoin transaction output"; auditor bandwidth from 90 GB to tens of MB ([catena-2017](https://eprint.iacr.org/2016/1062)). Single-use seals, Todd 2017: a seal "can be closed over a message exactly once", implemented by Bitcoin outpoints ([todd-2017](https://petertodd.org/2017/scalable-single-use-seal-asset-transfer)). IETF draft-fassbender-scitt-time-anchor-03 (2026-07-24): OpenTimestamps-based anchoring of SCITT transparency logs with block-height binding, six confirmations, motivating example "model weights and safety evaluations that must be auditable by regulators"; it explicitly does not claim to prevent equivocation for bare log roots ([ietf-scitt-anchor](https://www.ietf.org/archive/id/draft-fassbender-scitt-time-anchor-03.html)).
- Verdict: **exists** for non-equivocating logs (Catena) and for model-weight hash timestamping (IETF draft and OpenTimestamps); **partial** for logs of AI agent actions specifically (no source found that applies Catena-style non-equivocation to agent action logs).
- Queries tried: "Catena efficient non-equivocation via Bitcoin Tomescu Devadas"; "OpenTimestamps Peter Todd calendar aggregation Merkle bitcoin timestamp proof"; "model weights hash timestamp bitcoin OpenTimestamps AI model provenance anchoring".

**N9. Bitcoin as the clock for hardware-enabled compute governance (chip licence renewal anchored to block height).**
- Closest prior work: Petrie (2024) firmware-based offline licensing, chips disabled "unless they have an unused license from a regulator", requires firmware verification, rollback protection, secure NVRAM, no blockchain mentioned ([petrie-2024](https://arxiv.org/abs/2404.18308)); Petrie (2025) embedded off-switches, nonce-based licences and a consumable usage-allowance counter, no trusted clock and no ledger ([petrie-2025](https://arxiv.org/html/2509.07637)); the IETF SCITT draft uses block height as the normative time claim for artifacts ([ietf-scitt-anchor](https://www.ietf.org/archive/id/draft-fassbender-scitt-time-anchor-03.html)).
- Verdict: **not found**. Existing hardware-governance designs avoid clocks by using regulator nonces and counters; none uses Bitcoin headers as a freshness or expiry source. Note the design question this raises: a chip verifying block height needs header-chain validation (SPV) and is vulnerable to being fed a private low-work chain unless it enforces a minimum cumulative work, which a well-funded adversary can partly meet (see the compression costs above).
- Queries tried: "blockchain as trusted clock compute governance chip license block height"; "hardware-enabled governance mechanisms AI chips offline licensing renewal CNAS RAND flexHEG".

**N10. Proof-of-work as an energy anchor related to AI compute governance.**
- Closest prior work: proof-of-useful-work and proof-of-learning (Ball et al. 2017; Komargodski and Weinstein 2025; Jia et al. 2021; Fang et al. 2023; Gensyn 2022), which aim to make consensus work useful, not to govern AI; Sastry et al. (2024) on compute governance, whose abstract does not involve PoW.
- Verdict: **not found** as a governance proposal, and technically unsupported: SHA-256 work neither measures nor limits AI compute, and AI demand is currently displacing mining power.
- Queries tried: "proof-of-work energy AI compute governance analogy bitcoin mining compute threshold"; "Proof of useful work" related searches as above.

## Unverified (not opened or failed; no claim rests on these)
- Dwork and Naor 1992, "Pricing via Processing or Combatting Junk Mail", CRYPTO '92, DOI 10.1007/3-540-48071-4_10 (Springer redirect to login; Weizmann PDF connection reset).
- Back 2002, "Hashcash - A Denial of Service Counter-Measure" (hashcash.org TLS error).
- King and Nadal / King 2013 Primecoin whitepaper (404).
- Budish 2025, "Trust at Scale: The Economic Limits of Cryptocurrencies and Blockchains", QJE 140(1) (seen only in search results).
- Cambridge CBECI live dashboard (JavaScript only) and the CCAF primary release for 190 TWh.
- Glassnode and Coinglass inscription share dashboards; CryptoQuant exchange reserve quicktake; Santiment exchange share.
- IREN and Cipher GlobeNewswire releases (HTTP 403); Core Scientific 2024-06-03 release; TeraWulf CB-5 expansion release; b10c observation 08 (Nov 2023 F2Pool filtering).
- flexHEG interim report 2024 (404); RAND WRA3056-1; CNAS chip primer.
- Paul Sztorc 80% custodial claim; AgentGate bond write-up; ERC-8004 sybil study; Umarise Hugging Face POC; Project Eleven Risq list; McKinsey quantum monitor.
- iShares prospectus (custodian identity).

```yaml
sources:
  - key: mempool-fees
    authors: mempool.space
    year: 2026
    title: "mempool.space REST API: /api/v1/fees/recommended, /api/mempool, /api/v1/fees/mempool-blocks"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/fees/recommended
    url: https://mempool.space/api/v1/fees/recommended
    accessed: 2026-11-26
    supports: "Current recommended fees (2/1/1/1/1 sat/vB), mempool backlog 71,445 tx / 31.2 MvB, projected block fee rates"
  - key: mempool-hashrate
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/mining/hashrate/3y and /3d"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/mining/hashrate/3y
    url: https://mempool.space/api/v1/mining/hashrate/3y
    accessed: 2026-11-26
    supports: "Daily hashrate estimates 2023-11 to 2026-11, peak 1,306 EH/s on 2025-10-25, current 1,052 EH/s, difficulty adjustments"
  - key: mempool-pools
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/mining/pools/1w, 1m, 1y"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/mining/pools/1y
    url: https://mempool.space/api/v1/mining/pools/1y
    accessed: 2026-11-26
    supports: "Pool block shares (Foundry 27.8% 1y), top-2/top-5 concentration, 52,413 blocks in trailing year"
  - key: mempool-feerates
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/mining/blocks/fee-rates/all and /3y"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/mining/blocks/fee-rates/all
    url: https://mempool.space/api/v1/mining/blocks/fee-rates/all
    accessed: 2026-11-26
    supports: "Fee-rate history: 435 sat/vB 2023-05-08, 344 on 2023-12-16, 861 on 2024-04-20, monthly medians of 1 sat/vB since 2025-08"
  - key: mempool-block840000
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/block for height 840,000"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5
    url: https://mempool.space/api/v1/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5
    accessed: 2026-11-26
    supports: "Halving block: 2024-04-20 00:09 UTC, median fee 200 sat/vB, total fees 37.63 BTC, reward 40.75 BTC (subsidy 3.125 derived)"
  - key: mempool-ln
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/lightning/statistics/3y and /latest"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/lightning/statistics/3y
    url: https://mempool.space/api/v1/lightning/statistics/3y
    accessed: 2026-11-26
    supports: "Lightning capacity, channels, nodes 2023-11 to 2026-08-30; peak 5,756 BTC on 2025-12-24; series stalled after 2026-08-30"
  - key: mempool-blocks
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/blocks/{height} (last 144 blocks) and /api/v1/mining/blocks/sizes-weights/3y"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/blocks/977695
    url: https://mempool.space/api/v1/blocks/977695
    accessed: 2026-11-26
    supports: "Last 144 blocks: 4,620 tx/block, 3.93M WU, 257 vB/tx, median fee 1 sat/vB, 2.13 BTC fees; 30-day mean weight 3.92M WU"
  - key: mempool-difficulty
    authors: mempool.space
    year: 2026
    title: "mempool.space API /api/v1/difficulty-adjustment"
    venue: mempool.space
    type: dataset
    identifier: https://mempool.space/api/v1/difficulty-adjustment
    url: https://mempool.space/api/v1/difficulty-adjustment
    accessed: 2026-11-26
    supports: "Previous retarget -9.13%, next estimated +8.98% at height 977,760"
  - key: btccom-ntx
    authors: Blockchain.com
    year: 2026
    title: "Confirmed Transactions Per Day (charts API n-transactions)"
    venue: Blockchain.com
    type: dataset
    identifier: https://api.blockchain.info/charts/n-transactions?timespan=4years&format=json&sampled=false
    url: https://api.blockchain.info/charts/n-transactions?timespan=4years&format=json&sampled=false
    accessed: 2026-11-26
    supports: "Daily confirmed tx 2022-11 to 2026-11-25: annual means, max 927,010 (2024-04-23) and 963,618 (2026-11-15)"
  - key: bip141
    authors: Eric Lombrozo, Johnson Lau, Pieter Wuille
    year: 2015
    title: "BIP 141: Segregated Witness (Consensus layer)"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
    accessed: 2026-11-26
    supports: "Block weight = base size x 3 + total size; block weight <= 4,000,000; status Deployed"
  - key: optech-calc
    authors: Bitcoin Optech
    year: 2026
    title: "Transaction size calculator"
    venue: bitcoinops.org
    type: official docs
    identifier: https://bitcoinops.org/en/tools/calc-size/
    url: https://bitcoinops.org/en/tools/calc-size/
    accessed: 2026-11-26
    supports: "Overhead 10.5 vB; P2WPKH input 68.25, P2TR input 57.75; P2WPKH output 31, P2TR output 43 vB"
  - key: core-30
    authors: Bitcoin Core contributors
    year: 2025
    title: "Bitcoin Core 30.0 release notes"
    venue: bitcoincore.org
    type: official docs
    identifier: https://bitcoincore.org/en/releases/30.0/
    url: https://bitcoincore.org/en/releases/30.0/
    accessed: 2026-11-26
    supports: "Released 2025-10-10; datacarriersize 100,000 default, multiple OP_RETURN; minrelaytxfee 0.1 sat/vB; blockmintxfee 0.001; BIP54 sigops prep"
  - key: bip110
    authors: Dathon Ohm
    year: 2025
    title: "BIP 110: Reduced Data Temporary Softfork"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0110.mediawiki
    url: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0110.mediawiki
    accessed: 2026-11-26
    supports: "Proposed 34-byte scriptPubKey / 83-byte OP_RETURN / 256-byte push limits; mandatory signalling 961,632 to 963,647; status Closed"
  - key: bitcoindev-bip110
    authors: Jon Atack, Greg Tonoski, Anthony Towns, Murch, et al.
    year: 2026
    title: "BIP 110: update status to closed (mailing list thread)"
    venue: Bitcoin Development Mailing List
    type: essay/blog
    identifier: https://groups.google.com/g/bitcoindev/c/b_aV3JUtUqg
    url: https://groups.google.com/g/bitcoindev/c/b_aV3JUtUqg
    accessed: 2026-11-26
    supports: "Chain split 2026-08-08; about 2.5% signalling; 2 BIP-110 blocks vs 134 Bitcoin blocks; retarget 100 to 150 years away on minority chain"
  - key: bitquery-blocks
    authors: Bitquery
    year: 2026
    title: "What filled Bitcoin's blocks (on-chain forensics Oct 2022 to Aug 2026)"
    venue: bitquery.io
    type: company/vendor claim
    identifier: https://bitquery.io/investigations/what-filled-bitcoins-blocks
    url: https://bitquery.io/investigations/what-filled-bitcoins-blocks
    accessed: 2026-11-26
    supports: "Runes claims about 35% of block space and about six in ten tx in Jul 2026; payment-shaped tx 76.6% to 30.2%; witness share 21% Jul 2026"
  - key: coinpaprika-ln
    authors: CoinPaprika
    year: 2026
    title: "Bitcoin Lightning Network (statistics and guide)"
    venue: coinpaprika.com
    type: company/vendor claim
    identifier: https://coinpaprika.com/education/bitcoin-lightning-network/
    url: https://coinpaprika.com/education/bitcoin-lightning-network/
    accessed: 2026-11-26
    supports: "2026-11-04: 3,203 BTC, 28,939 channels, 15,899 nodes; peak 5,851 BTC 2025-12-28; 2026 incidents; top-10 nodes 34.8%; 20.11M BTC circulating"
  - key: kumar-2026
    authors: Saurabh Kumar
    year: 2026
    title: "Does Client Diversity Protect the Lightning Network? Evidence from the 2026 Core Lightning Shutdown"
    venue: arXiv
    type: preprint
    identifier: arXiv:2610.20952
    url: https://arxiv.org/abs/2610.20952
    accessed: 2026-11-26
    supports: "LND 80% of public nodes (84% incl. fleet), 84% of capacity; CLN disconnect instruction 2026-08-26; 22% of CLN nodes dark; reachability -7.8 pts"
  - key: waugh-holz-2020
    authors: Finnegan Waugh, Ralph Holz
    year: 2020
    title: "An empirical study of availability and reliability properties of the Bitcoin Lightning Network"
    venue: arXiv
    type: preprint
    identifier: arXiv:2006.14358
    url: https://arxiv.org/abs/2006.14358
    accessed: 2026-11-26
    supports: "Success falls with payment size; at best about one third of destinations reachable"
  - key: river-ln-2023
    authors: River Financial
    year: 2023
    title: "The Lightning Network Grew by 1212% in 2 Years (River Lightning Report 2023)"
    venue: river.com
    type: company/vendor claim
    identifier: https://www.river.com/learn/files/river-lightning-report-2023.pdf
    url: https://www.river.com/learn/files/river-lightning-report-2023.pdf
    accessed: 2026-11-26
    supports: "99.7% success over 308k payments Aug 2023; 6.6M routed tx Aug 2023; 1:8 non-custodial to custodial users Sept 2023; 279k to 1.116M MAU"
  - key: romiti-2021
    authors: Matteo Romiti, Friedhelm Victor, Pedro Moreno-Sanchez, Peter Sebastian Nordholt, Bernhard Haslhofer, Matteo Maffei
    year: 2021
    title: "Cross-Layer Deanonymization Methods in the Lightning Protocol"
    venue: Financial Cryptography 2021 (arXiv v3)
    type: peer-reviewed
    identifier: arXiv:2007.00764
    url: https://arxiv.org/abs/2007.00764
    accessed: 2026-11-26
    supports: "45.97% of LN nodes linked to 29.61% of LN-interacting BTC addresses; 5 actors control over 33% of capacity"
  - key: kappos-2021
    authors: George Kappos, Haaroon Yousaf, Ania Piotrowska, Sanket Kanjalkar, Sergi Delgado-Segura, Andrew Miller, Sarah Meiklejohn
    year: 2021
    title: "An Empirical Analysis of Privacy in the Lightning Network"
    venue: Financial Cryptography 2021 (arXiv v3)
    type: peer-reviewed
    identifier: arXiv:2003.12470
    url: https://arxiv.org/abs/2003.12470
    accessed: 2026-11-26
    supports: "Attacks using public information reveal node balances and payment sender/recipient"
  - key: kappos-2022
    authors: George Kappos, Haaroon Yousaf, Rainer Stutz, Sofia Rollet, Bernhard Haslhofer, Sarah Meiklejohn
    year: 2022
    title: "How to Peel a Million: Validating and Expanding Bitcoin Clusters"
    venue: USENIX Security 2022, pp. 2207-2223
    type: peer-reviewed
    identifier: https://www.usenix.org/conference/usenixsecurity22/presentation/kappos
    url: https://www.usenix.org/conference/usenixsecurity22/presentation/kappos
    accessed: 2026-11-26
    supports: "Peel-chain heuristic and ML validation of clustering against ground truth"
  - key: meiklejohn-2013
    authors: Sarah Meiklejohn, Marjori Pomarole, Grant Jordan, Kirill Levchenko, Damon McCoy, Geoffrey M. Voelker, Stefan Savage
    year: 2013
    title: "A Fistful of Bitcoins: Characterizing Payments Among Men with No Names"
    venue: ACM IMC 2013, Barcelona
    type: peer-reviewed
    identifier: https://smeiklej.com/files/imc13.pdf
    url: https://smeiklej.com/files/imc13.pdf
    accessed: 2026-11-26
    supports: "Ownership anonymous but flows globally visible; heuristic clustering plus re-identification by purchases"
  - key: bip341
    authors: Pieter Wuille, Jonas Nick, Anthony Towns
    year: 2020
    title: "BIP 341: Taproot: SegWit version 1 spending rules"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
    accessed: 2026-11-26
    supports: "Key-path spends indistinguishable from single-key; only executed script leaf revealed"
  - key: ishares-ibit-csv
    authors: BlackRock / iShares
    year: 2026
    title: "iShares Bitcoin Trust ETF (IBIT) fund holdings file"
    venue: ishares.com
    type: company/vendor claim
    identifier: https://www.ishares.com/us/products/333011/ibit/latest-holdings.csv
    url: https://www.ishares.com/us/products/333011/ibit/latest-holdings.csv
    accessed: 2026-11-26
    supports: "749,654.27 BTC, market value $44.497B as of 2026-11-24 (implied price $59,357)"
  - key: ishares-ibit
    authors: BlackRock / iShares
    year: 2026
    title: "iShares Bitcoin Trust ETF (IBIT) product page"
    venue: ishares.com
    type: company/vendor claim
    identifier: https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf-ibit
    url: https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf-ibit
    accessed: 2026-11-26
    supports: "Net assets $44,929,927,533 as of 2026-11-25; basket 22.63 BTC"
  - key: bitcointreasuries
    authors: BNET Media (BitcoinTreasuries.NET)
    year: 2026
    title: "Bitcoin Treasuries: public companies and category totals"
    venue: bitcointreasuries.net
    type: dataset
    identifier: https://bitcointreasuries.net/
    url: https://bitcointreasuries.net/
    accessed: 2026-11-26
    supports: "Category totals (public 1,239,002; private 201,884; government 645,639; ETFs and exchanges 1,589,940; DeFi 376,202); Strategy 851,305"
  - key: bitcointreasuries-gov
    authors: BNET Media (BitcoinTreasuries.NET)
    year: 2026
    title: "Governments holding bitcoin"
    venue: bitcointreasuries.net
    type: dataset
    identifier: https://bitcointreasuries.net/governments
    url: https://bitcointreasuries.net/governments
    accessed: 2026-11-26
    supports: "US 328,372; China 190,000; UK 61,245 BTC; total 645,639"
  - key: bitcointreasuries-etf
    authors: BNET Media (BitcoinTreasuries.NET)
    year: 2026
    title: "ETFs and exchanges holding bitcoin"
    venue: bitcointreasuries.net
    type: dataset
    identifier: https://bitcointreasuries.net/etfs-and-exchanges
    url: https://bitcointreasuries.net/etfs-and-exchanges
    accessed: 2026-11-26
    supports: "IBIT 785,531 (aggregator, conflicts with fund file), FBTC 184,058, GBTC 131,528, BTC mini 62,874, BITB 38,189, ARKB 35,026"
  - key: sec-mstr
    authors: Strategy Inc.
    year: 2026
    title: "Form 8-K, 2026-11-09"
    venue: SEC EDGAR
    type: company/vendor claim
    identifier: https://www.sec.gov/Archives/edgar/data/0001050446/000119312526452693/mstr-20261109.htm
    url: https://www.sec.gov/Archives/edgar/data/0001050446/000119312526452693/mstr-20261109.htm
    accessed: 2026-11-26
    supports: "850,364 BTC aggregate, $64.16B cost, $75,456 average, 1,036 BTC bought 2026-11-02 to 08"
  - key: theblock-mstr
    authors: The Block
    year: 2026
    title: "'This dip could use a little orange': Strategy buys another 485 BTC"
    venue: The Block
    type: news
    identifier: https://theblock.co/news/business/2026-11-16-this-dip-could-use-a-little-orange-michael-saylor-strategy-bitcoin-tumbles-440886
    url: https://theblock.co/news/business/2026-11-16-this-dip-could-use-a-little-orange-michael-saylor-strategy-bitcoin-tumbles-440886
    accessed: 2026-11-26
    supports: "850,849 BTC as of 2026-11-15; BTC below $65k that weekend"
  - key: adler-20261118
    authors: Axel Adler Jr.
    year: 2026
    title: "Weekly net exchange outflow reaches 14K BTC"
    venue: axeladlerjr.com
    type: essay/blog
    identifier: https://axeladlerjr.com/weekly-net-exchange-outflow-reaches-14k-btc.md
    url: https://axeladlerjr.com/weekly-net-exchange-outflow-reaches-14k-btc.md
    accessed: 2026-11-26
    supports: "Exchange addresses hold 2.85M BTC (2026-11-18); 7-day netflow -14.3K BTC"
  - key: b10c-2025
    authors: 0xB10C
    year: 2025
    title: "Bitcoin Mining Centralization in 2025"
    venue: b10c.me
    type: essay/blog
    identifier: https://b10c.me/blog/015-bitcoin-mining-centralization/
    url: https://b10c.me/blog/015-bitcoin-mining-centralization/
    accessed: 2026-11-26
    supports: "AntPool & friends about 40% (2024); six template producers mine over 95% of blocks; centralisation history"
  - key: b10c-ofac
    authors: 0xB10C
    year: 2025
    title: "Fifteen OFAC-sanctioned transactions missing from blocks"
    venue: b10c.me
    type: essay/blog
    identifier: https://b10c.me/observations/13-missing-sanctioned-transactions-2024-12/
    url: https://b10c.me/observations/13-missing-sanctioned-transactions-2024-12/
    accessed: 2026-11-26
    supports: "15 missing sanctioned tx in 14 blocks, 11 F2Pool; F2Pool may be filtering again; censorship resistance holding"
  - key: bnoc-reorg
    authors: 0xB10C, Anthony Towns, Matthias Grundmann, David Gumberg, Zawy12 (Bitcoin Network Operations Collective)
    year: 2026
    title: "Two-block reorg at height 941880"
    venue: bnoc (b10c mirror)
    type: essay/blog
    identifier: https://mirror.b10c.me/bnoc-xyz/2026-03-23-two-block-reorg-at-height-941880-id97.html
    url: https://mirror.b10c.me/bnoc-xyz/2026-03-23-two-block-reorg-at-height-941880-id97.html
    accessed: 2026-11-26
    supports: "2026-03-23 two-block reorg 941,881 to 941,882; prior two-block reorgs 2013, 2015, 2020, 2023"
  - key: bip50
    authors: Gavin Andresen
    year: 2013
    title: "BIP 50: March 2013 Chain Fork Post-Mortem"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0050.mediawiki
    url: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0050.mediawiki
    accessed: 2026-11-26
    supports: "0.8 chain had about 60% hashpower; one large double spend succeeded; resolved by pool downgrades"
  - key: crypto51
    authors: crypto51.app
    year: 2026
    title: "Cost of a 51% Attack for Different Cryptocurrencies"
    venue: crypto51.app
    type: dataset
    identifier: https://www.crypto51.app/
    url: https://www.crypto51.app/
    accessed: 2026-11-26
    supports: "BTC 1,082,363 PH/s; theoretical 1h attack cost $1,843,332; NiceHash-able 0%"
  - key: hri-20261116
    authors: Hashrate Index (Luxor)
    year: 2026
    title: "Hashrate Index Roundup (November 16, 2026)"
    venue: hashrateindex.com
    type: company/vendor claim
    identifier: https://hashrateindex.com/blog/hashrate-index-roundup-november-16-2026/
    url: https://hashrateindex.com/blog/hashrate-index-roundup-november-16-2026/
    accessed: 2026-11-26
    supports: "Hashprice $30.45/PH/day; energy hashprice $39 to $105/MWh; fees 0.71% of rewards; 7d SMA 967 EH/s; difficulty 134.82T"
  - key: hri-s21
    authors: Hashrate Index (Luxor)
    year: 2026
    title: "Bitmain Antminer S21 (200 TH) specifications"
    venue: hashrateindex.com
    type: company/vendor claim
    identifier: https://hashrateindex.com/rigs/bitmain-antminer-s21
    url: https://hashrateindex.com/rigs/bitmain-antminer-s21
    accessed: 2026-11-26
    supports: "200 TH/s, 3,500 W, 17.5 J/TH"
  - key: ct-bitmain
    authors: Cointelegraph
    year: 2025
    title: "Bitmain slashes ASIC prices amid mining turmoil"
    venue: Cointelegraph
    type: news
    identifier: https://cointelegraph.com/news/bitmain-slashes-asic-prices-mining-turmoil
    url: https://cointelegraph.com/news/bitmain-slashes-asic-prices-mining-turmoil
    accessed: 2026-11-26
    supports: "2025-12-26: S21 immersion discounted to about $7 per TH/s; hashprice near $35/TH/day multi-year low"
  - key: coindesk-1zh
    authors: CoinDesk
    year: 2025
    title: "Bitcoin hashrate surpasses 1 zettahash as miner revenue hits record low"
    venue: CoinDesk
    type: news
    identifier: https://www.coindesk.com/markets/2025/04/07/bitcoin-hashrate-surpasses-1-zettahash-as-miner-revenue-hits-record-low
    url: https://www.coindesk.com/markets/2025/04/07/bitcoin-hashrate-surpasses-1-zettahash-as-miner-revenue-hits-record-low
    accessed: 2026-11-26
    supports: "Glassnode: 1 ZH/s on Friday (2025-04-04); 7-day MA 879 EH/s; prior record 975 EH/s; hashprice $42.40"
  - key: forklog-1zh
    authors: ForkLog
    year: 2025
    title: "Bitcoin hashrate surpasses one zettahash for the first time"
    venue: ForkLog
    type: news
    identifier: https://forklog.com/en/bitcoin-hashrate-surpasses-one-zettahash-for-the-first-time/
    url: https://forklog.com/en/bitcoin-hashrate-surpasses-one-zettahash-for-the-first-time/
    accessed: 2026-11-26
    supports: "Intraday about 1,025 EH/s on 2025-04-04 (Glassnode); 7-day MA 897.6 EH/s on 2025-04-06"
  - key: nakamoto-2008
    authors: Satoshi Nakamoto
    year: 2008
    title: "Bitcoin: A Peer-to-Peer Electronic Cash System"
    venue: bitcoin.org
    type: preprint
    identifier: https://bitcoin.org/bitcoin.pdf
    url: https://bitcoin.org/bitcoin.pdf
    accessed: 2026-11-26
    supports: "Section 11 catch-up probabilities and P<0.1% z-table; section 4 moving-average difficulty"
  - key: budish-2018
    authors: Eric Budish
    year: 2018
    title: "The Economic Limits of Bitcoin and the Blockchain"
    venue: NBER Working Paper 24717
    type: preprint
    identifier: doi:10.3386/w24717
    url: https://www.nber.org/papers/w24717
    accessed: 2026-11-26
    supports: "Flow payments to miners must be large relative to stock attack benefits; Bitcoin majority-attacked if economically important"
  - key: optech-timewarp
    authors: Bitcoin Optech
    year: 2026
    title: "Time warp (topic page)"
    venue: bitcoinops.org
    type: official docs
    identifier: https://bitcoinops.org/en/topics/time-warp/
    url: https://bitcoinops.org/en/topics/time-warp/
    accessed: 2026-11-26
    supports: "Majority can drive difficulty down to six blocks per second after about a month; BIP54 fix"
  - key: bip54
    authors: Antoine Poinsot, Matt Corallo
    year: 2025
    title: "BIP 54: Consensus Cleanup"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0054.md
    url: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0054.md
    accessed: 2026-11-26
    supports: "Timewarp rule (7,200 s grace), sigops limit, 64-byte tx, duplicate coinbase; status Complete; no activation height"
  - key: bip360
    authors: Hunter Beast, Ethan Heilman, Isabel Foxen Duke
    year: 2026
    title: "BIP 360: Pay-to-Merkle-Root (P2MR)"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki
    accessed: 2026-11-26
    supports: "Draft, v0.12.1, assigned 2024-12-18; removes key path; resists long-exposure attacks only; no PQ signatures"
  - key: bip360-history
    authors: GitHub (bitcoin/bips commit log)
    year: 2026
    title: "Commit history for bip-0360.mediawiki"
    venue: GitHub API
    type: code
    identifier: https://api.github.com/repos/bitcoin/bips/commits?path=bip-0360.mediawiki
    url: https://api.github.com/repos/bitcoin/bips/commits?path=bip-0360.mediawiki
    accessed: 2026-11-26
    supports: "Merged 2026-02-11 (PR #1670) as P2MR; last change 2026-08-03"
  - key: bitcoindev-bip360
    authors: Hunter Beast
    year: 2025
    title: "Major BIP 360 Update"
    venue: Bitcoin Development Mailing List
    type: essay/blog
    identifier: https://groups.google.com/g/bitcoindev/c/3JWQwnMUetg
    url: https://groups.google.com/g/bitcoindev/c/3JWQwnMUetg
    accessed: 2026-11-26
    supports: "2025-12-19 rewrite, renamed Pay-to-Tapscript-Hash (P2TSH); no PQ signatures"
  - key: bip361
    authors: Jameson Lopp, Christian Papathanasiou, Ian Smith, Joe Ross, Steve Vaile, Pierre-Luc Dallaire-Demers
    year: 2026
    title: "BIP 361: Post Quantum Migration and Legacy Signature Sunset"
    venue: bitcoin/bips
    type: standard/BIP/RFC/spec
    identifier: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0361.mediawiki
    url: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0361.mediawiki
    accessed: 2026-11-26
    supports: "Draft assigned 2026-02-11; Phase A/B sunset; claims over 34% of BTC had revealed pubkeys as of 2026-03-01"
  - key: glassnode-quantum
    authors: Glassnode Research
    year: 2026
    title: "Measuring Bitcoin's Quantum-Exposed Supply"
    venue: Glassnode
    type: company/vendor claim
    identifier: https://research.glassnode.com/measuring-bitcoins-quantum-exposed-supply/
    url: https://research.glassnode.com/measuring-bitcoins-quantum-exposed-supply/
    accessed: 2026-11-26
    supports: "2026-05-20: 6.04M BTC (30.2%) exposed at rest; structural 1.92M; operational 4.12M; exchanges 1.63 to 1.66M"
  - key: babbush-2026
    authors: Ryan Babbush, Adam Zalcman, Craig Gidney, Michael Broughton, Tanuj Khattar, Hartmut Neven, Thiago Bergamaschi, Justin Drake, Dan Boneh
    year: 2026
    title: "Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations"
    venue: arXiv
    type: preprint
    identifier: arXiv:2603.28846
    url: https://arxiv.org/abs/2603.28846
    accessed: 2026-11-26
    supports: "256-bit ECDLP under 1,200 logical qubits / 90M Toffoli; under 500k physical qubits, minutes; ZK-proof validation"
  - key: cambridge-2025
    authors: Cambridge Centre for Alternative Finance (Cambridge Judge Business School)
    year: 2025
    title: "Cambridge study: sustainable energy rising in bitcoin mining (Cambridge Digital Mining Industry Report)"
    venue: Cambridge Judge Business School
    type: official docs
    identifier: https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/
    url: https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/
    accessed: 2026-11-26
    supports: "138 TWh, 0.5% of global, 39.8 MtCO2e, 52.4% sustainable, US 75.4%; survey of 48% of activity; 2025-04-28"
  - key: cryptonews-ccaf
    authors: Olivia Stephanie (crypto.news)
    year: 2026
    title: "Hydropower overtakes gas as Bitcoin mining power use jumps 38%"
    venue: crypto.news
    type: news
    identifier: https://crypto.news/hydropower-overtakes-gas-as-bitcoin-mining-power-use-jumps-38/
    url: https://crypto.news/hydropower-overtakes-gas-as-bitcoin-mining-power-use-jumps-38/
    accessed: 2026-11-26
    supports: "Preliminary CCAF: about 190 TWh annualised Dec 2025; 48 Mt CO2e; 59.4% low-carbon (2026-07-26)"
  - key: iea-2025
    authors: International Energy Agency
    year: 2025
    title: "Energy and AI: Executive summary"
    venue: IEA
    type: official docs
    identifier: https://www.iea.org/reports/energy-and-ai/executive-summary
    url: https://www.iea.org/reports/energy-and-ai/executive-summary
    accessed: 2026-11-26
    supports: "Data centres 415 TWh in 2024 (1.5%); about 945 TWh by 2030; US 45%, China 25%, Europe 15%"
  - key: iea-2026
    authors: International Energy Agency
    year: 2026
    title: "Key Questions on Energy and AI: Executive summary"
    venue: IEA
    type: official docs
    identifier: https://iea.org/reports/key-questions-on-energy-and-ai/executive-summary
    url: https://iea.org/reports/key-questions-on-energy-and-ai/executive-summary
    accessed: 2026-11-26
    supports: "Data centres +17% in 2025 to 485 TWh; 950 TWh by 2030 (about 3%); AI-focused data centres +50% in 2025"
  - key: euronews-weo
    authors: Euronews
    year: 2026
    title: "Data centre energy consumption could double by 2030, straining grids, IEA warns"
    venue: Euronews
    type: news
    identifier: https://www.euronews.com/2026/11/19/data-centre-energy-consumption-could-double-by-2030-straining-grids-iea-warns
    url: https://www.euronews.com/2026/11/19/data-centre-energy-consumption-could-double-by-2030-straining-grids-iea-warns
    accessed: 2026-11-26
    supports: "WEO 2026 Stated Policies: about 1,000 TWh by 2030"
  - key: corz-pr
    authors: Core Scientific, Inc.
    year: 2025
    title: "Core Scientific and CoreWeave Announce $1.2 Billion Expansion at Denton, TX Site"
    venue: Core Scientific investor relations
    type: company/vendor claim
    identifier: https://investors.corescientific.com/news-events/press-releases/detail/110/core-scientific-and-coreweave-expand-partnership-with-new-70-mw-contract
    url: https://investors.corescientific.com/news-events/press-releases/detail/110/core-scientific-and-coreweave-expand-partnership-with-new-70-mw-contract
    accessed: 2026-11-26
    supports: "2025-02-26: +70 MW Denton; about 590 MW across six sites; $10.2B projected over 12-year terms"
  - key: theblock-corz
    authors: The Block
    year: 2025
    title: "Core Scientific shareholder vote sinks $9 billion CoreWeave deal"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/news/deals/2025-10-30-core-scientific-vote-sinks-9-billion-coreweave-deal-halting-merger-ai-cloud-bitcoin-miner-376959
    url: https://www.theblock.co/news/deals/2025-10-30-core-scientific-vote-sinks-9-billion-coreweave-deal-halting-merger-ai-cloud-bitcoin-miner-376959
    accessed: 2026-11-26
    supports: "2025-10-30 vote rejected about $9B all-stock merger at 0.1235 ratio"
  - key: terawulf-pr
    authors: TeraWulf Inc.
    year: 2025
    title: "TeraWulf Signs 200+ MW, 10-Year AI Hosting Agreements with Fluidstack"
    venue: GlobeNewswire / TeraWulf IR (PDF)
    type: company/vendor claim
    identifier: https://d1io3yog0oux5.cloudfront.net/_feb0a76e67864434a1559c67c13db5b2/terawulf/news/2025-08-14_TeraWulf_Signs_200_MW_10_Year_AI_Hosting_112.pdf
    url: https://d1io3yog0oux5.cloudfront.net/_feb0a76e67864434a1559c67c13db5b2/terawulf/news/2025-08-14_TeraWulf_Signs_200_MW_10_Year_AI_Hosting_112.pdf
    accessed: 2026-11-26
    supports: "2025-08-14: over 200 MW IT, 10 yr, about $3.7B (up to $8.7B), Google $1.8B backstop, about 8% equity"
  - key: terawulf-2026
    authors: TeraWulf Inc.
    year: 2026
    title: "TeraWulf Secures Google Credit Backstop for Project Financing in Support of $19 Billion Anthropic Lease"
    venue: finviz (press release syndication)
    type: company/vendor claim
    identifier: https://finviz.com/news/415380/terawulf-secures-google-credit-backstop-for-project-financing-in-support-of-19-billion-anthropic-lease-executes-definitive-fluor-epc-agreement
    url: https://finviz.com/news/415380/terawulf-secures-google-credit-backstop-for-project-financing-in-support-of-19-billion-anthropic-lease-executes-definitive-fluor-epc-agreement
    accessed: 2026-11-26
    supports: "2026-11-04: about $19B Anthropic lease commitments at Hawesville KY; Google credit support; Fluor EPC"
  - key: theblock-cipher
    authors: The Block
    year: 2025
    title: "Bitcoin miner Cipher signs $3 billion Google-backed AI hosting deal over ten years"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/post/372315/cipher-mining-google-backed-3-billion-usd-ai-hosting-deal
    url: https://www.theblock.co/post/372315/cipher-mining-google-backed-3-billion-usd-ai-hosting-deal
    accessed: 2026-11-26
    supports: "2025-09-25: 168 MW IT, 10 yr, about $3B, Google $1.4B backstop for about 5.4%, Barber Lake TX"
  - key: davispolk-cipher
    authors: Davis Polk & Wardwell
    year: 2025
    title: "Cipher Mining 300 MW, $5.5 billion lease agreement with Amazon Web Services"
    venue: davispolk.com
    type: company/vendor claim
    identifier: https://www.davispolk.com/experience/cipher-mining-300-mw-5-5-billion-lease-agreement-amazon-web-services
    url: https://www.davispolk.com/experience/cipher-mining-300-mw-5-5-billion-lease-agreement-amazon-web-services
    accessed: 2026-11-26
    supports: "15-year AWS lease, 300 MW gross, about $5.5B (posted 2025-11-05)"
  - key: iren-yahoo
    authors: Yahoo Finance
    year: 2025
    title: "IREN signs Microsoft to $9.7 billion cloud compute deal"
    venue: Yahoo Finance
    type: news
    identifier: https://finance.yahoo.com/news/iren-signs-microsoft-9-7-132523930.html
    url: https://finance.yahoo.com/news/iren-signs-microsoft-9-7-132523930.html
    accessed: 2026-11-26
    supports: "2025-11-03: about $9.7B, 5 yr, GB300, 20% prepayment, $5.8B Dell, Childress TX 750 MW / 200 MW IT"
  - key: hut8-pr
    authors: Hut 8 Corp.
    year: 2025
    title: "Hut 8 Signs 15-Year, 245 MW AI Data Center Lease at River Bend Campus with Total Contract Value of USD $7.0 Billion"
    venue: Hut 8 press release
    type: company/vendor claim
    identifier: https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion
    url: https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion
    accessed: 2026-11-26
    supports: "2025-12-17: 245 MW IT, 15 yr, $7.0B (up to $17.7B), Fluidstack tenant, Google backstop, Louisiana"
  - key: laurie-clayton-2004
    authors: Ben Laurie, Richard Clayton
    year: 2004
    title: "'Proof-of-Work' Proves Not to Work"
    venue: Workshop draft dated 3 May 2004 (commonly cited as WEIS 2004; venue not stated in the PDF)
    type: peer-reviewed
    identifier: https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf
    url: https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf
    accessed: 2026-11-26
    supports: "PoW difficulty that stops spam would block legitimate senders; need orders of magnitude gap; attributes idea to Dwork-Naor 1992 and hashcash to Back"
  - key: ball-2017
    authors: Marshall Ball, Alon Rosen, Manuel Sabin, Prashant Nalini Vasudevan
    year: 2017
    title: "Proofs of Useful Work"
    venue: IACR ePrint 2017/203 (revised 2021)
    type: preprint
    identifier: https://eprint.iacr.org/2017/203
    url: https://eprint.iacr.org/2017/203
    accessed: 2026-11-26
    supports: "PoUW from OV, 3SUM, APSP; definition satisfied by naive construction per 2018 update"
  - key: komargodski-2025
    authors: Ilan Komargodski, Omri Weinstein
    year: 2025
    title: "Proofs of Useful Work from Arbitrary Matrix Multiplication"
    venue: arXiv
    type: preprint
    identifier: arXiv:2504.09971
    url: https://arxiv.org/abs/2504.09971
    accessed: 2026-11-26
    supports: "MatMul PoUW with 1+o(1) overhead; security conjectured"
  - key: jia-2021
    authors: Hengrui Jia, Mohammad Yaghini, Christopher A. Choquette-Choo, Natalie Dullerud, Anvith Thudi, Varun Chandrasekaran, Nicolas Papernot
    year: 2021
    title: "Proof-of-Learning: Definitions and Practice"
    venue: IEEE S&P 2021 (arXiv)
    type: peer-reviewed
    identifier: arXiv:2103.05633
    url: https://arxiv.org/abs/2103.05633
    accessed: 2026-11-26
    supports: "PoL proves compute spent to obtain parameters"
  - key: fang-2023
    authors: Congyu Fang, Hengrui Jia, Anvith Thudi, Mohammad Yaghini, Christopher A. Choquette-Choo, Natalie Dullerud, Varun Chandrasekaran, Nicolas Papernot
    year: 2023
    title: "Proof-of-Learning is Currently More Broken Than You Think"
    venue: IEEE EuroS&P 2023 (arXiv)
    type: peer-reviewed
    identifier: arXiv:2208.03567
    url: https://arxiv.org/abs/2208.03567
    accessed: 2026-11-26
    supports: "PoL not robust; cheap spoofs; provably robust PoL needs open learning-theory advances"
  - key: gensyn
    authors: Gensyn
    year: 2022
    title: "Gensyn Litepaper"
    venue: docs.gensyn.ai
    type: company/vendor claim
    identifier: https://docs.gensyn.ai/litepaper
    url: https://docs.gensyn.ai/litepaper
    accessed: 2026-11-26
    supports: "Probabilistic PoL, pinpoint protocol, Truebit-style staking; marketplace verification, not ledger consensus; marked out of date"
  - key: primecoin-code
    authors: Primecoin developers
    year: 2013
    title: "primecoin/primecoin repository"
    venue: GitHub
    type: code
    identifier: https://github.com/primecoin/primecoin
    url: https://github.com/primecoin/primecoin
    accessed: 2026-11-26
    supports: "Scientific computing proof-of-work searching for prime number chains"
  - key: sastry-2024
    authors: Girish Sastry, Lennart Heim, Haydn Belfield, Markus Anderljung, Miles Brundage, et al.
    year: 2024
    title: "Computing Power and the Governance of Artificial Intelligence"
    venue: arXiv
    type: preprint
    identifier: arXiv:2402.08797
    url: https://arxiv.org/abs/2402.08797
    accessed: 2026-11-26
    supports: "Compute is detectable, excludable, quantifiable; abstract does not involve PoW"
  - key: catena-2017
    authors: Alin Tomescu, Srinivas Devadas
    year: 2017
    title: "Catena: Efficient Non-equivocation via Bitcoin"
    venue: IEEE S&P 2017 (IACR ePrint 2016/1062)
    type: peer-reviewed
    identifier: doi:10.1109/SP.2017.19
    url: https://eprint.iacr.org/2016/1062
    accessed: 2026-11-26
    supports: "OP_RETURN chain logs; equivocation requires double spend; auditor bandwidth 90 GB to tens of MB"
  - key: todd-2017
    authors: Peter Todd
    year: 2017
    title: "Scalable Semi-Trustless Asset Transfer via Single-Use-Seals and Proof-of-Publication"
    venue: petertodd.org
    type: essay/blog
    identifier: https://petertodd.org/2017/scalable-single-use-seal-asset-transfer
    url: https://petertodd.org/2017/scalable-single-use-seal-asset-transfer
    accessed: 2026-11-26
    supports: "Single-use seal closed over a message exactly once; Bitcoin outpoints as seals"
  - key: belcher-2019
    authors: Chris Belcher
    year: 2019
    title: "Design for improving JoinMarket's resistance to sybil attacks using fidelity bonds"
    venue: GitHub Gist
    type: essay/blog
    identifier: https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af
    url: https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af
    accessed: 2026-11-26
    supports: "Timelocked/burned fidelity bonds; V^2 valuation; sybil cost 30k to 80k BTC for 6 months; proof by TXID and vout"
  - key: ietf-scitt-anchor
    authors: J. Fassbender (Umarise)
    year: 2026
    title: "Bitcoin-Anchored Temporal Proof for Transparency Services (draft-fassbender-scitt-time-anchor-03)"
    venue: IETF Internet-Draft
    type: standard/BIP/RFC/spec
    identifier: draft-fassbender-scitt-time-anchor-03
    url: https://www.ietf.org/archive/id/draft-fassbender-scitt-time-anchor-03.html
    accessed: 2026-11-26
    supports: "OpenTimestamps anchoring for SCITT; block-height binding; MIN_CONFIRMATIONS 6; model-weights motivating example; no equivocation claim for bare roots"
  - key: petrie-2024
    authors: James Petrie
    year: 2024
    title: "Near-Term Enforcement of AI Chip Export Controls Using A Firmware-Based Design for Offline Licensing"
    venue: arXiv
    type: preprint
    identifier: arXiv:2404.18308
    url: https://arxiv.org/abs/2404.18308
    accessed: 2026-11-26
    supports: "Chips disabled unless they hold an unused regulator license; firmware features needed; no blockchain"
  - key: petrie-2025
    authors: James Petrie
    year: 2025
    title: "Embedded Off-Switches for AI Compute"
    venue: arXiv
    type: preprint
    identifier: arXiv:2509.07637
    url: https://arxiv.org/html/2509.07637
    accessed: 2026-11-26
    supports: "Nonce-based licences and usage-allowance counters; no trusted clock; no ledger"
```
