"""
Graphene Electronic Band Structure
====================================
Model  : Tight-Binding (nearest neighbor)
Author : [BENALI ABDELKADER]
Date   : 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. Physical Constants
# ============================================================
a = 1.42e-10       # C-C bond length (meters)
t = 2.7            # hopping parameter (eV)

# ============================================================
# 2. Nearest-Neighbor Vectors
# ============================================================
delta1 = a * np.array([0, 1])
delta2 = a * np.array([-np.sqrt(3)/2, -1/2])
delta3 = a * np.array([+np.sqrt(3)/2, -1/2])

# ============================================================
# 3. Hamiltonian
# ============================================================
def h(kx, ky):
    """
    Off-diagonal element of the tight-binding Hamiltonian.
    h(k) = -t * sum_j exp(i k . delta_j)
    """
    k     = np.array([kx, ky])
    term1 = np.exp(1j * np.dot(k, delta1))
    term2 = np.exp(1j * np.dot(k, delta2))
    term3 = np.exp(1j * np.dot(k, delta3))
    return -t * (term1 + term2 + term3)

# ============================================================
# 4. Band Energies
# ============================================================
def energy(kx, ky):
    """
    E±(k) = ± |h(k)|
    """
    hk = h(kx, ky)
    return np.abs(hk), -np.abs(hk)

# ============================================================
# 5. High-Symmetry Points
# ============================================================
Gamma = np.array([0.0, 0.0])
K     = np.array([4*np.pi / (3*np.sqrt(3)*a), 0.0])
M     = np.array([np.pi / (np.sqrt(3)*a), np.pi/(3*a)])

# ============================================================
# 6. Build k-path:  Γ → K → M → Γ
# ============================================================
def make_path(p1, p2, n=100):
    return np.array([
        (1 - i/(n-1))*p1 + (i/(n-1))*p2
        for i in range(n)
    ])

n = 100
path = np.vstack([
    make_path(Gamma, K, n),
    make_path(K,     M, n),
    make_path(M, Gamma, n)
])

# ============================================================
# 7. Compute Bands
# ============================================================
E_plus  = np.array([energy(k[0], k[1])[0] for k in path])
E_minus = np.array([energy(k[0], k[1])[1] for k in path])

# ============================================================
# 8. Plot
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(E_plus,  color='royalblue', linewidth=2,
        label='Conduction Band')
ax.plot(E_minus, color='crimson',   linewidth=2,
        label='Valence Band')

ax.axhline(y=0, color='black', linestyle='--',
           linewidth=1, alpha=0.5, label='Fermi Level')

for pos in [0, n, 2*n, 3*n-1]:
    ax.axvline(x=pos, color='gray', linestyle=':', linewidth=1)

ax.set_xticks([0, n, 2*n, 3*n-1])
ax.set_xticklabels(['Γ', 'K', 'M', 'Γ'], fontsize=14)
ax.set_ylabel('Energy (eV)', fontsize=12)
ax.set_title('Graphene Electronic Band Structure\n'
             'Tight-Binding Model', fontsize=13)
ax.set_ylim(-10, 10)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('results/graphene_bands.png', dpi=150)
plt.show()

# ============================================================
# 9. Key Results
# ============================================================
print("="*40)
print("KEY RESULTS")
print("="*40)
print(f"Energy at Γ : ±{energy(0,0)[0]:.3f} eV")
print(f"Energy at K : ±{energy(K[0],K[1])[0]:.2e} eV")
print(f"Bandwidth   :  {2*np.max(E_plus):.3f} eV")
print(f"Band Gap    :  {2*np.min(E_plus):.2e} eV  → semimetal")
print("="*40)
