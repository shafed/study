"""
=============================================================================
Сравнительный анализ семантических пространств LSA и BERT
=============================================================================
Численный эксперимент: алгебраическая структура и семантическая
выразительность линейной (LSA) и нелинейной контекстуальной (BERT) моделей.

Запуск:
    python experiment.py

Результаты:
    results/   — CSV-таблицы
    figures/   — графики (PNG, 300 dpi)
=============================================================================
"""

import os
import time
import warnings
from typing import Dict, List, Optional, Tuple

# ── визуализация ─────────────────────────────────────────────
import matplotlib
import numpy as np
import pandas as pd
from datasets import load_dataset
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist

# ── sentence-transformers / datasets ─────────────────────────
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# ── sklearn ──────────────────────────────────────────────────
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    adjusted_rand_score,
    f1_score,
    silhouette_score,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

matplotlib.rcParams.update(
    {
        "figure.dpi": 150,
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
    }
)
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# ╔════════════════════════════════════════════════════════════╗
# ║  1. КОНФИГУРАЦИЯ                                         ║
# ╚════════════════════════════════════════════════════════════╝

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

LSA_DIMS = [50, 100, 200, 300, 500]
LSA_DEFAULT_K = 300  # для основного попарного сравнения
BERT_MODEL = "all-MiniLM-L6-v2"

# Все 20 категорий
NG_CATEGORIES = None  # None = все категории

K_NEIGHBORS = 5  # для hubness
N_HEATMAP_SAMPLES = 200  # для тепловой карты
N_COS_PAIRS = 10_000  # для гистограммы cos-sim
BERT_BATCH = 128

OUT_DIR = os.path.join(PROJECT_ROOT, "results")
FIG_DIR = os.path.join(SCRIPT_DIR, "figures")


def unique_preserve_order(items: List[str]) -> List[str]:
    """Удаляет дубликаты, сохраняя стабильный порядок."""
    return list(dict.fromkeys(items))


# ╔════════════════════════════════════════════════════════════╗
# ║  2. ЗАГРУЗКА ДАННЫХ                                      ║
# ╚════════════════════════════════════════════════════════════╝


def load_stsb() -> Tuple[List[str], List[str], np.ndarray]:
    """STS Benchmark (validation, 0-5 scale)."""
    print("[DATA] STS-B …")
    try:
        ds = load_dataset("mteb/stsbenchmark-sts", split="test")
        s1, s2, sc = ds["sentence1"], ds["sentence2"], ds["score"]
    except Exception:
        ds = load_dataset("glue", "stsb", split="validation")
        s1, s2, sc = ds["sentence1"], ds["sentence2"], ds["label"]
    scores = np.asarray(sc, dtype=float)
    print(f"       {len(scores)} пар предложений")
    return list(s1), list(s2), scores


def load_newsgroups():
    """20 Newsgroups — 6 категорий, без служебных блоков."""
    print("[DATA] 20 Newsgroups …")
    kw = dict(
        categories=NG_CATEGORIES,
        remove=("headers", "footers", "quotes"),
        random_state=RANDOM_STATE,
    )
    train = fetch_20newsgroups(subset="train", **kw)
    test = fetch_20newsgroups(subset="test", **kw)

    # Отфильтруем пустые документы
    def _filter(bunch):
        mask = [i for i, t in enumerate(bunch.data) if len(t.strip()) > 10]
        bunch.data = [bunch.data[i] for i in mask]
        bunch.target = bunch.target[mask]
        return bunch

    train, test = _filter(train), _filter(test)
    print(f"       Train {len(train.data)}  |  Test {len(test.data)}")
    print(f"       Категории: {train.target_names}")
    return train, test


def load_mrpc() -> Tuple[List[str], List[str], np.ndarray]:
    """MRPC — Microsoft Research Paraphrase Corpus."""
    print("[DATA] MRPC …")
    ds = load_dataset("glue", "mrpc", split="validation")
    labels = np.array(ds["label"])
    print(f"       {len(labels)} пар  |  парафраз {labels.sum()}")
    return list(ds["sentence1"]), list(ds["sentence2"]), labels


