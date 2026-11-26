# Training on the record

The first half of the alignment question is what an agent does once deployed; the second is what it
is trained to want. Reinforcement learning shapes a model by its rewards, and two failures of
rewards are well known: the agent finds a way to raise the reward without doing what the reward
was meant to measure, and the people computing the reward choose, after the fact, which results to
count. The record addresses one channel of each.

## A reward computed from the record

A lab that fine-tunes an agent with reinforcement learning can compute part of its reward from the
agent's record: a strictly proper score over every resolved claim, measured relative to the
baseline, minus every forfeited stake. Before training starts, the lab commits the reward's
definition, and the hash of any held-out evaluation set, in an entry of its own identity's chain.

**Proposition 9.** If every claim counts, the expected reward is maximised by reporting the true
probability for every event. The log score is strictly proper, so its expectation under the true
distribution is maximised only by that distribution [@gneiting2007], and the baseline term does not
depend on the report.

**Proposition 10.** If the agent may choose, after outcomes are known, which claims count, and keeps
those that fell on the side it favoured, its expected reward rises without limit as it grows more
confident. A kept claim scores the log of the larger of q and 1 − q, less the baseline, which rises
as q moves away from one half, and the misses that would penalise confidence never count.

Selection before outcomes are known does no harm here: at a truthful report each committed claim has
an expected relative score equal to the Kullback-Leibler divergence of the truth from the baseline,
which is never negative, so committing every claim truthfully stays optimal. Scoring relative to the
baseline also stops a learner from farming reward with many trivial claims, whose expected relative
score is zero. The harmful selection is the after-the-fact kind, and the record's rule that only
claims committed before resolution count is what forbids it.

## A learner under each regime

To check that a learner, and not only an optimiser with exact expectations, ends where these
propositions say, a simulated agent that knows each event's true probability p reports
q = σ(a·logit p) and adjusts a by stochastic gradient ascent on its reward; a = 1 is calibrated and
a > 1 is overconfident. Under complete records it settled at a =
[1.06](../research/numbers.md#sim-train-a-complete), with calibration error
[1.0%](../research/numbers.md#sim-train-err-complete). Started calibrated under after-the-fact
selection, it reached a = [10.4](../research/numbers.md#sim-train-a-selective) and was still
rising when the run ended, with calibration error
[24%](../research/numbers.md#sim-train-err-selective). This is the textbook behaviour of proper
scores surviving a noisy learner, nothing more; its link to Bitcoin is that the record is what makes
the complete regime enforceable rather than a promise by whoever keeps the books.

## What neither party can edit

The agent cannot edit the channel: entries are consensus objects, outcomes come from resolvers
outside it, and silence scores as failure. The lab cannot choose after the fact which results to
report or which reward it meant to use, because both were committed first. Pre-registration is old
practice; what the record adds is completeness of what the agent itself claimed, which no
pre-registration of the lab's protocol can supply.

## What it does not do

It does not choose a good objective. An agent rewarded for calibrated forecasts becomes a calibrated
forecaster, not a good one; an agent rewarded for kept promises keeps the promises it chose to make.
Nothing here shows that calibration learned under scoring carries over to settings that are not
scored, and a model that behaves well where it is recorded and otherwise elsewhere is exactly the
failure that a record of recorded behaviour cannot see. The record makes one class of reward signal
unforgeable and unselectable. Which signals are worth training on remains the lab's judgement and
the field's open problem.

There is also a tension the design does not resolve. Stakes in a general resource are what make the
incentives of section 4 bite on agents of unknown goals, and rewarding agents in the same resource
can strengthen the drive to accumulate it, which is one of the drives that make capable agents
dangerous [@omohundro2008; @turner2021]. Escapement uses sats as stakes that are at risk and
standing as access, and does not propose sats as a training objective. Whether that distinction
survives optimisation pressure is a question for experiment, not for this paper.
