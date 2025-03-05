import numpy as np

def generate_random_bits(n):
    """Generate n random bits."""
    return np.random.randint(0, 2, n)

def generate_random_bases(n):
    """Generate n random bases (0 for + basis, 1 for × basis)."""
    return np.random.randint(0, 2, n)

def encode_qubits(bits, bases):
    """Encode bits into qubits based on the selected bases."""
    return [(bit, base) for bit, base in zip(bits, bases)]

def measure_qubits(qubits, measurement_bases):
    """Measure qubits using the given bases."""
    measured_bits = []
    for (bit, base), measure_base in zip(qubits, measurement_bases):
        if base == measure_base:
            measured_bits.append(bit)  # Correct measurement
        else:
            measured_bits.append(np.random.randint(0, 2))  # Random collapse
    return np.array(measured_bits)

def sift_key(alice_bases, bob_bases, bob_bits):
    """Keep only bits where Alice and Bob used the same bases."""
    matching_indices = alice_bases == bob_bases
    return bob_bits[matching_indices]

def introduce_eavesdropper(alice_bits, alice_bases):
    """Simulate an eavesdropper (Eve) intercepting and measuring qubits."""
    eve_bases = generate_random_bases(len(alice_bits))
    eve_measured_bits = measure_qubits(encode_qubits(alice_bits, alice_bases), eve_bases)
    return eve_measured_bits, eve_bases

def detect_eavesdropping(alice_bits, bob_bits, sample_size=10):
    """Check a small random subset of bits to detect eavesdropping."""
    indices = np.random.choice(len(alice_bits), sample_size, replace=False)
    errors = np.sum(alice_bits[indices] != bob_bits[indices])
    return errors > 0, errors

# Simulation parameters
num_qubits = 100

# Step 1: Alice generates a random bit string and chooses random bases
alice_bits = generate_random_bits(num_qubits)
alice_bases = generate_random_bases(num_qubits)

# Step 2: Eavesdropper (Eve) tries to intercept
eve_measured_bits, eve_bases = introduce_eavesdropper(alice_bits, alice_bases)

# Step 3: Alice encodes qubits and sends to Bob
qubits = encode_qubits(eve_measured_bits, eve_bases)  # Eve retransmits (tampered qubits)

# Step 4: Bob randomly selects bases and measures qubits
bob_bases = generate_random_bases(num_qubits)
bob_measured_bits = measure_qubits(qubits, bob_bases)

# Step 5: Alice and Bob publicly compare bases
sifted_key = sift_key(alice_bases, bob_bases, bob_measured_bits)

# Step 6: Detect eavesdropping
is_eavesdropped, error_count = detect_eavesdropping(alice_bits, bob_measured_bits)

# Print results
print(f"Alice's Bits:       {alice_bits}")
print(f"Alice's Bases:      {alice_bases}")
print(f"Bob's Bases:        {bob_bases}")
print(f"Bob's Measured Bits:{bob_measured_bits}")
print(f"Sifted Key:         {sifted_key}")
if is_eavesdropped:
    print(f"Warning! Eavesdropping detected with {error_count} errors.")
else:
    print("No eavesdropping detected. Secure communication established.")