# ╔════════════════════════════════════════════════════════════╗
# ║  3. МОДЕЛИ-ОБЁРТКИ                                       ║
# ╚════════════════════════════════════════════════════════════╝


class LSAEmbedder:
    """TF-IDF (sublinear_tf) → Truncated SVD → L₂-нормализация."""

    def __init__(self, n_components: int = 300):
        self.n_components = n_components
        self.tfidf = TfidfVectorizer(
            sublinear_tf=True,
            max_features=50_000,
            min_df=2,
            max_df=0.95,
            stop_words="english",
        )
        self.svd = TruncatedSVD(
            n_components=n_components,
            random_state=RANDOM_STATE,
        )

    # ---- API ----
    def fit(self, texts: List[str]) -> "LSAEmbedder":
        X = self.tfidf.fit_transform(texts)
        self.svd.fit(X)
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        X = self.tfidf.transform(texts)
        Z = self.svd.transform(X)
        return normalize(Z, norm="l2")

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        X = self.tfidf.fit_transform(texts)
        Z = self.svd.fit_transform(X)
        return normalize(Z, norm="l2")

    @property
    def singular_values(self) -> np.ndarray:
        return self.svd.singular_values_

    @property
    def explained_variance_ratio(self) -> np.ndarray:
        return self.svd.explained_variance_ratio_


class BERTEmbedder:
    """all-MiniLM-L6-v2 через sentence-transformers."""

    def __init__(self, model_name: str = BERT_MODEL):
        print(f"[MODEL] Загрузка BERT: {model_name} …")
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        print(f"        dim = {self.dim}")

    def encode(
        self, texts, batch_size: int = 128, show_progress: bool = True
    ) -> np.ndarray:
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=True,  # L₂-норм
        )


# ╔════════════════════════════════════════════════════════════╗
# ║  4. ИНТРИНСИВНЫЕ МЕТРИКИ                                 ║
# ╚════════════════════════════════════════════════════════════╝


def participation_ratio(E: np.ndarray) -> float:
    """PR = (Σ λ_i)² / Σ λ_i², λ — собственные числа Cov."""
    cov = np.cov(E, rowvar=False)
    lam = np.linalg.eigvalsh(cov)
    lam = np.maximum(lam, 0.0)
    s = lam.sum()
    s2 = (lam**2).sum()
    return (s**2) / s2 if s2 > 0 else 0.0


def effective_rank(E: np.ndarray) -> float:
    """ER = exp(H(p)),  p_i = σ_i / Σ σ_j."""
    _, sv, _ = np.linalg.svd(E, full_matrices=False)
    sv = sv[sv > 0]
    p = sv / sv.sum()
    H = -np.sum(p * np.log(p))
    return float(np.exp(H))


def isotropy_score(E: np.ndarray) -> float:
    """min(λ) / max(λ), λ — собственные числа Cov."""
    cov = np.cov(E, rowvar=False)
    lam = np.linalg.eigvalsh(cov)
    lam = lam[lam > 1e-12]
    if len(lam) == 0:
        return 0.0
    return float(lam.min() / lam.max())


def hubness_score(E: np.ndarray, k: int = 5) -> float:
    """Skewness N_k — скошенность k-вхождений."""
    nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine", algorithm="brute")
    nn.fit(E)
    _, idx = nn.kneighbors(E)
    idx = idx[:, 1:]  # убираем self
    N_k = np.bincount(idx.ravel(), minlength=E.shape[0])
    return float(stats.skew(N_k))


