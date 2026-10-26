"""Analisis estadistico del diseno de la validacion clinica (HU-07g): potencia, tamano de muestra y efecto de agrupamiento.

Reproduce las tablas de docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md (secciones 4.3 y 4.4). Requiere numpy.
Los supuestos (codigos por caso, correlacion intraclase rho, distribucion del calificador) NO vienen de datos reales:
son escenarios para dimensionar la prueba. El rho real se puede estimar con la hoja llena.

    python scripts/design_simulation.py              # todas las secciones
    python scripts/design_simulation.py --sims 3000  # mas simulaciones
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from icf.review import weighted_kappa  # noqa: E402

Z = 1.959964
Z_BETA = 0.841621  # potencia 80 %
CRITERIA = (("flexible", 0.80, 0.60), ("estricta/cobertura", 0.60, 0.40))  # (nombre, meta, piso)


def wilson_lb(k, n):
    p = np.asarray(k, dtype=float) / n
    d = 1 + Z * Z / n
    return (p + Z * Z / (2 * n) - Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))) / d


def p_pass_independent(n, p, target, floor):
    """P(observado >= meta y LB de Wilson >= piso) con k ~ Binomial(n, p), codigos independientes (exacto)."""
    k = np.arange(n + 1)
    ok = (k / n >= target) & (wilson_lb(k, n) >= floor)
    pmf = np.array([math.comb(n, int(i)) * p**i * (1 - p) ** (n - i) for i in k])
    return float(pmf[ok].sum())


def sim_clustered(rng, p, rho, cases, m, nsim):
    """Aciertos por caso ~ Beta-Binomial(m, p, rho): rho es la correlacion intraclase."""
    if rho <= 1e-9:
        return rng.binomial(m, p, size=(nsim, cases))
    s = 1 / rho - 1
    return rng.binomial(m, rng.beta(p * s, (1 - p) * s, size=(nsim, cases)))


def section_independent():
    print("## 4.3 Codigos independientes (exacto, binomial)\n")
    print("| n | criterio | real = piso | real = meta | real = meta + 10 |\n|---|---|---|---|---|")
    for n in (30, 60):
        for name, target, floor in CRITERIA:
            vals = [p_pass_independent(n, p, target, floor) for p in (floor, target, target + 0.10)]
            print(f"| {n} | {name} {target:.0%}/{floor:.0%} | " + " | ".join(f"{v:.3f}" for v in vals) + " |")
    print("\nObservado minimo para que el limite inferior alcance X:\n\n| LB >= | n=30 | n=45 | n=60 | n=90 |\n|---|---|---|---|---|")
    for floor in (0.40, 0.60, 0.70, 0.80):
        row = []
        for n in (30, 45, 60, 90):
            k = next(k for k in range(n + 1) if wilson_lb(k, n) >= floor)
            row.append(f"{k / n:.0%}")
        print(f"| {floor:.0%} | " + " | ".join(row) + " |")


def section_sample_size():
    print("\n## 4.4 (2) Tamano de muestra (alfa unilateral 2,5 %, potencia 80 %)\n")
    print("| criterio | N independientes | DEFF 1,4 / 1,8 / 2,2 | casos de 5 codigos |\n|---|---|---|---|")
    for name, s1, s0 in CRITERIA:
        n = math.ceil((Z * math.sqrt(s1 * (1 - s1)) + Z_BETA * math.sqrt(s0 * (1 - s0))) ** 2 / (s1 - s0) ** 2)
        deff = [math.ceil(n * d) for d in (1.4, 1.8, 2.2)]
        print(f"| {name} ({s0:.0%} -> {s1:.0%}) | {n} | {' / '.join(map(str, deff))} | {' / '.join(str(math.ceil(x / 5)) for x in deff)} |")


def section_clustered(rng, sims, cases, m, boot):
    n = cases * m
    print(f"\n## 4.4 (4) Agrupamiento: {cases} casos x {m} codigos (n={n}), {sims} simulaciones, bootstrap por caso con {boot} remuestras\n")
    print("| rho | DEFF | n efectivo | cobertura LB Wilson p=0,6 / 0,8 (nominal 97,5 %) | aprueba real=piso flex / estr (Wilson | bootstrap) | real=meta flex / estr | real=meta+10 flex / estr |")
    print("|---|---|---|---|---|---|---|")
    for rho in (0.0, 0.1, 0.2, 0.3):
        deff = 1 + (m - 1) * rho
        cover = [float((wilson_lb(sim_clustered(rng, p, rho, cases, m, 4000).sum(1), n) < p).mean()) for p in (0.6, 0.8)]
        cells = []
        for which in ("piso", "meta", "meta+10"):
            parts = []
            for _, target, floor in CRITERIA:
                p = {"piso": floor, "meta": target, "meta+10": min(target + 0.10, 0.99)}[which]
                K = sim_clustered(rng, p, rho, cases, m, sims)
                tot = K.sum(1)
                obs, lb_w = tot / n, wilson_lb(tot, n)
                idx = rng.integers(0, cases, size=(sims, boot, cases))
                bs = np.take_along_axis(np.broadcast_to(K[:, None, :], (sims, boot, cases)), idx, 2).sum(2) / n
                lb_b = np.quantile(bs, 0.025, axis=1)
                w, b = ((obs >= target) & (lb_w >= floor)).mean(), ((obs >= target) & (lb_b >= floor)).mean()
                parts.append(f"{w:.3f} | {b:.3f}" if which == "piso" else f"{w:.3f}")
            cells.append(" / ".join(parts))
        print(f"| {rho:.1f} | {deff:.1f} | {round(n / deff)} | {cover[0]:.3f} / {cover[1]:.3f} | " + " | ".join(cells) + " |")


def section_kappa(rng, reps=150, boot=300):
    print("\n## 4.4 (6) Kappa ponderado lineal con pocos pares (IC 95 % por bootstrap de pares)\n")
    probs = np.array([0.10, 0.20, 0.30, 0.25, 0.15])  # distribucion supuesta de la gravedad de la revisora

    def draw(n):
        r = rng.choice(5, size=n, p=probs)
        u = rng.random(n)
        shift = np.where(u < 0.55, 0, np.where(u < 0.90, rng.choice([-1, 1], n), rng.choice([-2, 2], n)))
        return r, np.clip(r + shift, 0, 4)

    big_r, big_s = draw(200000)
    print(f"Escenario: acuerdo exacto 55 %, dentro de +-1 el 90 %; kappa ponderado verdadero = {weighted_kappa(list(zip(big_r.tolist(), big_s.tolist())))}\n")
    print("| Pares | Ancho medio del IC | Limite inferior medio |\n|---|---|---|")
    for n in (10, 20, 30, 40, 60):
        widths, lows = [], []
        for _ in range(reps):
            r, s = draw(n)
            pairs = list(zip(r.tolist(), s.tolist()))
            ks = [k for k in (weighted_kappa([pairs[j] for j in rng.integers(0, n, n)]) for _ in range(boot)) if k is not None]
            if ks:
                lo, hi = np.quantile(ks, [0.025, 0.975])
                widths.append(hi - lo)
                lows.append(lo)
        print(f"| {n} | {np.mean(widths):.2f} | {np.mean(lows):.2f} |")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sims", type=int, default=1500)
    parser.add_argument("--boot", type=int, default=400)
    parser.add_argument("--cases", type=int, default=24)
    parser.add_argument("--codes-per-case", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20261021)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    section_independent()
    section_sample_size()
    section_clustered(rng, args.sims, args.cases, args.codes_per_case, args.boot)
    section_kappa(rng)
    return 0


if __name__ == "__main__":
    sys.exit(main())
