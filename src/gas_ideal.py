import sympy
from sympy.plotting import plot
import numpy as np
import matplotlib.pyplot as plt

from collections import namedtuple

plt.style.use("fivethirtyeight")

Coordenadas = namedtuple("Coordenadas", "V T P")


class GasIdeal:

    CONSTANTE_GASES = 0.082057366080960  # atm L / (mol K)
    P, V, T, R, n = sympy.symbols("P V T R n", posivite=True)
    lei_gases_ideais = sympy.Eq(P * V, n * R * T)

    def __init__(self, mol=1):
        self.mol = mol

    def _resolver_para(self, simbolo, mol=1):
        equacao = sympy.solve(self.lei_gases_ideais, simbolo)[0].subs(
            {self.R: self.CONSTANTE_GASES, self.n: mol}
        )
        return equacao

    def plot_2d(self, eixos_xy="PV", constante=373.15, faixa_abscissa=(0.1, 4)):
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=(1, 1, 1))

        match eixos_xy:
            case "PV":
                abscissa = self.P
                ordenada = self.V
                simbolo_constante = self.T
                ax.set_xlabel("Pressão / atm")
                ax.set_ylabel("Volume / litro")
                legenda = f"T = {constante:.1f} K"
            case "TV":
                abscissa = self.T
                ordenada = self.V
                simbolo_constante = self.P
                ax.set_xlabel("Temperatura / K")
                ax.set_ylabel("Volume / litro")
                legenda = f"P = {constante:.2f} atm"
            case "TP":
                abscissa = self.T
                ordenada = self.P
                simbolo_constante = self.V
                ax.set_xlabel("Temperatura / K")
                ax.set_ylabel("Pressão / atm")
                legenda = f"V = {constante:.2f} L"
            case _:
                raise ValueError("Eixos inválidos. Tente 'PV', 'TV' ou 'TP'.")

        equacao = self._resolver_para(ordenada).subs({simbolo_constante: constante})
        p = plot(equacao, (abscissa, *faixa_abscissa), show=False)
        data = p[0].get_points()
        ax.plot(*data, label=legenda)
        ax.legend()
        return fig, ax

    def _grid_points(
        self,
        volume_array,
        temperature_array,
    ):
        volume_matrix, temperature_matrix = np.meshgrid(volume_array, temperature_array)
        pressure_matrix = (
            self.mol * self.CONSTANTE_GASES * temperature_matrix / volume_matrix
        )
        return volume_matrix, temperature_matrix, pressure_matrix

    def plot_3d(
        self,
        volume_array,
        temperature_array,
        labels=("Volume / L", "Temperatura / K", "Pressão / atm"),
        step=10,
        mostrar_ponto=False,
        mostrar_curva_VT=False,
        mostrar_curva_PV=False,
        mostrar_curva_PT=False,
        ponto_VT=(1, 1),
        visao_inicial=(None, None),
    ):
        volume_matrix, temperature_matrix, pressure_matrix = self._grid_points(
            volume_array, temperature_array
        )
        ax = plt.gca()  # gca = get current axis
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
        ax.plot_wireframe(
            volume_matrix,
            temperature_matrix,
            pressure_matrix,
            rstride=step,
            cstride=step,
            alpha=0.05,
        )

        pressao = self.CONSTANTE_GASES * ponto_VT[1] / ponto_VT[0]
        ponto = Coordenadas(*ponto_VT, pressao)
        if mostrar_curva_VT:
            temp_array = pressao * volume_array / self.CONSTANTE_GASES
            temp_array[temp_array > np.max(temperature_array)] = np.nan
            ax.plot(
                volume_array, temp_array, pressao, c="g", zdir="z", label="Curva VT"
            )
        if mostrar_curva_PV:
            pres_array = self.CONSTANTE_GASES * ponto.T / volume_array
            ax.plot(
                volume_array, pres_array, ponto.T, c="y", zdir="y", label="Curva PV"
            )
        if mostrar_curva_PT:
            pres_array = self.CONSTANTE_GASES * temperature_array / ponto.V
            ax.plot(
                temperature_array,
                pres_array,
                ponto.V,
                c="r",
                zdir="x",
                label="Curva PT",
            )
        if mostrar_ponto:
            ax.scatter(ponto.V, ponto.T, ponto.P, color="black", s=100)
        ax.view_init(*visao_inicial)
        ax.legend(bbox_to_anchor=(0.5, -0.3), loc="lower center", ncol=3)
        return ax


if __name__ == "__main__":
    gas_ideal = GasIdeal()

    print(gas_ideal.P)
    print(gas_ideal.CONSTANTE_GASES)
    print(gas_ideal.lei_gases_ideais)

    gas_ideal.plot_2d()
    gas_ideal.plot_2d("TV", 5, (0.1, 400))
    gas_ideal.plot_2d("TP", 5, (0.1, 400))

    vol = np.linspace(1, 10, 100)
    temp = np.linspace(1, 300, 100)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    gas_ideal.plot_3d(vol, temp, step=1)
    gas_ideal.plot_3d(
        vol,
        temp,
        step=1,
        mostrar_ponto=True,
        ponto_VT=(2, 250),
        mostrar_curva_VT=True,
        mostrar_curva_PV=True,
        mostrar_curva_PT=True,
    )

    plt.show()
