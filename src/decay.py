from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from uncertainties import unumpy
from scipy.optimize import curve_fit
import pandas as pd

from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]

DADOS = pd.read_csv(
    f"{PROJECT_ROOT}/data/betaDecay.txt",
    skiprows=2,
    delimiter="\s+",
    names=("dias", "contagem", "incerteza"),
)


class DecaimentoRadioativo:
    def __init__(
        self,
        tempo,
        contagem,
        incerteza,
        literatura_pre_exp=None,
        literatura_meia_vida=None,
        literatura_numero_pontos=None,
    ):
        self.tempo = tempo
        self.contagem = contagem
        self.incerteza = incerteza
        self.contagem_com_incerteza = unumpy.uarray(self.contagem, self.incerteza)
        self.literatura_pre_exp = literatura_pre_exp
        self.literatura_meia_vida = literatura_meia_vida
        self.literatura_numero_pontos = literatura_numero_pontos
        self.chutes_iniciais_fit_exp = [
            self.literatura_pre_exp,
            np.log(2) / self.literatura_meia_vida,
            0,
        ]

    @staticmethod
    def exponencial(variavel, pre_exp, taxa_decaimento, constante):
        return pre_exp * np.exp(-taxa_decaimento * variavel) + constante

    def fit_exponencial(self):
        popt, pcov = curve_fit(
            f=self.exponencial,
            xdata=self.tempo,
            ydata=self.contagem,
            p0=self.chutes_iniciais_fit_exp,
            sigma=self.incerteza,
            absolute_sigma=True,
        )
        perr = np.sqrt(np.diag(pcov))
        ParametrosFit = namedtuple(
            "Parâmetros",
            ["pre_exp", "taxa_decaimento", "constante"],
        )
        ResultadoFit = namedtuple("Fit", ["valores_otimos", "covariancia", "erro"])
        resultado = ResultadoFit(ParametrosFit(*popt), pcov, ParametrosFit(*perr))
        return resultado

    @property
    def tempo_de_meia_vida(self):
        taxa_decaimento = unumpy.uarray(
            self.fit_exponencial().valores_otimos.taxa_decaimento,
            self.fit_exponencial().erro.taxa_decaimento,
        )
        return np.log(2) / taxa_decaimento

    def pontos_literatura(self, linearizacao=False, intervalo_de_tempo=(0, 101)):
        literatura_cte_tempo_exp = self.literatura_meia_vida / np.log(2)
        t_teorico = np.linspace(*intervalo_de_tempo, self.literatura_numero_pontos)
        contagem_teorico = self.literatura_pre_exp * np.exp(
            -t_teorico / literatura_cte_tempo_exp
        )
        if linearizacao:
            contagem_teorico = np.log(contagem_teorico)
        return t_teorico, contagem_teorico

    def plot(
        self,
        erro=True,
        linearizacao=False,
        curva_literatura=False,
        fit=False,
        escala_log10=False,
    ):
        fig, ax = plt.subplots()

        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.grid(visible=True, axis="both", which="major", linestyle="--", linewidth=1.5)
        ax.minorticks_on()
        ax.grid(visible=True, axis="both", which="minor", linestyle=":", linewidth=1.0)
        ax.set_axisbelow(True)

        if escala_log10:
            linearizacao = False
            ax.set_yscale("log")
            ax.yaxis.set_major_formatter(FormatStrFormatter("%0.2f"))
            ax.set_ylabel(r"$\log_{10}$Contagem")

        if linearizacao:
            y = unumpy.log(self.contagem_com_incerteza)
            ax.set_ylabel(r"$\ln$Contagem")
        else:
            y = self.contagem_com_incerteza
            if not escala_log10:
                ax.set_ylabel("Contagem")

        ax.errorbar(
            self.tempo,
            unumpy.nominal_values(y),
            fmt="ro",
            label="Experimento",
            yerr=unumpy.std_devs(y),
            markersize=5,
            ecolor="black" if erro else "white",
            capsize=3,
        )
        ax.set_xlabel("Tempo / dias")

        if curva_literatura:
            ax.plot(*self.pontos_literatura(linearizacao), "b-", label="Literatura")

        if fit:
            popt, _, _ = self.fit_exponencial()
            if linearizacao:
                y_fit = np.log(self.exponencial(self.tempo, *popt))
            else:
                y_fit = self.exponencial(self.tempo, *popt)
            ax.plot(self.tempo, y_fit, "g-", label="Fit")

        ax.legend()
        fig.set_tight_layout(True)
        return fig, ax


if __name__ == "__main__":
    tempo = DADOS["dias"]
    contagem = DADOS["contagem"]
    incerteza = DADOS["incerteza"]

    fosforo32 = DecaimentoRadioativo(
        tempo,
        contagem,
        incerteza,
        literatura_pre_exp=1000,
        literatura_meia_vida=14.29,
        literatura_numero_pontos=120,
    )

    fosforo32.plot()
    fosforo32.plot(erro=False)
    fosforo32.plot(escala_log10=True)
    fosforo32.plot(escala_log10=True, curva_literatura=True)
    fosforo32.plot(escala_log10=True, curva_literatura=True, fit=True)
    fosforo32.plot(
        escala_log10=True, curva_literatura=True, fit=True, linearizacao=True
    )
    fosforo32.plot(curva_literatura=True)
    fosforo32.plot(curva_literatura=True, fit=True)
    fosforo32.plot(linearizacao=True)
    fosforo32.plot(linearizacao=True, curva_literatura=True)
    fosforo32.plot(linearizacao=True, curva_literatura=True, fit=True)
    plt.show()

    print(f"Valores otimizados: {fosforo32.fit_exponencial().valores_otimos}")
    # print(f"Valores covariância: {fosforo32.fit_exponencial().covariancia}")
    print(f"Valores dos erros: {fosforo32.fit_exponencial().erro}")
    resultado_fit = unumpy.uarray(
        fosforo32.fit_exponencial().valores_otimos, fosforo32.fit_exponencial().erro
    )
    print(f"Resultado fit: {resultado_fit}")

    print(f"t1/2 literatura: {fosforo32.literatura_meia_vida}")
    print(f"t1/2 calculado: {fosforo32.tempo_de_meia_vida}")
