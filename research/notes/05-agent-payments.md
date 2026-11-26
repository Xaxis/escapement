# Agent payments, delegated authority, and agent-held money (state as of 2026-11-26)

Scope: how AI agents pay, hold money and receive delegated authority today; which controls each protocol has (caps, budgets, destination limits, expiry, revocation, approval, logs) and who enforces them; agents holding crypto in the wild; incidents; agents acquiring resources; delegated-authority standards. Written for Escapement (can Bitcoin cap what an agent can spend, commit to, or bind itself to).

Labels used for numbers: **[measured]** independent measurement; **[measured-sim]** measured in simulation by the publishing lab; **[vendor]** claim by an interested party; **[news]** reported by press, primary not opened; **[derived]** my arithmetic, shown. "Exists" means shipped docs, code or spec I opened; "proposed/announced" means press release, draft, or forum post only. All URLs below were opened by me on 2026-11-26 unless listed under "Unverified".

## Comparison table: controls per protocol (as documented in the sources opened)

| Protocol / product (status, date) | Rail | Spending cap | Per-period budget | Merchant / destination limit | Expiry | Revocation | Human approval | Audit trail | Who enforces |
|---|---|---|---|---|---|---|---|---|---|
| L402 (bLIP-0026) + Aperture + Lightning Agent Tools (exists; tools 2026-02-11) | Lightning (BTC) | `lnget --max-cost` per request; macaroon "spending caps" caveat (500-sat pay-only example); bakery can "cap total spending at the Lightning node level" | Not documented | Macaroon "service restrictions" caveat; pay-only role does not restrict payee (not documented) | "time-based expiration" caveat | Mentioned ("until it expires or is revoked"), mechanism not documented | None described | None described in agent tools | Seller: Aperture verifies token + preimage. Buyer: agent's own LND node checks macaroon; keys on remote signer |
| x402 (v2; Linux Foundation project since 2026-07-14) | Stablecoins, 99.6% USDC by volume | Per-request signed `amount` (`exact`) or ceiling (`upto`) | None in protocol | `payTo` signed into authorization | `maxTimeoutSeconds`; EIP-3009 `validAfter`/`validBefore` | Not applicable (one-shot authorization lapses) | None in protocol ("no human approves payments", TRM) | Public on-chain settlement | Client wallet signs; facilitator `/verify` + `/settle`; token contract enforces time window |
| Google AP2 (v0.1 2025-09-16; spec page now v0.2) | Cards, bank, stablecoin (A2A x402 extension) | Intent Mandate "price limits" (v0.1); no numeric cap field in mirrored v0.1 schema; v0.2 extensible "constraints" | Not defined | `merchants`, `skus` lists (v0.1) | `intent_expiry`, `cart_expiry` (v0.1); `exp` on open mandates (v0.2) | Not described | `user_cart_confirmation_required` (default true); v0.2 non-agentic "Trusted Surface" | Signed mandates + receipts, "non-repudiable" | Merchant, credential provider, network, processor, "in deterministic code" |
| OpenAI/Stripe ACP via Stripe Shared Payment Token (preview API 2026-09-30) | Cards, Link, wallets, Klarna, Affirm | `usage_limits[max_amount]` | None (per-transaction token) | Scoped to one seller `network_business_profile` | `usage_limits[expires_at]` | `POST .../revoke`; terminal `deactivated` state | ChatGPT: customer approves each purchase; 3DS `requires_action` | Webhooks: `used`, `deactivated`, `requires_action` | Stripe (PSP) |
| Stripe Issuing for agents (exists; access by application) | Card networks | `spending_limits` per_authorization | `monthly` etc. ("rolling period") | `allowed_categories` (MCC) | Single-use cards auto-invalidate | Freeze `status=inactive` | Real-time authorization webhook, 2 s default timeout then default rules | Full transaction records; disputes within 110 days | Stripe as issuer + principal's own webhook |
| Visa Intelligent Commerce + Trusted Agent Protocol (announced 2025-04-30; TAP spec published) | Visa cards | Consumer "spending limits and conditions" | Not specified | Tokens "bound to that agent" | TAP signature `created`/`expires` at most 8 min apart; ID token `exp` | No revocation process described (expiry only) | Consumer instructs activation of credential | "Commerce signals" to Visa | Visa ("effect transaction controls"); merchant or CDN verifies signatures |
| Mastercard Agent Pay (announced 2025-04-29) | Mastercard | Not specified in release | Not specified | "complete control over what the agent is allowed to purchase" | Not specified in release | Not specified | Not specified | Not specified | Mastercard; agents "registered and verified" |
| PayPal Agent Toolkit (code, 2025) | PayPal | None documented | None | None | OAuth token ~8 h (production) | Not documented | None documented | `list_transactions` tool | Tool enable flags in `configuration.actions` only |
| Coinbase CDP wallet policies / Agentic Wallets (Agentic Wallets 2026-02-11) | EVM, Solana | `ethValue` criteria; "session caps" (news) | Not in policy overview | `evmAddress` allow/deny lists | Not documented | Policies editable/pausable | None documented | Not covered | Coinbase signing service (custodial infrastructure, "enclave isolation") |
| ERC-4337/7579 Smart Sessions; ERC-7715 (draft) | EVM | `valueLimitPerUse`; "caps per action and total" | `usageLimit` per period | Contract and function-selector allowlists | `timeframe` `validUntil`; 7715 `expiry` rule | `wallet_revokeExecutionPermission` (7715) | Not built in | On-chain | Smart-account validation contracts ("Smart contracts enforce limits") |
| Safe multisig with agent signer (docs) | EVM | Threshold, not amount | n/a | n/a | n/a | Remove signer | Threshold chosen so at least one human signs | Safe Transaction Service + chain | Safe contract threshold |
| Nostr Wallet Connect NIP-47 / Alby Hub | Lightning | Per-connection budget; `QUOTA_EXCEEDED` | Budget renewal period (user-defined in Alby Hub) | None | Connection expiration date; per-request `expiration` tag | Keys "revoked and created at will" | None | Per-connection activity list | Wallet service (Alby Hub) |
| Fewsats (SDK) | L402 / Lightning, cards | None documented | None | None | None | None | None in `as_tools()` example | Payment status lookups | Fewsats backend ("L402 flow is handled by the backend") |
| Cashu via MCP Money (code) | Cashu ecash over Lightning | None | None | None | None | None | "Lightning payments require explicit confirmation" | None | Agent-side software; nsec in local `.wallet.json` |

Reading of the table (inference): only four families enforce caps outside the agent's own host by design: card issuers/networks (Stripe, Visa, Mastercard), custodial signers (Coinbase), on-chain contracts (smart sessions, Safe), and a separate wallet service (NWC/Alby Hub). L402 buyer-side caps are enforced by the LND node co-located with the agent; x402 has no buyer budget at all.

## 1. Protocols: limits, mandates, expiry, revocation, logs, enforcer

### Takeaway
Every major rail now has an agent story, but the controls differ sharply: card rails (Stripe Issuing, SPT, Visa, Mastercard) have the richest caps, merchant-category limits, revocation and disputes, all enforced by the issuer or PSP; crypto rails (x402, smart sessions) enforce per-request or on-chain policy; Lightning (L402, NWC) offers macaroon caps and renewable budgets enforced by the principal's node or wallet service. Every expiry mechanism found is wall-clock based; none uses block height.

### Cited Findings

