import torch
import matplotlib.pyplot as plt


vocab = {
    "closer": 0,
    "every": 1,
    "effort": 2,
    "forward": 3,
    "inches": 4,
    "moves": 5,
    "pizza": 6,
    "toward": 7,
    "you": 8
}

inverse_vocab = {v: k for k, v in vocab.items()}

print("\nInverse vocab:\n", inverse_vocab)

# Assume the LLM is given the start context "every effort moves you" and
# generates the following next-token logits:
next_token_logits = torch.tensor(
    [4.51, 0.89, -1.90, 6.75, 1.63, -1.62, -1.89, 6.28, 1.79]
)

# In chapter 4 its discussed that inside the generate_text_simple function, we convert the logits
# into probabilities via the softmax function and obtain the token ID corresponding to
# the generated token via the argmax funciton, which we can then map back into text via
# the inverse vocabulary.
probas = torch.softmax(next_token_logits, dim=0)
next_token_id = torch.argmax(probas).item()

print("\nProbabilities:\n", probas)
print("Next token ID:", next_token_id)
print("Next token:", inverse_vocab[next_token_id])

#           Probabilistic sampling process
torch.manual_seed(123)
next_token_id = torch.multinomial(probas, num_samples=1).item()
print("\nProbabilistic Sampling Method text token:", inverse_vocab[next_token_id])


def print_sampled_tokens(probas):
    torch.manual_seed(123)
    sample = [torch.multinomial(probas, num_samples=1).item() for i in range(1_000)]
    sampled_ids = torch.bincount(torch.tensor(sample))
    for i, freq in enumerate(sampled_ids):
        print(f"{freq} x {inverse_vocab[i]}")

print("\nMultinomial Sampling Results over 1000 iterations:")
print_sampled_tokens(probas)

#               Temperature Scaling
# We can further control the distribution and selection process via a concept called
# "temperature scaling". Temperature scaling is just a fancy description for dividing
# the logits by a number greater than 0

def softmax_with_temperature(logits, temperature):
    scaled_logits = logits / temperature
    return torch.softmax(scaled_logits, dim=0)

# Temperature values
temperatures = [1, 0.1, 5] # Original, higher confidence, and lower confidence

# Calculate scaled probabilities
scaled_probas = [softmax_with_temperature(next_token_logits, T) for T in temperatures]

print("\nScaled Probabilities:\n", scaled_probas)

# Plotting
x = torch.arange(len(vocab))
bar_width = 0.15

fig, ax = plt.subplots(figsize=(5, 3))
for i, T in enumerate(temperatures):
    rects = ax.bar(x + i * bar_width, scaled_probas[i], bar_width, label=f"Temperature = {T}")

ax.set_ylabel("Probability")
ax.set_xticks(x)
ax.set_xticklabels(vocab.keys(), rotation=90)
ax.legend()

plt.tight_layout()
# plt.savefig("temperature-plot.pdf")
plt.show()


# Exerc
for i, probas in enumerate(scaled_probas):
    print("\n\nTemperature", temperatures[i])
    print_sampled_tokens(probas)