def compute_intrinsic(
    E: np.ndarray, name: str = "", k: int = K_NEIGHBORS
) -> Dict[str, float]:
    """Собрать все 4 интринсивные метрики."""
    print(f"\n[INTRINSIC] «{name}»  shape={E.shape}")
    t0 = time.time()

    pr = participation_ratio(E)
    er = effective_rank(E)
    iso = isotropy_score(E)
    hub = hubness_score(E, k)

    print(f"   Participation Ratio : {pr:.2f}")
    print(f"   Effective Rank      : {er:.2f}")
    print(f"   Isotropy Score      : {iso:.6f}")
    print(f"   Hubness  (skewness) : {hub:.4f}")
    print(f"   ({time.time() - t0:.1f} с)")
    return dict(
        participation_ratio=pr, effective_rank=er, isotropy_score=iso, hubness_score=hub
    )


# ╔════════════════════════════════════════════════════════════╗
# ║  5. ЭКСТРИНСИВНЫЕ МЕТРИКИ                                ║
# ╚════════════════════════════════════════════════════════════╝


def evaluate_sts(e1: np.ndarray, e2: np.ndarray, gold: np.ndarray) -> Dict[str, float]:
    """Spearman ρ (cos-sim vs gold)."""
    cos = np.sum(e1 * e2, axis=1)  # dot = cos для L₂-norm
    rho, p = stats.spearmanr(cos, gold)
    return dict(spearman_rho=rho, p_value=p)


def evaluate_classification(Xtr, Xte, ytr, yte) -> Dict[str, float]:
    """Logistic Regression → Accuracy + F1-macro."""
    clf = LogisticRegression(
        max_iter=1000, C=1.0, solver="lbfgs", random_state=RANDOM_STATE
    )
    clf.fit(Xtr, ytr)
    yp = clf.predict(Xte)
    return dict(
        accuracy=accuracy_score(yte, yp), f1_macro=f1_score(yte, yp, average="macro")
    )


def evaluate_clustering(E: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
    """KMeans → ARI + Silhouette (cosine)."""
    n_cl = len(np.unique(labels))
    km = KMeans(n_clusters=n_cl, n_init=10, max_iter=300, random_state=RANDOM_STATE)
    pred = km.fit_predict(E)
    ari = adjusted_rand_score(labels, pred)
    sil = silhouette_score(E, pred, metric="cosine", sample_size=min(5000, len(E)))
    return dict(ari=ari, silhouette=sil)


def evaluate_paraphrase(
    e1: np.ndarray, e2: np.ndarray, labels: np.ndarray
) -> Dict[str, float]:
    """F1 с оптимальным порогом на cos-sim."""
    cos = np.sum(e1 * e2, axis=1)
    best_f1, best_th = 0.0, 0.5
    for th in np.arange(0.0, 1.01, 0.01):
        f = f1_score(labels, (cos >= th).astype(int), zero_division=0)
        if f > best_f1:
            best_f1, best_th = f, th
    return dict(f1=best_f1, optimal_threshold=best_th)


# ╔════════════════════════════════════════════════════════════╗
# ║  6. ВИЗУАЛИЗАЦИЯ                                         ║
# ╚════════════════════════════════════════════════════════════╝


def _save(fig, path: Optional[str]):
    if path:
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"  → сохранено: {path}")