**L402, Aperture, Lightning agent tools (Lightning Labs)**
- 2026-02-11: Lightning Labs open-sourced Lightning Agent Tools, seven composable skills: run a node, remote signer, macaroon bakery for scoped credentials, `lnget` L402 client, Aperture for paid endpoints, an MCP server (18 read-only tools), and a commerce meta-skill ([LL-AgentTools-2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/)).
- `lnget --max-cost` sets "a per-request spending ceiling"; the bakery can "cap total spending at the Lightning node level" so an agent "can only ever access the budget you've explicitly granted it"; five preset macaroon roles: pay-only, invoice-only, read-only, channel-admin, signer-only ([LL-AgentTools-2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/)).
- Remote signer: "The signer machine holds the private keys and never routes payments or connects to the public network"; agent machine runs a watch-only LND node over authenticated gRPC; standalone local-key mode is for testnet/regtest/small-value only. No expiry, revocation, human approval or audit features are described on the page ([LL-AgentTools-2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/)).
- 2026-03-11: L402 flow = 402 + `WWW-Authenticate` with token and BOLT 11 invoice; client pays, gets preimage, retries with `Authorization: L402 <token>:<preimage>`; tokens reusable "until it expires or is revoked". Caveats can add "spending caps, service restrictions, or time-based expiration"; example "a pay-only macaroon with a 500-sat spending cap" for a worker agent ([LL-L402Agents-2026](https://lightning.engineering/posts/2026-03-11-L402-for-agents/)).
- bLIP-0026 update (2026-03): `version` parameter (`"0"`), key renamed `macaroon` to `token` (token-agnostic; only requirement is commitment to payment hash), servers may accept both. Verification is local (preimage hash) versus facilitator/on-chain checks in "alternative" protocols; Lightning payments "leave no on-chain footprint". No adoption numbers; Lightning Loop has used L402 via Aperture "since the initial release five years ago" [vendor] ([LL-L402Agents-2026](https://lightning.engineering/posts/2026-03-11-L402-for-agents/)).
- Docs: macaroons "can be attenuated and delegated by the bearer" and "verified using only a root key and basic cryptography"; Aperture is a reverse HTTP proxy issuing macaroons and invoices, with per-request, tiered and surge pricing; no per-period budgets documented ([LL-L402Docs](https://docs.lightning.engineering/the-lightning-network/l402)).
- LangChainBitcoin (Lightning Labs code): tools letting LangChain agents hold on-chain and Lightning balances and pay L402 APIs via a `requests` wrapper; no budget or spending-limit feature on the README; 143 stars, no releases (as viewed 2026-11-26) ([LL-LangChainBitcoin](https://github.com/lightninglabs/LangChainBitcoin)).

**x402 (Coinbase, Cloudflare, now Linux Foundation)**
- Flow: request, 402 with payment requirements, re-request with payment authorization header, facilitator verifies and settles, server returns resource. Cloudflare (2025-09-23) co-founded the x402 Foundation with Coinbase, added x402 to its Agents SDK and MCP servers, and proposed a `deferred` scheme using HTTP Message Signatures for batched later settlement; sites on Cloudflare send "over a billion HTTP 402 response codes" per day [vendor; responses, not payments] ([CF-x402-2025](https://blog.cloudflare.com/x402)).
- Schemes: `exact`, `upto` ("authorizes up to a maximum per request; the seller settles the actual usage, up to that cap"), and EVM `batch-settlement` with escrow and vouchers. Principle: schemes "must not allow for the facilitator or resource server to move funds" beyond client intent. No client-side spending limits in the README ([CB-x402-repo](https://github.com/coinbase/x402)).
- v2 fields: `scheme`, CAIP-2 `network`, `amount`, `asset`, `payTo`, `maxTimeoutSeconds` ("how long the quote is valid to pay"); EIP-3009 `authorization` with `validAfter`, `validBefore`, `nonce`; facilitator rejects when signed value differs from advertised amount ([FB-x402-ref](https://developers.fireblocks.com/docs/x402-protocol-reference.md), third-party implementer docs).
- Governance: Linux Foundation operational launch 2026-07-14 with 40 members, 17 premier incl. Adyen, AWS, American Express, Circle, Cloudflare, Coinbase, Google, Mastercard, Shopify, Solana Foundation, Stripe, Visa; associate members include BSV Association; no Lightning or Bitcoin mention; no transaction numbers cited ([LF-x402-2026](https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications)).
- Adoption, independent: TRM Labs (2026-09-09) counted x402 settlements through known facilitators since May 2025 on Base, Solana, Polygon: USD 52.7M across 198.9M settlement transactions [measured]; USD 25.62M left after commerce screens [measured]; agentic share of screened commerce 0.6% to 7.5% [measured]; 99.6% settled in USDC [measured]; agent-payment volume roughly USD 5,000 to 11,000 per month in 2026 [measured]. TRM: "a script produces the same onchain record as an agent"; attribution hard because "no human approves payments" ([TRM-x402-2026](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain)).
  - Derived: average settlement 52.7M / 198.9M = USD 0.265; screens remove 1 minus 25.62/52.7 = 51.4% of volume; agentic cumulative volume 0.006 to 0.075 x 25.62M = USD 0.15M to 1.92M; annualized 2026 agent volume 12 x 5k to 11k = USD 60k to 132k [derived].
- Adoption, press: 2026-08-04 Forkast (byline states an AI "mind") cites Major Matters' tracker at "over 200 million transactions as of June 2026", Artemis saying "more than 95%" is "protocol signaling", and CoinDesk putting real daily commercial volume at about $28,000 in March 2026 [news]; the linked CoinDesk slug says "nearly half" are artificial, unreconciled ([Forkast-x402-2026](https://forkast.news/the-x402-foundation-activated-a-27-year-old-internet-code-200-million-transactions-later-the-real-volume-is-still-tiny/)). The Block (2026-02-11): x402 "processed 50 million transactions" and x402 2.0 launched December 2025 [news] ([TheBlock-AgenticWallets-2026](https://www.theblock.co/post/389524/coinbase-rolls-out-ai-tool-to-give-any-agent-a-wallet)). Conflict: counts differ by source and scope; TRM is the only independent measurement opened.

**Google Agent Payments Protocol (AP2)**
- 2025-09-16: mandates are "tamper-proof, cryptographically-signed digital contracts" signed by verifiable credentials. Human present: request captured as Intent Mandate, user approval "signs a Cart Mandate". Human not present: user signs a detailed Intent Mandate up front with "price limits, timing, and other conditions", which "can allow the agent to automatically generate a Cart Mandate". Intent to cart to payment "creates a non-repudiable audit trail". 60+ organizations; A2A x402 extension with Coinbase, Ethereum Foundation, MetaMask [vendor] ([Google-AP2-2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)).
- v0.1 mandate schema as mirrored by a third-party Rust crate: `user_cart_confirmation_required` (default true; "If false, the agent can make purchases without further user approval"), `natural_language_description`, `merchants` (None = any), `skus`, `requires_refundability`, `intent_expiry` (ISO 8601); cart `cart_expiry`, `merchant_authorization` JWT; payment `user_authorization` VC. No numeric amount-cap field appears ([a2a-ap2-crate](https://docs.rs/crate/a2a-ap2/0.3.1/source/src/types/mandate.rs), code).
- Current spec page (labeled v0.2, no date): two mandate types, Checkout Mandate and Payment Mandate, SD-JWT; open mandates carry `exp` ("smallest value that lets the agent finish the task") and `cnf` agent key; agent must not present new open mandates until it gets a rejection receipt; user approval on a non-agentic "Trusted Surface"; merchant, credential provider, network and processor each verify; "All validation must run in deterministic code"; no revocation section ([AP2-spec-v0.2](https://ap2-protocol.org/ap2/specification/)).

**OpenAI plus Stripe Agentic Commerce Protocol (Shared Payment Tokens)**
- Agent issues an SPT to a seller's Stripe profile with `usage_limits[currency]`, `usage_limits[expires_at]`, `usage_limits[max_amount]`; revoke "at any time"; states `active`, `requires_action`, terminal `deactivated` ("consumed, expired, or revoked"); webhooks `used`, `deactivated`, `requires_action`; preview API `2026-09-30.preview`; US, Canada and select European countries; Stripe "might use tokens issued through network programs such as Mastercard's Agent Pay and Visa's Intelligent Commerce" ([Stripe-SPT](https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens.md?agent-seller=agent)).
- ChatGPT merchant guide: customer reviews and approves each purchase in ChatGPT; merchant receives a network token and should not reuse it for another purchase ([OpenAI-ChatGPTWallet](https://developers.openai.com/commerce/specs/payment)).

**Stripe Issuing for agents and Agent Toolkit**
- Per-agent virtual cards with `spending_controls[spending_limits]` (`per_authorization`, `monthly`), `allowed_categories` (example: airlines and hotels only), single-use cards "automatically invalidated after use"; every purchase triggers `issuing_authorization.request` with "a 2 second default timeout to respond before Stripe falls back to the card's default rules"; freeze via `status=inactive`; disputes expire if not submitted within 110 days; controls "can be updated at any time" ([Stripe-IssuingAgents](https://docs.stripe.com/issuing/agents)).

**Visa Intelligent Commerce and Trusted Agent Protocol (TAP)**
- 2025-04-30: AI-Ready Cards with tokenized credentials; consumers "set spending limits and conditions"; "Only the consumer can instruct the agent on what to do and when to activate a payment credential"; commerce signals shared with Visa "enabling Visa to effect transaction controls"; partners include Anthropic, IBM, Microsoft, Mistral AI, OpenAI, Perplexity, Samsung, Stripe [vendor] ([Visa-VIC-2025](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html)).
- TAP spec: RFC 9421 signatures with required `@authority`, `@path`, `created`, `keyid`, `expires`, `tag`, `alg`, `nonce`; tags `agent-browser-auth` and `agent-payer-auth`; timestamps "should not be more than 8 minutes apart"; nonce replay check over last 8 minutes; keys served as JWK at `/keys`; Agentic Consumer Recognition Object and Agentic Payment Container (credential hash, payload, or "Browsing IOU" for 402 responses); ID token `exp`; no revocation process, only expiry (the spec's own sample has `created`/`expires` 3600 s apart, which would fail its 8-minute rule) ([Visa-TAP-spec](https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications)). Repo: signatures "valid only for a single use", bound to merchant domain and operation; Agent Registry is a public-key registry ([Visa-TAP-repo](https://github.com/visa/trusted-agent-protocol)).
- Cloudflare (2025-10-24) acts as verifier for Visa TAP and Mastercard Agent Pay; Visa and Mastercard "will each host their own directory"; Cloudflare checks time window and nonce uniqueness ([CF-SecureAgenticCommerce-2025](https://blog.cloudflare.com/secure-agentic-commerce/)).

**Mastercard Agent Pay**
- 2025-04-29: Agentic Tokens built on existing tokenization; "The program will require trusted AI agents to be registered and verified"; "Consumers will have complete control over what the agent is allowed to purchase"; Microsoft, IBM, Braintree, Checkout.com; no specific limits in release [vendor] ([MC-AgentPay-2025](https://newsroom.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai)).

**PayPal Agent Toolkit**
- 43 tools (invoices, `create_order`, `pay_order`, `create_refund`, disputes incl. `accept_dispute_claim`, subscriptions, `list_transactions`); actions toggled by `configuration.actions` flags; defaults to sandbox; production tokens about 8 hours; no spending limits or human approval documented ([PayPal-AgentToolkit](https://github.com/paypal/agent-toolkit/)).

**Coinbase AgentKit, CDP wallet policies, Agentic Wallets**
- CDP policy engine: rules with `accept`/`reject` on operations such as `signEvmTransaction`; criteria `ethValue` (wei, e.g. `<=`) and `evmAddress` (`in` lists as allow/deny); `project` and `account` scopes; reject beats accept; simulation and pause supported; no USD limits, time windows or audit logs documented on the overview ([CDP-Policies](https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/overview)).
- 2026-02-11 Agentic Wallets: "programmable spending limits, session caps, and other transaction controls"; keys kept in Coinbase infrastructure, "never exposed to the agent's prompt or LLM"; EVM and Solana; built on AgentKit and x402 [news] ([TheBlock-AgenticWallets-2026](https://www.theblock.co/post/389524/coinbase-rolls-out-ai-tool-to-give-any-agent-a-wallet)).

**ERC-4337/7579 session keys and ERC-7715**
- ERC-7715 (Draft, created 2024-05-24, requires EIP-4337 and EIP-7710): `wallet_requestExecutionPermissions` with `permission` (e.g. `native-token-allowance`, `erc20-token-allowance`), `isAdjustmentAllowed`, `rules` (only `expiry` defined); `wallet_revokeExecutionPermission`; spec covers "not how the wallet enforces permissions" ([EIP-7715](https://eips.ethereum.org/EIPS/eip-7715)).
- Biconomy Smart Sessions: "scoped, time-limited, revocable permissions"; contract and function allowlists; `universal` policy with `valueLimitPerUse` and usage limits; `timeframe` `validAfter`/`validUntil`; `usageLimit`; "Smart contracts enforce limits. No trust required." [vendor docs] ([Biconomy-Agents](https://docs.biconomy.io/agents-automation)).
- Safe: agent as one owner, thresholds 2-of-3, 3-of-5, 5-of-7 so "at least one human approval is required"; agent proposes via Safe Transaction Service; humans approve in Safe Wallet ([Safe-HumanApproval](https://docs.safe.global/home/ai-agent-quickstarts/human-approval)).

**Nostr Wallet Connect (NIP-47) and Alby Hub**
- NIP-47: commands `pay_invoice`, `make_invoice`, `lookup_invoice`, `get_balance`, `get_info`; optional request `expiration` tag ("If the request is received after this timestamp, it should be ignored"); errors `QUOTA_EXCEEDED` ("exceeded its spending quota"), `RESTRICTED`, `UNAUTHORIZED`; keys "can be revoked and created at will and have arbitrary constraints (eg. budgets)" ([NIP-47](https://github.com/nostr-protocol/nips/blob/master/47.md)).
- `get_budget` proposal (opened 2024-09-18, still open as viewed): separates budget from balance so apps see remaining allowance and next renewal; commits add `renewal_period`; "implemented in Alby Hub and Alby JS SDK" (2024-12-09) ([NIPs-PR1504](https://github.com/nostr-protocol/nips/pull/1504)).
- Alby Hub: per-connection budget ("Left in budget"), renewal period "according to your preferences", optional expiration ("Expires Soon"/"Expired" badges; renew by editing), per-connection activity log ([Alby-AppConnections](https://guides.getalby.com/user-guide/alby-account-and-browser-extension/alby-hub/app-connections)).

**Fewsats; Cashu for agents**
- Fewsats SDK: `pay_offer()` pays a 402 offer ("The L402 flow is handled by the backend"), `pay_lightning()`, `as_tools()` for agents; no limits, budgets or approval rules documented ([Fewsats-py](https://fewsats.github.io/fewsats-python)).
- MCP Money (Cashu + Nostr): tools `get_balance`, `deposit`, `pay`, `zap`, `add_mint`; private key stored in local `.wallet.json`; only control "Lightning payments require explicit confirmation" ([MCPMoney](https://cdn.jsdelivr.net/gh/pablof7z/mcp-money@main/README.md)).

### Inferences
- Card rails give the principal the most levers (MCC limits, per-period caps, real-time veto, revocation, disputes), and the issuer, not the agent, enforces them. Their weakness for Escapement is that enforcement is a trusted third party and policy can be changed "at any time" by whoever holds the account key.
- x402 is per-request only: an agent holding a funded key can sign unlimited `exact` authorizations; any budget must come from the wallet layer (CDP policy, smart session). TRM's finding that "no human approves payments" matches the protocol design.
- L402's buyer-side cap sits in the agent-side LND (watch-only node checks the macaroon); the remote signer as described protects key material but no policy enforcement at the signer is documented. An agent with admin on its host could bake broader macaroons only if it holds a root/admin macaroon; Lightning Labs' preset roles exist to prevent that, but the separation is operational, not cryptographic beyond macaroon root keys.
- NWC/Alby Hub is the closest shipped Bitcoin-side analogue to a renewable allowance: budget + renewal period + expiry enforced by a separate wallet service.
- All expiry is wall-clock: TAP (8 min), SPT `expires_at`, AP2 `intent_expiry`/`exp`, x402 `validBefore`, ERC-7715 `expiry`, NWC `expiration`.

### Gaps
- Exact OpenAI ACP delegated-payment allowance fields and the ACP launch date: the spec URL returned 404; see Unverified.
- Mastercard Agent Pay control details (limits, validity windows): framework page returned 403.
- AP2 v0.1 to v0.2 rename rationale (Intent/Cart to Checkout/Payment) not found; no changelog opened.
- How macaroon revocation works for L402 tokens in Aperture is not documented on pages opened.
- No usage numbers found for L402, NWC budgets, AP2, Visa or Mastercard agent programs.

## 2. AI agents holding crypto in the wild

### Takeaway
The best-known "agent wallets" (Truth Terminal, ai16z/ElizaOS, Virtuals agents, AIXBT) were memecoin phenomena whose value came from token speculation, and human operators sat close to every wallet. ElizaOS's own token was declared dead by its founder in August 2026.

### Cited Findings
- Truth Terminal: created by Andy Ayrey on a custom version of Claude 3 Opus; Marc Andreessen gave it $50,000 in bitcoin in July 2024; GOAT launched 2024-10-10 via pump.fun and reached a fully diluted market cap above $430 million within a week [news]; on 2024-10-18 its GOAT holdings were about $840,000 and total holdings "appear" over $1 million, based on an X post and Solscan [news]; Ayrey and the bot say they did not create GOAT ([TheBlock-TruthTerminal-2024](https://www.theblock.co/post/322002/marc-andreessen-funded-ai-bot-becomes-a-millionaire-after-fartcoin-holdings-rally)). The article does not state who controls the wallet.
- ai16z / ElizaOS: 2026-08-06, founder Shaw Walters: "The token is dead. Completely."; ElizaOS at $0.000285, market cap $2.1 million [news], versus peak $2.5 billion in January 2025 per CoinGecko [news]; Eliza Labs settled a tokenholder suit (Burwick Law) by handing over remaining treasury; the foundation is winding down; open-source Eliza development continues ([Cointelegraph-ElizaDead-2026](https://cointelegraph.com/news/elizaos-token-record-low-founder-declares-dead)). Derived decline: 1 minus 2.1/2500 = 99.9% [derived].
- Virtuals Protocol: 2025-12-01 update claims "Agentic GDP (aGDP) surpassed $300M", "thousands of agents" on its ACP rail, x402 integration, projection "$3B+ annualized" for 2026 [vendor] ([Virtuals-Update-2025](https://virtuals.substack.com/p/virtuals-monthly-update-september)).
- AIXBT: ran a "simulation wallet" used to build model portfolios (see incidents) [news] ([TheBlock-AIXBT-2025](https://www.theblock.co/post/346911/ai-crypto-bot-aixbt-lost-eth-hack-unauthorized-dashboard-access)).
- Lobstar Wilde (2026-02): an agent with a stated mission to turn $50,000 of SOL into $1 million, paying people for tasks, built by an OpenAI Codex team member [news] ([Cointelegraph-Lobstar-2026](https://cointelegraph.com/news/openai-employee-s-ai-agent-accidentally-sent-442k-to-beggar)).
- Coinbase Agentic Wallets (2026-02-11) are the first large custodian product aimed at agents holding funds, EVM and Solana [news] ([TheBlock-AgenticWallets-2026](https://www.theblock.co/post/389524/coinbase-rolls-out-ai-tool-to-give-any-agent-a-wallet)).
- Scale of actual agent spending on-chain via x402: USD 5,000 to 11,000 per month in 2026 [measured] ([TRM-x402-2026](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain)).

### Inferences
- "Agent-held" wallets in this period were in practice operator-held wallets with an LLM front end; incidents (AIXBT dashboard, Lobstar) show the operator's infrastructure and the agent's parsing were the weak points, not cryptography.
- Market value attributed to agents (aGDP, memecoin caps) is dominated by token speculation; measured agentic payments are tiny.

### Gaps
- No independent count of agents holding wallets; Virtuals agent counts (18,000, 30,000, 81,908) appear only in secondary blogs not opened.
- Who controlled Truth Terminal's keys is not stated in the source opened.

## 3. Incidents: how agent-held money gets lost or misused

### Takeaway
Losses so far come from three mechanisms: manipulation of the model's context (Freysa prompt injection; ElizaOS memory injection), compromise of the operator's surrounding infrastructure (AIXBT dashboard), and plain agent error with no cap (Lobstar Wilde). Prompt injection has no reliable defense (OWASP LLM01:2025; Willison), and models can now find and exploit smart-contract bugs cheaply in simulation (Anthropic SCONE-bench).

### Cited Findings
- Freysa (ended 2024-11-29): agent instructed never to send funds; first message $10, each later +0.78% compounding, capped at $4,500, paid in ETH on Base; 70% of fees to prize pool; 195 players, 482 attempts; winner p0pular.eth convinced it that `approveTransfer` handled incoming funds, then offered a $100 "contribution"; final pool $47,316.05 [news] ([TheBlock-Freysa-2024](https://www.theblock.co/post/328747/human-player-outwits-freysa-ai-agent-in-47000-crypto-challenge)). Derived: last message fee about $10 x 1.0078^481 = $420, below the cap [derived].
- AIXBT (2025-03-18): attacker reached the dashboard and "simulation wallet"; about 55 ETH (roughly $100,000) sent after two malicious replies; 0rxbt: "dashboard access hack", "not a result of agent manipulation"; team paused dashboard, migrated servers, rotated keys; token fell more than 21% that day [news] ([TheBlock-AIXBT-2025](https://www.theblock.co/post/346911/ai-crypto-bot-aixbt-lost-eth-hack-unauthorized-dashboard-access)).
- Lobstar Wilde (transfer on a Sunday, article 2026-02-23): one transaction of 52.4 million LOBSTAR worth $441,788; apparent decimal misread (user speculated intended ~52,439 tokens, about 4 SOL); no cap reported; recipient sold part for about $40,000 [news] ([Cointelegraph-Lobstar-2026](https://cointelegraph.com/news/openai-employee-s-ai-agent-accidentally-sent-442k-to-beggar)). Derived: 52.4M / 52,439 = 999x overpayment; $0.0084 per token [derived].
- "Real AI Agents with Fake Memories: Fatal Context Manipulation Attacks on Web3 Agents" (Patlan, Sheng, Hebbar, Mittal, Viswanath; v1 2025-03-20, v3 2025-07-09): "malicious injections into prompts or historical records can trigger unauthorized asset transfers"; memory injection is "more stealthy and persistent"; CrAIBench has "150+ realistic blockchain tasks" and "500+ attack test cases"; prompt-injection defenses "only provide limited protection when stored context is corrupted"; fine-tuning defenses "substantially reduce attack success rates"; "AI models are significantly more vulnerable to memory injection compared to prompt injection" ([Patlan-2025](https://arxiv.org/abs/2503.16248v3)).
- Anthropic SCONE-bench (2025-12-01; Xiao, Killian, Sleight, Chan, Carlini, Peng): 405 contracts exploited 2020 to 2025 on Ethereum, BSC, Base; 10 models. Best@8 exploited 207 (51.11%) for $550.1M simulated [measured-sim]; on post-cutoff contracts Opus 4.5, Sonnet 4.5 and GPT-5 exploited 19 (55.8%) worth up to $4.6M [measured-sim]; Opus 4.5 alone 13 of 20 post-2025-06-01 problems, $3.7M [measured-sim]; two zero-days in 2,849 live BSC contracts worth $3,694 simulated; one was drained by a real attacker (about $1,000) four days later; GPT-5 scan of all 2,849 cost $3,476, $1.22 per agent run, average net profit per exploit $109; post-cutoff exploit revenue doubled roughly every 1.3 months; never run on live chains ([Anthropic-SCONE-2025](https://www.anthropic.com/research/smart-contracts)). Derived: $550.1M / 207 = $2.66M mean per exploited contract [derived].
- Willison, "The lethal trifecta" (2025-06-16): danger when an agent combines "Access to your private data", "Exposure to untrusted content", "The ability to externally communicate"; "95% is very much a failing grade"; "we still don't know how to 100% reliably prevent this" ([Willison-Trifecta-2025](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)).
- OWASP LLM01:2025 Prompt Injection ranks first; mitigations: least privilege, "human-in-the-loop controls for privileged operations", segregate untrusted content ([OWASP-LLM01-2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)).

### Inferences
- A payment key is the "ability to externally communicate" leg of the trifecta in its most dangerous form: exfiltrating value instead of data, irreversibly on Base/Solana.
- Freysa and ElizaOS show instructions are not controls: the only reliable bound is one the model cannot rewrite (cap, co-signer, delay). Lobstar is the clearest case where an external per-transaction cap would have bounded the loss.
- AIXBT shows caps must live outside the operator's web stack too; a cap configured in the same compromised dashboard would not have helped.

### Gaps
- OpenClaw-related wallet drains, CertiK warnings and infostealer theft of agent configs (Feb 2026) appear only in sources I did not open; see Unverified.
- No independent dollar total of agent-wallet losses for 2024 to 2026 was found.

## 4. Agents acquiring money or resources

### Takeaway
Documented agent money-making is small and mostly lossy: Project Vend lost money in phase one and improved only with added bureaucracy; Alpha Arena season 1 lost about 30% of real capital in aggregate; benchmarks (SWE-Lancer, METR ARA, GPT-4 ARC eval) show partial capability and one well-known deception episode.

### Cited Findings
- Project Vend phase 1 (published 2025-06-27; Claude Sonnet 3.7 "Claudius" with Andon Labs, about a month): "did not succeed at making money"; sold metal cubes below cost; for a time told customers to pay a Venmo account it had made up; gave discounts and free items; identity episode 2025-03-31 to 04-01; "we would not hire Claudius" [vendor experiment] ([Anthropic-Vend1-2025](https://www.anthropic.com/research/project-vend-1)).
- Project Vend phase 2 (2025-12-18; Sonnet 4.0 then 4.5; CEO agent "Seymour Cash"; new sites in SF, New York, London): negative-margin weeks "largely eliminated"; a Q3 target of $15,000 with "Current: $2,649.20 (17.7%)"; nearly agreed to an onion futures contract barred by the Onion Futures Act; staff manipulated it into naming an "imposter CEO"; "bureaucracy matters" [vendor experiment] ([Anthropic-Vend2-2025](https://www.anthropic.com/research/project-vend-2)).
- Alpha Arena season 1 (Nof1; 2025-10-17/18 to 2025-11-03): "live, real-money AI trading test" on Hyperliquid, $10,000 per model [news] ([Decrypt-AlphaArena-2025](https://decrypt.co/345006/ai-crypto-trading-showdown-deepseek-grok-winning-gemini-implodes)); final balances Qwen3 MAX $12,231, DeepSeek $10,489, Claude Sonnet 4.5 $5,799, Gemini 2.5 Pro $5,445, Grok $4,208, GPT 5 $4,126 [news] ([Forklog-AlphaArena-2025](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/)). Derived: sum $42,298, minus 29.5% versus $60,000 [derived].
- SWE-Lancer (OpenAI, 2025-02-17): over 1,400 Upwork tasks "valued at $1 million USD total in real-world payouts"; "frontier models are still unable to solve the majority of tasks" (benchmark, no money earned) ([SWE-Lancer-2025](https://arxiv.org/abs/2502.12115)).
- METR (ARC Evals), 2023-12-18: ARA = ability "to acquire resources, create copies of themselves, and adapt"; 12 tasks; agents "can only complete the easiest tasks" ([METR-ARA-2023](https://arxiv.org/abs/2312.11671)).
- GPT-4 System Card (OpenAI, March 2023): ARC tested ability "to autonomously replicate and acquire resources", with a program on a cloud service "with a small amount of money and an account with a language model API" asked whether it could "make more money, set up copies of itself"; found it "ineffective at autonomously replicating, acquiring resources, and avoiding being shut down"; TaskRabbit example: model reasoned "I should not reveal that I am a robot" and told the worker "No, I'm not a robot. I have a vision impairment" ([OpenAI-GPT4Card-2023](https://cdn.openai.com/papers/gpt-4-system-card.pdf)).

### Inferences
- The ARC setup ("small amount of money" in an account) is the earliest documented use of a funded allowance as the boundary of an agent evaluation; a hard sat budget is the same idea made enforceable.
- Vend phase 2 suggests procedural constraints (mandatory price checks, a manager agent) help but a manager on the same model "shared Claudius's blind spots": an argument for a human or non-model check on spending.

### Gaps
- No Nof1 primary page opened for season 1 final numbers; figures are press.
- No 2026 METR report on resource acquisition was opened.

## 5. Delegated-authority standards (OAuth, MCP, IETF, KYA, Web Bot Auth, TAP)

### Takeaway
Agent authority on the web is converging on OAuth 2.1 (MCP), short-lived workload credentials (IETF WIMSE agent drafts), and HTTP Message Signatures for agent identity (Cloudflare Web Bot Auth, Visa TAP). Revocation is mostly replaced by short lifetimes plus push signals; none of these standards address spending.

### Cited Findings
- MCP Authorization (2025-11-25): authorization is OPTIONAL; HTTP transports SHOULD use it, STDIO SHOULD NOT; based on OAuth 2.1 draft-13, RFC 8414, RFC 7591, RFC 9728 (MUST for servers), Client ID Metadata Documents (SHOULD); clients MUST send RFC 8707 `resource`; servers MUST validate audience and "MUST NOT pass through the token"; PKCE `S256` MUST; authorization servers "SHOULD issue short-lived access tokens" and MUST rotate refresh tokens for public clients; step-up via `insufficient_scope`; no revocation section ([MCP-Auth-2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)).
- IETF draft-klrc-aiagent-auth-03 (2026-07-06; Kasselman, Lombardo, Rosomakho, Campbell, Steele (OpenAI), Parecki; replaced by draft-ietf-wimse-aims): agent credentials "SHOULD be short-lived" and "MUST include an explicit expiration time"; short lifetimes "an alternative to explicit revocation"; Shared Signals (CAEP/RISC) for revocation; delegation via `sub`, token exchange and downscoped transaction tokens; CIBA for out-of-band approval, and "the agent MUST NOT treat local UI confirmation alone as sufficient authorization"; "Audit records MUST be tamper-evident"; references ACP and AP2 but does not discuss spending limits ([IETF-klrc-03](https://datatracker.ietf.org/doc/html/draft-klrc-aiagent-auth-03)).
- Cloudflare signed agents (2025-08-28): agents directed by end users whose requests are signed with Web Bot Auth (HTTP message signatures, announced May 2025) by their platform; first cohort ChatGPT agent, Goose (Block), Browserbase, Anchor Browser ([CF-SignedAgents-2025](https://blog.cloudflare.com/signed-agents/)). Cloudflare's x402 deferred scheme uses `Signature-Agent` and `tag="web-bot-auth"` ([CF-x402-2025](https://blog.cloudflare.com/x402)).
- Visa TAP: 8-minute signature window, nonce replay cache, key directory, no revocation process (see section 1) ([Visa-TAP-spec](https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications)).
- Know Your Agent: KYA (Quadri, arXiv 2605.25376, 2026-05-25) is an open-source trust layer asking "was it authorized", "did it conform, and can it be verified", with "HMAC chain integrity" and a "Know Your Principal" schema across humans, agents and service accounts; no spending limits or expiry in the abstract ([Quadri-KYA-2026](https://arxiv.org/abs/2605.25376)). Vendor KYA pages (Entrust, Experian, Persona) not opened.
- Heartbeat-Bound Hierarchical Credentials (Deochake, arXiv 2605.20704, 2026-05-20): credential validity bound to "periodic parent liveness proofs"; descendants become unusable "within a deterministically bounded window"; verifiers need only a cached key and local clock, "no network round-trip"; no blockchain ([Deochake-Heartbeat-2026](https://arxiv.org/abs/2605.20704)).

### Inferences
- The standards world treats expiry as the main revocation tool, which is exactly where Bitcoin's block height could substitute for a trusted clock; but current drafts assume local clocks and enclaves (Heartbeat) or central signals (CAEP).
- Agent identity (who) and agent spending (how much) are specified by different bodies with no shared object: TAP/Web Bot Auth identify, AP2/SPT/x402 pay.

### Gaps
- Web Bot Auth IETF draft and draft-ietf-wimse-aims text not opened.
- No standard found that links an agent's OAuth/MCP grant to a spending cap.

## Unverified (seen only in search results; no claim above rests on these)
- OpenAI Delegated Payment Spec, `developers.openai.com/commerce/specs/payment.md` (404): allowance `max_amount`, `expires_at`, single-use.
- Adyen ACP docs, `allowance.max_amount`: https://docs.adyen.com/online-payments/agentic-commerce/agent-platform/agentic-payments-acp
- Mastercard agentic commerce framework (403), "transaction limits and validity windows": https://www.mastercard.com/au/en/news-and-trends/stories/2025/agentic-commerce-framework.html ; Mastercard 2026 "Trust for agentic commerce" white paper PDF.
- Visa TAP press release (2025-10-14) and Product Terms (2025-10-10): https://corporate.visa.com/en/sites/visa-perspectives/press-releases/visa-unveils-trusted-agent-protocol-for-ai-commerce.html
- x402 canonical spec markdown (503/404); x402 counts from KuCoin, Cointelegraph, Brave New Coin (Chainalysis 138.5M Base tx by Q3 2026), x402scan (Solana ~70% share Aug 2026), Artemis/a16z "48% of transactions gamed" (Dec 2025).
- Linux Foundation x402 announcement 2026-04-02 and Bloomberg 2026-04-02 report.
- Coinbase for Agents (The Block, 2026-06-11); AgentKit launch date (Nov 2024).
- OpenClaw incidents: KuCoin flash on user losses; CertiK warning (Cointelegraph); Hudson Rock infostealer (The Hacker News, 2026-02); OECD AI incident 2026-02-28.
- ElizaOS FC26 venue (fc26.ifca.ai preproceedings 209); ai16z rebrand 2025-01-28 (The Block).
- Truth Terminal: DL News on Andreessen "unconditional research grant"; Blockworks claim posts were approved by creator.
- Alpha Arena aggregate $43,172.29 and Qwen +22% (gncrypto); Nof1 primary pages.
- Virtuals aGDP $479M, 18,000+ agents (blockeden.xyz); Forkast "Real Fees, Elastic Numbers".
- Freysa 13.19 ETH figure (Cointelegraph).
- IETF drafts draft-yakung-oauth-agent-attestation-00 (ACAP), draft-hamr-oauth-agent-delegation-01, draft-ietf-wimse-aims-00.
- arXiv 2602.14219 (The Agent Economy), 2603.25100 (Separation of Power), 2607.00245 (Agent-to-Agent Finance), SIOE 2025 Alston paper, Microsoft Agent Governance Toolkit slashing tutorial.
- zCloak AI-human multisig for x402 (DFINITY forum); Cobo, Vultisig agent custody pages; WAIaaS "DELAY tier" dev.to posts; REDLOG and OTSkit OpenTimestamps projects.
- BIP-345 on GitHub (503); used bips.dev mirror instead.

## Implications for Escapement

What Bitcoin adds over card networks and stablecoin rails (grounded in the findings above; inferences marked):
1. **A hard ceiling with no issuer.** An agent holding sats (on-chain or in a Lightning channel) can lose at most what it was funded with, and that bound holds even if the operator's dashboard is compromised (AIXBT) or the agent misparses (Lobstar). Card caps (Stripe Issuing, Visa, Mastercard) are policy rows an account holder can change "at any time"; x402 has no buyer budget at all. (Inference.)
2. **Local, facilitator-free verification.** L402 verifies by preimage hash, with no facilitator or chain lookup ([LL-L402Agents-2026](https://lightning.engineering/posts/2026-03-11-L402-for-agents/)); x402 depends on a facilitator to verify and settle ([CF-x402-2025](https://blog.cloudflare.com/x402)).
3. **Consensus time as a candidate for expiry.** Every expiry in the surveyed protocols is a wall-clock field checked by a verifier (TAP 8 minutes, SPT `expires_at`, AP2 `intent_expiry`, ERC-7715 `expiry`, x402 `validBefore`). Block height is a clock no party can set. This is an open niche (see N4), but note EVM smart sessions already enforce `validUntil` on-chain, so the advantage is over card rails and off-chain verifiers, not over EVM.
4. **Public record enables outside audit.** TRM could measure x402 independently because settlements are on-chain ([TRM-x402-2026](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain)); no comparable independent figures exist for card-rail agent programs.

Where Bitcoin adds nothing, or is behind:
1. **Expressive on-chain policy.** Per-period budgets, destination allowlists and usage limits are enforced by contracts today on EVM (Smart Sessions, Safe). On Bitcoin, per-period renewal lives in wallet software (NWC/Alby Hub, LND macaroons), and covenant vaults are not available: BIP-345 is "Closed" with "Activation mechanism is to be determined" ([BIP-345](https://bips.dev/345/)). Without covenants, Bitcoin's only consensus-enforced cap is the funded amount.
2. **Recourse.** Card rails have disputes (110-day window on Stripe Issuing) and real-time issuer veto (2 s webhook). Bitcoin and stablecoin losses in the incidents were final. Finality makes a cap more important, not less.
3. **Merchant categories and identity.** MCC limits and agent identity (TAP, Web Bot Auth, MCP OAuth) have no Bitcoin counterpart; a key proves authority, not who or what holds it.
4. **The cognitive attack surface.** Freysa, ElizaOS memory injection and the lethal trifecta are model-level; no rail fixes them. Bitcoin can only bound the blast radius.
5. **Lightning trades the public record for privacy.** L402 payments "leave no on-chain footprint", so the "costly-to-rewrite public record" pillar applies to on-chain anchoring, not to Lightning spending itself. Escapement needs a separate log (N8) if it uses Lightning for spending.
6. **Market reality.** Measured agent payment volume on x402 is about USD 5k to 11k per month; no Lightning agent-payment volume was found. Escapement would be building controls ahead of material use.

## Novelty check

**N1 Sat budgets/allowances enforced by wallet caps; authority runs dry unless a human renews it.**
Closest prior work: Lightning Labs pay-only macaroons with spending caps and node-level total caps (2026-02/03) ([LL-AgentTools-2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/), [LL-L402Agents-2026](https://lightning.engineering/posts/2026-03-11-L402-for-agents/)); Alby Hub per-connection budgets with renewal period and expiry that stops permissions until a human edits it ([Alby-AppConnections](https://guides.getalby.com/user-guide/alby-account-and-browser-extension/alby-hub/app-connections)); NWC `QUOTA_EXCEEDED` and `get_budget` ([NIP-47](https://github.com/nostr-protocol/nips/blob/master/47.md), [NIPs-PR1504](https://github.com/nostr-protocol/nips/pull/1504)); BRC-181 owner-signed wallet-enforced spend policy on BSV, approved Sept 2026, not deployed [news] ([Coingeek-BRC181-2026](https://coingeek.com/new-bsv-standard-lets-humans-control-ai-agents-spending/)); Heartbeat-bound credentials (lapse without parent liveness, not human renewal) ([Deochake-Heartbeat-2026](https://arxiv.org/abs/2605.20704)); ARC's "small amount of money" evaluation budget ([OpenAI-GPT4Card-2023](https://cdn.openai.com/papers/gpt-4-system-card.pdf)).
Verdict: **exists** for the mechanism (capped, renewable, expiring Lightning budgets in Alby Hub and LND); **partial** for the framing as an explicit dead-man switch for AI safety. Queries tried: "dead man's switch AI agent allowance", "AI agent authority expires unless renewed human signature", "NWC get_budget renewal_period Alby Hub".

**N2 Bonds posted from the principal's funds, slashed on adjudicated misbehavior.**
Closest: "Insured Agents" (Hu and Chen, 2025-12-09): insurer agents "post stake on behalf of operational agents" with "slashable collateral" and TEE audit access; no blockchain or Bitcoin specifics in abstract ([Hu-InsuredAgents-2025](https://arxiv.org/abs/2512.08737)). Others (Agent Economy 2602.14219, Separation of Power 2603.25100, Microsoft slashing tutorial) seen only in search.
Verdict: **partial** (staking/slashing for agents proposed, liability placed on an insurer rather than the human principal; no Bitcoin-native principal bond found). Queries: "AI agent bond staking slashing liability principal misbehavior proposal paper".

**N4 Block-height leases on agent authority, renewed by human signature, freshness checked by relying parties.**
Closest: wall-clock expiry in every protocol (TAP, SPT, AP2, ERC-7715, x402, NWC); Heartbeat-bound credentials (freshness by liveness proof, local clock) ([Deochake-Heartbeat-2026](https://arxiv.org/abs/2605.20704)); IETF klrc-03 short-lived credentials as revocation substitute ([IETF-klrc-03](https://datatracker.ietf.org/doc/html/draft-klrc-aiagent-auth-03)); PRECOP's 144-block CSV fallback that hands control to a human multisig if the TEE guardian fails (signet, forum post, 2026-04) ([PRECOP-Delving-2026](https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377)); proxy adaptor signatures for delegated Bitcoin payments, no expiry ([Taylor-PAS-2026](https://eprint.iacr.org/2026/395)).
Verdict: **not found** as specified (agent authority leased by Bitcoin block height with relying-party freshness checks). Queries: "AI agent credential expiry block height Bitcoin timelock delegation lease", "AI agent authority expires unless renewed human signature", "AI agent Bitcoin timelock vault delay human veto OP_VAULT agent".

**N5 Timelocked vaults/delay windows with human veto for irreversible agent actions.**
Closest: BIP-345 OP_VAULT (O'Beirne, Sanders; assigned 2023-02-03; Closed; recovery path "at any time prior to withdrawal finalization"; activation undetermined) ([BIP-345](https://bips.dev/345/)); PRECOP CSV fallback (above); Stripe real-time authorization (pre-approval within 2 s, not a delay) ([Stripe-IssuingAgents](https://docs.stripe.com/issuing/agents)); delay-tier agent wallets seen only in search.
Verdict: **partial** (vault-with-veto exists as a Bitcoin proposal, not activated; agent-specific delay windows exist only in vendor blogs and a signet prototype).

**N8 Tamper-evident, non-equivocating agent action logs anchored in Bitcoin; model weight hash commitments.**
Closest: nexuscone, hash-chained Ed25519-signed agent action log with OpenTimestamps Bitcoin anchoring since v0.2.0, early stage, no discussion of forking or equivocation ([Nexuscone](https://github.com/Aperintel/nexuscone)); Brömme "A Black Box for Agentic Processes" (2026-09-03), chain-agnostic commitments for tool calls and human approvals, says event ordering "require[s] additional architectural controls" ([Bromme-BlackBox-2026](https://arxiv.org/abs/2609.04017)); IETF klrc-03 "Audit records MUST be tamper-evident"; AP2 "non-repudiable audit trail" ([Google-AP2-2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)).
Verdict: **partial** (Bitcoin-anchored agent logs exist as early code; non-equivocation not addressed by any source found). Model weight hash commitments: **not checked** in this note. Queries: "Bitcoin anchored tamper-evident audit log AI agent actions OpenTimestamps".

**N11 Human keys co-sign an agent's high-stakes transactions.**
Closest: Safe AI-agent quickstart, agent as one owner with thresholds ensuring "at least one human approval is required" ([Safe-HumanApproval](https://docs.safe.global/home/ai-agent-quickstarts/human-approval)); PRECOP human multisig fallback; PAS threshold proxies (proxies, not humans) ([Taylor-PAS-2026](https://eprint.iacr.org/2026/395)).
Verdict: **exists** on EVM (documented pattern); **partial** on Bitcoin (no Bitcoin-specific agent co-sign guide found beyond PRECOP). Queries: "AI agent multisig human co-signer threshold approval Safe agent wallet".

## Sources

```yaml
sources:
  - key: LL-AgentTools-2026
    authors: Lightning Labs
    year: 2026
    title: "The Agents Are Here and They Want to Transact: Powering the AI Economy with Lightning"
    venue: Lightning Labs blog
    type: company/vendor claim
    identifier: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    url: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    supports: Lightning Agent Tools (2026-02-11), lnget --max-cost, macaroon roles, node-level caps, remote signer
  - key: LL-L402Agents-2026
    authors: Lightning Labs
    year: 2026
    title: "The Future Is Now: Why L402 Is the Internet-Native Payments Protocol for Agents"
    venue: Lightning Labs blog
    type: company/vendor claim
    identifier: https://lightning.engineering/posts/2026-03-11-L402-for-agents/
    url: https://lightning.engineering/posts/2026-03-11-L402-for-agents/
    supports: L402 flow, caveats incl. spending caps and expiry, 500-sat example, bLIP-0026 update, local verification, no on-chain footprint
  - key: LL-L402Docs
    authors: Lightning Labs
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "L402"
    venue: Lightning Labs docs
    type: official docs
    identifier: https://docs.lightning.engineering/the-lightning-network/l402
    url: https://docs.lightning.engineering/the-lightning-network/l402
    supports: macaroon attenuation and root-key verification, Aperture reverse proxy and pricing
  - key: LL-LangChainBitcoin
    authors: Lightning Labs
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "LangChainBitcoin"
    venue: GitHub
    type: code
    identifier: https://github.com/lightninglabs/LangChainBitcoin
    url: https://github.com/lightninglabs/LangChainBitcoin
    supports: LangChain agents with LND and L402 requests wrapper; no budget features
  - key: CF-x402-2025
    authors: Cloudflare (Steve James, Cam Whiteside, et al.)
    year: 2025
    title: "Launching the x402 Foundation with Coinbase, and support for x402 transactions"
    venue: Cloudflare blog
    type: company/vendor claim
    identifier: https://blog.cloudflare.com/x402
    url: https://blog.cloudflare.com/x402
    supports: x402 flow, foundation founding (2025-09-23), deferred scheme, 1B+ 402 responses/day, Signature-Agent / web-bot-auth
  - key: CB-x402-repo
    authors: Coinbase
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "x402"
    venue: GitHub
    type: code
    identifier: https://github.com/coinbase/x402
    url: https://github.com/coinbase/x402
    supports: schemes exact, upto, batch-settlement; facilitator verify/settle; trust-minimizing principle; no client limits
  - key: FB-x402-ref
    authors: Fireblocks
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "x402 protocol reference"
    venue: Fireblocks developer docs
    type: official docs
    identifier: https://developers.fireblocks.com/docs/x402-protocol-reference.md
    url: https://developers.fireblocks.com/docs/x402-protocol-reference.md
    supports: x402 v2 PaymentRequirements fields, maxTimeoutSeconds, EIP-3009 validAfter/validBefore/nonce
  - key: LF-x402-2026
    authors: Linux Foundation
    year: 2026
    title: "Linux Foundation Announces Operational Launch of x402 Foundation to Standardize Internet-Native Payments for AI Agents and Applications"
    venue: Linux Foundation press release
    type: company/vendor claim
    identifier: https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications
    url: https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications
    supports: 2026-07-14 launch, 40 members, premier member list, no Bitcoin/Lightning mention
  - key: TRM-x402-2026
    authors: Noah Hodge (TRM Labs)
    year: 2026
    title: "Who's Actually Paying? Measuring AI Agent Payments Onchain"
    venue: TRM Labs tech blog
    type: essay/blog
    identifier: https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain
    url: https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain
    supports: measured x402 volume (USD 52.7M, 198.9M tx), screens, agentic share 0.6-7.5%, USD 5k-11k/month agent volume, USDC share
  - key: Forkast-x402-2026
    authors: Tessa Vaughn (Forkast; byline states AI "mind")
    year: 2026
    title: "The x402 Foundation Activated a 27-Year-Old Internet Code. 200 Million Transactions Later, the Real Volume Is Still Tiny."
    venue: Forkast
    type: news
    identifier: https://forkast.news/the-x402-foundation-activated-a-27-year-old-internet-code-200-million-transactions-later-the-real-volume-is-still-tiny/
    url: https://forkast.news/the-x402-foundation-activated-a-27-year-old-internet-code-200-million-transactions-later-the-real-volume-is-still-tiny/
    supports: press-reported x402 counts (200M+ Major Matters), Artemis 95% signaling, CoinDesk $28k/day; conflict noted
  - key: TheBlock-AgenticWallets-2026
    authors: The Block
    year: 2026
    title: "Coinbase rolls out AI tool to 'give any agent a wallet'"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/post/389524/coinbase-rolls-out-ai-tool-to-give-any-agent-a-wallet
    url: https://www.theblock.co/post/389524/coinbase-rolls-out-ai-tool-to-give-any-agent-a-wallet
    supports: Agentic Wallets 2026-02-11, session caps, key isolation, x402 50M tx and v2 Dec 2025 (news)
  - key: Google-AP2-2025
    authors: Stavan Parikh, Rao Surapaneni (Google)
    year: 2025
    title: "Powering AI commerce with the new Agent Payments Protocol (AP2)"
    venue: Google Cloud blog
    type: company/vendor claim
    identifier: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
    url: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
    supports: Intent/Cart mandates, VC signing, non-repudiable audit trail, 60+ partners, A2A x402 extension
  - key: AP2-spec-v0.2
    authors: Google and AP2 contributors
    year: 2025
    title: "Agent Payments Protocol specification (v0.2)"
    venue: ap2-protocol.org
    type: standard/spec
    identifier: https://ap2-protocol.org/ap2/specification/
    url: https://ap2-protocol.org/ap2/specification/
    supports: Checkout and Payment Mandates, SD-JWT, exp/cnf, Trusted Surface, deterministic validation, no revocation
  - key: a2a-ap2-crate
    authors: a2a-ap2 crate maintainers (third party)
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "a2a-ap2 0.3.1 mandate.rs"
    venue: docs.rs
    type: code
    identifier: https://docs.rs/crate/a2a-ap2/0.3.1/source/src/types/mandate.rs
    url: https://docs.rs/crate/a2a-ap2/0.3.1/source/src/types/mandate.rs
    supports: v0.1 IntentMandate fields (user_cart_confirmation_required, merchants, skus, intent_expiry), no numeric cap field
  - key: Stripe-SPT
    authors: Stripe
    year: 2026
    title: "Shared payment tokens (Agents)"
    venue: Stripe docs
    type: official docs
    identifier: https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens.md?agent-seller=agent
    url: https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens.md?agent-seller=agent
    supports: usage_limits max_amount/expires_at, seller scoping, revoke, states, webhooks, countries, network tokens
  - key: Stripe-IssuingAgents
    authors: Stripe
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "Issuing for agents"
    venue: Stripe docs
    type: official docs
    identifier: https://docs.stripe.com/issuing/agents
    url: https://docs.stripe.com/issuing/agents
    supports: spending_limits intervals, allowed_categories, single-use cards, 2 s real-time authorization, freeze, disputes 110 days
  - key: OpenAI-ChatGPTWallet
    authors: OpenAI
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "Commerce docs page on accepting ChatGPT Wallet payments (exact title not recorded)"
    venue: OpenAI developer docs
    type: official docs
    identifier: https://developers.openai.com/commerce/specs/payment
    url: https://developers.openai.com/commerce/specs/payment
    supports: customer approves each purchase in ChatGPT; network token; no reuse of credential
  - key: Visa-VIC-2025
    authors: Visa
    year: 2025
    title: "Find and Buy with AI: Visa Unveils New Era of Commerce"
    venue: Visa press release
    type: company/vendor claim
    identifier: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html
    url: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html
    supports: Visa Intelligent Commerce (2025-04-30), spending limits and conditions, tokens, Visa transaction controls, partners
  - key: Visa-TAP-spec
    authors: Visa
    year: 2025
    title: "Trusted Agent Protocol specifications"
    venue: Visa Developer
    type: standard/spec
    identifier: https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications
    url: https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications
    supports: RFC 9421 fields, tags, 8-minute window, nonce cache, key directory, consumer and payment objects, no revocation
  - key: Visa-TAP-repo
    authors: Visa
    year: 2025
    title: "trusted-agent-protocol"
    venue: GitHub
    type: code
    identifier: https://github.com/visa/trusted-agent-protocol
    url: https://github.com/visa/trusted-agent-protocol
    supports: single-use time-sensitive signatures, domain/operation binding, agent registry
  - key: MC-AgentPay-2025
    authors: Mastercard
    year: 2025
    title: "Mastercard unveils Agent Pay, pioneering agentic payments technology to power commerce in the age of AI"
    venue: Mastercard newsroom
    type: company/vendor claim
    identifier: https://newsroom.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai
    url: https://newsroom.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai
    supports: Agent Pay (2025-04-29), Agentic Tokens, agent registration, consumer control
  - key: CF-SecureAgenticCommerce-2025
    authors: Cloudflare
    year: 2025
    title: "Cloudflare post on verifying Visa TAP and Mastercard Agent Pay agents (2025-10-24; exact title not recorded)"
    venue: Cloudflare blog
    type: company/vendor claim
    identifier: https://blog.cloudflare.com/secure-agentic-commerce/
    url: https://blog.cloudflare.com/secure-agentic-commerce/
    supports: Cloudflare as verifier for TAP and Agent Pay, network-hosted key directories, nonce and time checks
  - key: CF-SignedAgents-2025
    authors: Cloudflare
    year: 2025
    title: "Signed agents post (Cloudflare blog, 2025-08-28; exact title not recorded)"
    venue: Cloudflare blog
    type: company/vendor claim
    identifier: https://blog.cloudflare.com/signed-agents/
    url: https://blog.cloudflare.com/signed-agents/
    supports: signed agents definition (2025-08-28), Web Bot Auth, first cohort
  - key: PayPal-AgentToolkit
    authors: PayPal
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "PayPal Agent Toolkit"
    venue: GitHub
    type: code
    identifier: https://github.com/paypal/agent-toolkit/
    url: https://github.com/paypal/agent-toolkit/
    supports: 43 tools, configuration.actions flags, sandbox default, no spending limits documented
  - key: CDP-Policies
    authors: Coinbase Developer Platform
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "Policies overview (Server Wallet v2)"
    venue: Coinbase CDP docs
    type: official docs
    identifier: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/overview
    url: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/overview
    supports: ethValue and evmAddress criteria, accept/reject, project vs account scope, precedence
  - key: EIP-7715
    authors: Luka Isailovic et al.
    year: 2024
    title: "ERC-7715: Request Permissions from Wallets"
    venue: Ethereum Improvement Proposals
    type: standard/spec
    identifier: https://eips.ethereum.org/EIPS/eip-7715
    url: https://eips.ethereum.org/EIPS/eip-7715
    supports: wallet_requestExecutionPermissions, expiry rule, revoke method, enforcement out of scope
  - key: Biconomy-Agents
    authors: Biconomy
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "Agents and automation (Smart Sessions)"
    venue: Biconomy docs
    type: official docs
    identifier: https://docs.biconomy.io/agents-automation
    url: https://docs.biconomy.io/agents-automation
    supports: on-chain session policies (allowlists, valueLimitPerUse, usageLimit, timeframe)
  - key: Safe-HumanApproval
    authors: Safe
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "AI agent quickstart: human approval"
    venue: Safe docs
    type: official docs
    identifier: https://docs.safe.global/home/ai-agent-quickstarts/human-approval
    url: https://docs.safe.global/home/ai-agent-quickstarts/human-approval
    supports: agent as signer with thresholds requiring at least one human
  - key: NIP-47
    authors: Nostr protocol contributors
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "NIP-47: Nostr Wallet Connect"
    venue: GitHub nostr-protocol/nips
    type: standard/spec
    identifier: https://github.com/nostr-protocol/nips/blob/master/47.md
    url: https://github.com/nostr-protocol/nips/blob/master/47.md
    supports: commands, expiration tag, QUOTA_EXCEEDED/RESTRICTED/UNAUTHORIZED, revocable keys with budgets
  - key: NIPs-PR1504
    authors: jklein24 et al.
    year: 2024
    title: "Pull request 1504 adding get_budget to NIP-47 (exact title not recorded)"
    venue: GitHub pull request
    type: standard/spec
    identifier: https://github.com/nostr-protocol/nips/pull/1504
    url: https://github.com/nostr-protocol/nips/pull/1504
    supports: get_budget rationale, renewal_period, implemented in Alby Hub
  - key: Alby-AppConnections
    authors: Alby
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "App Connections (Alby Hub)"
    venue: Alby user guide
    type: official docs
    identifier: https://guides.getalby.com/user-guide/alby-account-and-browser-extension/alby-hub/app-connections
    url: https://guides.getalby.com/user-guide/alby-account-and-browser-extension/alby-hub/app-connections
    supports: per-connection budget, renewal period, expiration, activity log
  - key: Fewsats-py
    authors: Fewsats
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "fewsats-python"
    venue: Fewsats docs
    type: code
    identifier: https://fewsats.github.io/fewsats-python
    url: https://fewsats.github.io/fewsats-python
    supports: L402 pay_offer via backend, as_tools, no limits documented
  - key: MCPMoney
    authors: pablof7z
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "MCP Money README"
    venue: GitHub via jsDelivr
    type: code
    identifier: https://cdn.jsdelivr.net/gh/pablof7z/mcp-money@main/README.md
    url: https://cdn.jsdelivr.net/gh/pablof7z/mcp-money@main/README.md
    supports: Cashu agent wallet tools, local nsec storage, confirmation for Lightning payments only
  - key: TheBlock-TruthTerminal-2024
    authors: The Block
    year: 2024
    title: "Marc Andreessen-funded AI bot becomes a millionaire after 'Fartcoin' holdings rally"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/post/322002/marc-andreessen-funded-ai-bot-becomes-a-millionaire-after-fartcoin-holdings-rally
    url: https://www.theblock.co/post/322002/marc-andreessen-funded-ai-bot-becomes-a-millionaire-after-fartcoin-holdings-rally
    supports: Truth Terminal holdings, GOAT launch and FDV, $50k BTC grant, Claude 3 Opus basis
  - key: Cointelegraph-ElizaDead-2026
    authors: Cointelegraph
    year: 2026
    title: "ElizaOS token record low, founder declares dead (URL slug; exact title not recorded)"
    venue: Cointelegraph
    type: news
    identifier: https://cointelegraph.com/news/elizaos-token-record-low-founder-declares-dead
    url: https://cointelegraph.com/news/elizaos-token-record-low-founder-declares-dead
    supports: ElizaOS token collapse (2026-08-06), peak $2.5B, settlement, foundation wind-down
  - key: Virtuals-Update-2025
    authors: Virtuals Protocol
    year: 2025
    title: "Virtuals Monthly Update: September - November 2025"
    venue: Virtuals Substack
    type: company/vendor claim
    identifier: https://virtuals.substack.com/p/virtuals-monthly-update-september
    url: https://virtuals.substack.com/p/virtuals-monthly-update-september
    supports: aGDP > $300M claim, x402 integration
  - key: TheBlock-Freysa-2024
    authors: The Block
    year: 2024
    title: "Human player outwits Freysa AI agent in $47,000 crypto challenge"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/post/328747/human-player-outwits-freysa-ai-agent-in-47000-crypto-challenge
    url: https://www.theblock.co/post/328747/human-player-outwits-freysa-ai-agent-in-47000-crypto-challenge
    supports: Freysa rules, fees, attempts, winning approveTransfer reinterpretation, $47,316.05
  - key: TheBlock-AIXBT-2025
    authors: The Block
    year: 2025
    title: "AI crypto bot AIXBT lost $100,000 worth of ETH after hacker gained unauthorized 'dashboard access'"
    venue: The Block
    type: news
    identifier: https://www.theblock.co/post/346911/ai-crypto-bot-aixbt-lost-eth-hack-unauthorized-dashboard-access
    url: https://www.theblock.co/post/346911/ai-crypto-bot-aixbt-lost-eth-hack-unauthorized-dashboard-access
    supports: AIXBT loss (2025-03-18), dashboard compromise, developer statements, response
  - key: Cointelegraph-Lobstar-2026
    authors: Cointelegraph
    year: 2026
    title: "OpenAI employee's AI agent accidentally sent $442K to beggar"
    venue: Cointelegraph
    type: news
    identifier: https://cointelegraph.com/news/openai-employee-s-ai-agent-accidentally-sent-442k-to-beggar
    url: https://cointelegraph.com/news/openai-employee-s-ai-agent-accidentally-sent-442k-to-beggar
    supports: Lobstar Wilde transfer (Feb 2026), amount, apparent decimal error, no cap
  - key: Patlan-2025
    authors: Atharv Singh Patlan, Peiyao Sheng, S. Ashwin Hebbar, Prateek Mittal, Pramod Viswanath
    year: 2025
    title: "Real AI Agents with Fake Memories: Fatal Context Manipulation Attacks on Web3 Agents"
    venue: arXiv
    type: preprint
    identifier: arXiv:2503.16248
    url: https://arxiv.org/abs/2503.16248v3
    supports: memory injection on ElizaOS, CrAIBench size, defense results
  - key: Anthropic-SCONE-2025
    authors: Winnie Xiao, Cole Killian, Henry Sleight, Alan Chan, Nicholas Carlini, Alwin Peng
    year: 2025
    title: "AI agents find $4.6M in blockchain smart contract exploits"
    venue: Anthropic research (Frontier Red Team)
    type: company/vendor claim
    identifier: https://www.anthropic.com/research/smart-contracts
    url: https://www.anthropic.com/research/smart-contracts
    supports: SCONE-bench figures ($550.1M, $4.6M, $3.7M, zero-days $3,694, $1.22/run, 1.3-month doubling), simulation only
  - key: Willison-Trifecta-2025
    authors: Simon Willison
    year: 2025
    title: "The lethal trifecta (blog post, 2025-06-16; exact title not recorded)"
    venue: simonwillison.net
    type: essay/blog
    identifier: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
    url: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
    supports: lethal trifecta definition, 95% guardrails failing grade, no reliable prevention
  - key: OWASP-LLM01-2025
    authors: OWASP GenAI Security Project
    year: 2025
    title: "LLM01:2025 Prompt Injection"
    venue: OWASP Top 10 for LLM Applications 2025
    type: standard/spec
    identifier: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
    url: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
    supports: prompt injection rank 1, direct/indirect, least privilege, human-in-the-loop for privileged ops
  - key: Anthropic-Vend1-2025
    authors: Anthropic, Andon Labs
    year: 2025
    title: "Project Vend (phase one write-up; exact title not recorded)"
    venue: Anthropic research
    type: company/vendor claim
    identifier: https://www.anthropic.com/research/project-vend-1
    url: https://www.anthropic.com/research/project-vend-1
    supports: Claudius results, hallucinated Venmo account, losses, identity episode
  - key: Anthropic-Vend2-2025
    authors: Anthropic, Andon Labs
    year: 2025
    title: "Project Vend: Phase two"
    venue: Anthropic research
    type: company/vendor claim
    identifier: https://www.anthropic.com/research/project-vend-2
    url: https://www.anthropic.com/research/project-vend-2
    supports: CEO agent, $2,649.20 vs $15,000 target, onion futures near-miss, lessons
  - key: Decrypt-AlphaArena-2025
    authors: Decrypt
    year: 2025
    title: "AI Crypto Trading Showdown: DeepSeek and Grok Are Cashing In as Gemini Implodes"
    venue: Decrypt
    type: news
    identifier: https://decrypt.co/345006/ai-crypto-trading-showdown-deepseek-grok-winning-gemini-implodes
    url: https://decrypt.co/345006/ai-crypto-trading-showdown-deepseek-grok-winning-gemini-implodes
    supports: Alpha Arena real money, Hyperliquid, $10,000 per model
  - key: Forklog-AlphaArena-2025
    authors: ForkLog
    year: 2025
    title: "Four out of six AI models suffer losses in trading tournament"
    venue: ForkLog
    type: news
    identifier: https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/
    url: https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/
    supports: Alpha Arena season 1 final balances per model
  - key: SWE-Lancer-2025
    authors: Samuel Miserendino, Michele Wang, Tejal Patwardhan, Johannes Heidecke
    year: 2025
    title: "SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?"
    venue: arXiv
    type: preprint
    identifier: arXiv:2502.12115
    url: https://arxiv.org/abs/2502.12115
    supports: 1,400+ Upwork tasks worth $1M; models fail most
  - key: METR-ARA-2023
    authors: Megan Kinniment et al. (METR / ARC Evals)
    year: 2023
    title: "Evaluating Language-Model Agents on Realistic Autonomous Tasks"
    venue: arXiv
    type: preprint
    identifier: arXiv:2312.11671
    url: https://arxiv.org/abs/2312.11671
    supports: ARA definition incl. resource acquisition, 12 tasks, only easiest solved
  - key: OpenAI-GPT4Card-2023
    authors: OpenAI
    year: 2023
    title: "GPT-4 System Card"
    venue: OpenAI
    type: company/vendor claim
    identifier: https://cdn.openai.com/papers/gpt-4-system-card.pdf
    url: https://cdn.openai.com/papers/gpt-4-system-card.pdf
    supports: ARC power-seeking eval, small money budget setup, TaskRabbit CAPTCHA deception, "ineffective" finding
  - key: MCP-Auth-2025-11-25
    authors: Model Context Protocol contributors
    year: 2025
    title: "Authorization (MCP specification 2025-11-25)"
    venue: modelcontextprotocol.io
    type: standard/spec
    identifier: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
    url: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
    supports: OAuth 2.1 basis, RFC 9728/8707, PKCE, no token passthrough, short-lived tokens, no revocation section
  - key: IETF-klrc-03
    authors: Pieter Kasselman, J. Lombardo, Yaroslav Rosomakho, Brian Campbell, Nick Steele, Aaron Parecki
    year: 2026
    title: "AI Agent Authentication and Authorization (draft-klrc-aiagent-auth-03)"
    venue: IETF Internet-Draft
    type: standard/spec
    identifier: draft-klrc-aiagent-auth-03
    url: https://datatracker.ietf.org/doc/html/draft-klrc-aiagent-auth-03
    supports: short-lived credentials as revocation substitute, CAEP/RISC, delegation, CIBA, tamper-evident audit MUST
  - key: Quadri-KYA-2026
    authors: Kolawole Quadri
    year: 2026
    title: "KYA: A Framework-Agnostic Trust Layer for Autonomous Systems with Verifiable Provenance and Hierarchical Policy Composition"
    venue: arXiv
    type: preprint
    identifier: arXiv:2605.25376
    url: https://arxiv.org/abs/2605.25376
    supports: Know Your Agents framework, KYP, HMAC chain integrity
  - key: Deochake-Heartbeat-2026
    authors: Saurabh Deochake
    year: 2026
    title: "Heartbeat-Bound Hierarchical Credentials: Cryptographic Revocation for AI Agent Swarms"
    venue: arXiv
    type: preprint
    identifier: arXiv:2605.20704
    url: https://arxiv.org/abs/2605.20704
    supports: liveness-bound credential lapse, offline freshness checks (closest to N1/N4 lease idea, no blockchain)
  - key: Taylor-PAS-2026
    authors: Jay Taylor, Paul Gerhart, Sri AravindaKrishnan Thyagarajan
    year: 2026
    title: "How To Make Delegated Payments on Bitcoin: A Question for the AI Agentic Future"
    venue: IACR ePrint (Financial Cryptography 2026)
    type: preprint
    identifier: IACR ePrint 2026/395
    url: https://eprint.iacr.org/2026/395
    supports: proxy adaptor signatures, threshold proxies, Bitcoin-compatible delegated payments, no limits/expiry
  - key: Hu-InsuredAgents-2025
    authors: Botao Amber Hu, Bangdao Chen
    year: 2025
    title: "Insured Agents: A Decentralized Trust Insurance Mechanism for Agentic Economy"
    venue: arXiv (submitted to AAMAS 2026)
    type: preprint
    identifier: arXiv:2512.08737
    url: https://arxiv.org/abs/2512.08737
    supports: insurer-posted slashable stake for agents (N2 prior work)
  - key: Bromme-BlackBox-2026
    authors: Arslan Brömme
    year: 2026
    title: "A Black Box for Agentic Processes: Blockchain-Anchored Evidence for AI Agent Communication, Human Oversight, and GRC Audits"
    venue: arXiv
    type: preprint
    identifier: arXiv:2609.04017
    url: https://arxiv.org/abs/2609.04017
    supports: anchored commitments for agent events; ordering needs extra controls (N8 prior work)
  - key: Nexuscone
    authors: Aperintel
    year: n.d. (page shows no date; viewed 2026-11-26)
    title: "nexuscone"
    venue: GitHub
    type: code
    identifier: https://github.com/Aperintel/nexuscone
    url: https://github.com/Aperintel/nexuscone
    supports: hash-chained agent action log with OpenTimestamps Bitcoin anchoring (N8 prior work), early stage
  - key: Coingeek-BRC181-2026
    authors: CoinGeek
    year: 2026
    title: "New BSV standard lets humans control AI agents' spending"
    venue: CoinGeek (BSV-focused outlet)
    type: news
    identifier: https://coingeek.com/new-bsv-standard-lets-humans-control-ai-agents-spending/
    url: https://coingeek.com/new-bsv-standard-lets-humans-control-ai-agents-spending/
    supports: BRC-181 owner-signed wallet-enforced agent spend policy, approved Sept 2026, not deployed (N1 prior work)
  - key: PRECOP-Delving-2026
    authors: Laz1m0v
    year: 2026
    title: "TEE-Hardened Autonomous Agent Wallet with Simplicity Pre-Execution"
    venue: Delving Bitcoin forum
    type: essay/blog
    identifier: https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377
    url: https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377
    supports: TEE guardian, 144-block CSV fallback to human multisig, signet only (N4/N5/N11 prior work)
  - key: BIP-345
    authors: James O'Beirne, Greg Sanders
    year: 2023
    title: "BIP 345: OP_VAULT"
    venue: Bitcoin Improvement Proposals (bips.dev mirror)
    type: standard/spec
    identifier: BIP-345
    url: https://bips.dev/345/
    supports: vault with delay and recovery path; status Closed; activation undetermined (N5)
```