# ── 6.1  Спектр сингулярных чисел ────────────────────────────
def plot_sv_spectrum(emb_dict: Dict[str, np.ndarray], path: Optional[str] = None):
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, E in emb_dict.items():
        _, sv, _ = np.linalg.svd(E, full_matrices=False)
        ax.plot(range(1, len(sv) + 1), sv / sv[0], lw=2, label=name)
    ax.set(
        xlabel="Индекс компоненты",
        ylabel="σ_i / σ_1  (нормализованное)",
        title="Спектр сингулярных чисел",
        yscale="log",
    )
    ax.legend()
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ── 6.2  Тепловые карты cos-sim ──────────────────────────────
def plot_cos_heatmaps(
    emb_dict: Dict[str, np.ndarray],
    n: int = N_HEATMAP_SAMPLES,
    path: Optional[str] = None,
):
    ncols = len(emb_dict)
    fig, axes = plt.subplots(1, ncols, figsize=(7 * ncols, 6))
    if ncols == 1:
        axes = [axes]
    for ax, (name, E) in zip(axes, emb_dict.items()):
        idx = np.random.choice(E.shape[0], min(n, E.shape[0]), replace=False)
        C = E[idx] @ E[idx].T
        off = C[np.triu_indices(len(idx), k=1)]
        sns.heatmap(
            C,
            ax=ax,
            cmap="RdBu_r",
            center=0,
            vmin=-0.5,
            vmax=1.0,
            xticklabels=False,
            yticklabels=False,
        )
        ax.set_title(f"{name}\nmean off-diag = {off.mean():.3f}")
    fig.suptitle("Тепловые карты косинусного сходства", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ── 6.3  Гистограмма cos-sim случайных пар ───────────────────
def plot_cos_distribution(
    emb_dict: Dict[str, np.ndarray],
    n_pairs: int = N_COS_PAIRS,
    path: Optional[str] = None,
):
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, E in emb_dict.items():
        i = np.random.randint(0, E.shape[0], n_pairs)
        j = np.random.randint(0, E.shape[0], n_pairs)
        m = i != j
        i, j = i[m], j[m]
        cos = np.sum(E[i] * E[j], axis=1)
        ax.hist(cos, bins=100, alpha=0.55, label=name, density=True)
    ax.set(
        xlabel="Косинусное сходство",
        ylabel="Плотность",
        title="Распределение cos-sim случайных пар",
    )
    ax.legend()
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ── 6.4  Чувствительность LSA (k vs ρ) ──────────────────────
def plot_lsa_sensitivity(
    sts_by_k: Dict[int, float], bert_rho: float, path: Optional[str] = None
):
    fig, ax = plt.subplots(figsize=(10, 6))
    ks = sorted(sts_by_k)
    rhos = [sts_by_k[k] for k in ks]
    ax.plot(ks, rhos, "bo-", lw=2, ms=8, label="LSA")
    ax.axhline(bert_rho, color="r", ls="--", lw=2, label=f"BERT ({bert_rho:.4f})")
    ax.set(
        xlabel="Размерность k",
        ylabel="Spearman ρ",
        title="Чувствительность LSA к размерности (STS-B)",
    )
    ax.set_xticks(ks)
    ax.legend()
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ── 6.5  Столбчатое сравнение экстринсивных метрик ──────────
def plot_extrinsic(lsa: Dict, bert: Dict, path: Optional[str] = None):
    names = ["STS (ρ)", "Accuracy", "F1-macro", "ARI", "Silhouette", "MRPC F1"]
    keys = [
        "sts_spearman",
        "cls_accuracy",
        "cls_f1",
        "cluster_ari",
        "cluster_silhouette",
        "mrpc_f1",
    ]
    lv = [lsa[k] for k in keys]
    bv = [bert[k] for k in keys]
    x = np.arange(len(names))
    w = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    b1 = ax.bar(
        x - w / 2,
        lv,
        w,
        label=f"LSA (k={LSA_DEFAULT_K})",
        color="steelblue",
        alpha=0.85,
    )
    b2 = ax.bar(x + w / 2, bv, w, label="BERT", color="coral", alpha=0.85)
    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{h:.3f}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=8,
            )
    ax.set(ylabel="Значение", title="Экстринсивные метрики: LSA vs BERT")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=12)
    ax.legend()
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ── 6.6  Столбчатое сравнение интринсивных метрик ───────────
def plot_intrinsic_bars(lsa_i: Dict, bert_i: Dict, path: Optional[str] = None):
    titles = [
        "Participation\nRatio",
        "Effective\nRank",
        "Isotropy\nScore",
        "Hubness\n(Skewness)",
    ]
    keys = ["participation_ratio", "effective_rank", "isotropy_score", "hubness_score"]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, t, k in zip(axes, titles, keys):
        vals = [lsa_i[k], bert_i[k]]
        bars = ax.bar(["LSA", "BERT"], vals, color=["steelblue", "coral"], alpha=0.85)
        ax.set_title(t)
        for b in bars:
            h = b.get_height()
            fmt = f"{h:.4f}" if abs(h) < 1 else f"{h:.2f}"
            ax.annotate(
                fmt,
                xy=(b.get_x() + b.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=9,
            )
    fig.suptitle("Интринсивные (алгебраические) метрики", fontsize=14)
    fig.tight_layout()
    _save(fig, path)
    plt.show()


# ╔════════════════════════════════════════════════════════════╗
# ║  7. ГЕНЕРАТОР LaTeX-ТАБЛИЦ                               ║
# ╚════════════════════════════════════════════════════════════╝


def to_latex(df: pd.DataFrame, caption: str, label: str) -> str:
    """Обёртка DataFrame → LaTeX table."""
    body = df.to_latex(
        index=False,
        float_format="%.4f",
        column_format="l" + "c" * (len(df.columns) - 1),
    )
    return (
        f"\\begin{{table}}[htbp]\n\\centering\n"
        f"\\caption{{{caption}}}\n\\label{{{label}}}\n"
        f"{body}"
        f"\\end{{table}}\n"
    )


# ╔════════════════════════════════════════════════════════════╗
# ║  8. ОСНОВНОЙ ПАЙПЛАЙН                                    ║
# ╚════════════════════════════════════════════════════════════╝


def main():
    t_start = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    sep = "=" * 70
    print(f"\n{sep}")
    print("  СРАВНИТЕЛЬНЫЙ АНАЛИЗ СЕМАНТИЧЕСКИХ ПРОСТРАНСТВ LSA И BERT")
    print(f"{sep}\n")

    # ── Загрузка данных ──────────────────────────────────────
    sts_s1, sts_s2, sts_gold = load_stsb()
    ng_train, ng_test = load_newsgroups()
    mrpc_s1, mrpc_s2, mrpc_y = load_mrpc()

    # ── Инициализация BERT ───────────────────────────────────
    bert = BERTEmbedder(BERT_MODEL)

    # ════════════════════════════════════════════════════════
    #  ЭТАП 1 — ГЕНЕРАЦИЯ ЭМБЕДДИНГОВ
    # ════════════════════════════════════════════════════════
    print(f"\n{sep}\n  ЭТАП 1: ГЕНЕРАЦИЯ ЭМБЕДДИНГОВ\n{sep}")

    # ── BERT ─────────────────────────────────────────────────
    print("\n[BERT] STS-B …")
    b_sts1 = bert.encode(sts_s1, BERT_BATCH)
    b_sts2 = bert.encode(sts_s2, BERT_BATCH)

    print("[BERT] 20 Newsgroups …")
    b_ng_tr = bert.encode(ng_train.data, BERT_BATCH)
    b_ng_te = bert.encode(ng_test.data, BERT_BATCH)

    print("[BERT] MRPC …")
    b_mr1 = bert.encode(mrpc_s1, BERT_BATCH)
    b_mr2 = bert.encode(mrpc_s2, BERT_BATCH)

    # ── LSA: чувствительность к k ────────────────────────────
    sts_all = unique_preserve_order(sts_s1 + sts_s2)
    mrpc_all = unique_preserve_order(mrpc_s1 + mrpc_s2)

    lsa_sts_by_k: Dict[int, float] = {}
    print("\n[LSA] Анализ чувствительности к k …")
    for k in LSA_DIMS:
        lsa = LSAEmbedder(k)
        lsa.fit(sts_all)
        e1 = lsa.transform(sts_s1)
        e2 = lsa.transform(sts_s2)
        rho = evaluate_sts(e1, e2, sts_gold)["spearman_rho"]
        lsa_sts_by_k[k] = rho
        print(f"   k={k:>3d}  →  Spearman ρ = {rho:.4f}")

    # ── LSA (k_main) для основного сравнения ─────────────────
    K = LSA_DEFAULT_K
    print(f"\n[LSA] Основная модель  k = {K}")

    lsa_ng = LSAEmbedder(K)
    l_ng_tr = lsa_ng.fit_transform(ng_train.data)
    l_ng_te = lsa_ng.transform(ng_test.data)

    lsa_sts = LSAEmbedder(K)
    lsa_sts.fit(sts_all)
    l_sts1 = lsa_sts.transform(sts_s1)
    l_sts2 = lsa_sts.transform(sts_s2)

    lsa_mr = LSAEmbedder(K)
    lsa_mr.fit(mrpc_all)
    l_mr1 = lsa_mr.transform(mrpc_s1)
    l_mr2 = lsa_mr.transform(mrpc_s2)

    # LSA explained variance
    ev = lsa_ng.explained_variance_ratio.sum()
    print(f"   Объяснённая дисперсия (20NG, k={K}): {ev:.4f}")

    # ════════════════════════════════════════════════════════
    #  ЭТАП 2 — СПЕКТРАЛЬНЫЙ АНАЛИЗ
    # ════════════════════════════════════════════════════════
    print(f"\n{sep}\n  ЭТАП 2: СПЕКТРАЛЬНЫЙ АНАЛИЗ\n{sep}")

    lsa_intr = compute_intrinsic(l_ng_te, f"LSA (k={K})", K_NEIGHBORS)
    bert_intr = compute_intrinsic(b_ng_te, "BERT", K_NEIGHBORS)

    emb_pair = {f"LSA (k={K})": l_ng_te, "BERT": b_ng_te}

    plot_sv_spectrum(emb_pair, path=os.path.join(FIG_DIR, "sv_spectrum.png"))
    plot_cos_heatmaps(emb_pair, path=os.path.join(FIG_DIR, "cos_heatmaps.png"))
    plot_cos_distribution(emb_pair, path=os.path.join(FIG_DIR, "cos_distribution.png"))
    plot_intrinsic_bars(
        lsa_intr, bert_intr, path=os.path.join(FIG_DIR, "intrinsic_bars.png")
    )

    # ════════════════════════════════════════════════════════
    #  ЭТАП 3 — ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ
    # ════════════════════════════════════════════════════════
    print(f"\n{sep}\n  ЭТАП 3: ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ\n{sep}")

    # 3.1 STS-B
    print("\n─── STS-B ───")
    r_lsa_sts = evaluate_sts(l_sts1, l_sts2, sts_gold)
    r_bert_sts = evaluate_sts(b_sts1, b_sts2, sts_gold)
    print(
        f"  LSA   ρ = {r_lsa_sts['spearman_rho']:.4f}  (p = {r_lsa_sts['p_value']:.2e})"
    )
    print(
        f"  BERT  ρ = {r_bert_sts['spearman_rho']:.4f}  "
        f"(p = {r_bert_sts['p_value']:.2e})"
    )

    # 3.2 Классификация
    print("\n─── Классификация (20 Newsgroups) ───")
    r_lsa_cls = evaluate_classification(
        l_ng_tr, l_ng_te, ng_train.target, ng_test.target
    )
    r_bert_cls = evaluate_classification(
        b_ng_tr, b_ng_te, ng_train.target, ng_test.target
    )
    for tag, r in [("LSA ", r_lsa_cls), ("BERT", r_bert_cls)]:
        print(f"  {tag}  Acc = {r['accuracy']:.4f}  F1-macro = {r['f1_macro']:.4f}")

    # 3.3 Кластеризация
    print("\n─── Кластеризация (20 Newsgroups test) ───")
    r_lsa_cl = evaluate_clustering(l_ng_te, ng_test.target)
    r_bert_cl = evaluate_clustering(b_ng_te, ng_test.target)
    for tag, r in [("LSA ", r_lsa_cl), ("BERT", r_bert_cl)]:
        print(f"  {tag}  ARI = {r['ari']:.4f}  Silhouette = {r['silhouette']:.4f}")

    # 3.4 Парафразы
    print("\n─── Обнаружение парафраз (MRPC) ───")
    r_lsa_mr = evaluate_paraphrase(l_mr1, l_mr2, mrpc_y)
    r_bert_mr = evaluate_paraphrase(b_mr1, b_mr2, mrpc_y)
    for tag, r in [("LSA ", r_lsa_mr), ("BERT", r_bert_mr)]:
        print(f"  {tag}  F1 = {r['f1']:.4f}  (θ = {r['optimal_threshold']:.2f})")

    # ════════════════════════════════════════════════════════
    #  СВОДКА
    # ════════════════════════════════════════════════════════
    print(f"\n{sep}\n  СВОДНЫЕ РЕЗУЛЬТАТЫ\n{sep}")

    lsa_ext = dict(
        sts_spearman=r_lsa_sts["spearman_rho"],
        cls_accuracy=r_lsa_cls["accuracy"],
        cls_f1=r_lsa_cls["f1_macro"],
        cluster_ari=r_lsa_cl["ari"],
        cluster_silhouette=r_lsa_cl["silhouette"],
        mrpc_f1=r_lsa_mr["f1"],
    )
    bert_ext = dict(
        sts_spearman=r_bert_sts["spearman_rho"],
        cls_accuracy=r_bert_cls["accuracy"],
        cls_f1=r_bert_cls["f1_macro"],
        cluster_ari=r_bert_cl["ari"],
        cluster_silhouette=r_bert_cl["silhouette"],
        mrpc_f1=r_bert_mr["f1"],
    )

    # Единая таблица
    rows = [
        ("STS Spearman ρ", r_lsa_sts["spearman_rho"], r_bert_sts["spearman_rho"]),
        ("Classification Accuracy", r_lsa_cls["accuracy"], r_bert_cls["accuracy"]),
        ("Classification F1-macro", r_lsa_cls["f1_macro"], r_bert_cls["f1_macro"]),
        ("Clustering ARI", r_lsa_cl["ari"], r_bert_cl["ari"]),
        ("Clustering Silhouette", r_lsa_cl["silhouette"], r_bert_cl["silhouette"]),
        ("MRPC F1", r_lsa_mr["f1"], r_bert_mr["f1"]),
        (
            "Participation Ratio",
            lsa_intr["participation_ratio"],
            bert_intr["participation_ratio"],
        ),
        ("Effective Rank", lsa_intr["effective_rank"], bert_intr["effective_rank"]),
        ("Isotropy Score", lsa_intr["isotropy_score"], bert_intr["isotropy_score"]),
        ("Hubness (Skewness)", lsa_intr["hubness_score"], bert_intr["hubness_score"]),
    ]
    df = pd.DataFrame(rows, columns=["Метрика", f"LSA (k={K})", "BERT"])

    print("\n" + df.to_string(index=False, float_format="%.4f"))

    # CSV
    csv_path = os.path.join(OUT_DIR, "results_summary.csv")
    df.to_csv(csv_path, index=False, float_format="%.4f")

    # LSA sensitivity CSV
    sens_df = pd.DataFrame(sorted(lsa_sts_by_k.items()), columns=["k", "spearman_rho"])
    sens_df.to_csv(
        os.path.join(OUT_DIR, "lsa_sensitivity.csv"), index=False, float_format="%.4f"
    )

    # LaTeX
    tex = to_latex(df, "Сводные результаты сравнения LSA и BERT", "tab:results")
    tex_path = os.path.join(OUT_DIR, "results_table.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)
    print(f"\n  LaTeX таблица → {tex_path}")

    # Оставшиеся графики
    plot_lsa_sensitivity(
        lsa_sts_by_k,
        r_bert_sts["spearman_rho"],
        path=os.path.join(FIG_DIR, "lsa_sensitivity.png"),
    )
    plot_extrinsic(lsa_ext, bert_ext, path=os.path.join(FIG_DIR, "extrinsic_bars.png"))

    elapsed = time.time() - t_start
    print(f"\n{'=' * 70}")
    print(f"  ГОТОВО.  Общее время: {elapsed / 60:.1f} мин")
    print(f"  Таблицы  → {OUT_DIR}/")
    print(f"  Графики  → {FIG_DIR}/")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
