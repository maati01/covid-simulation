import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


def graph():
    plt.style.use('fivethirtyeight')

    def animate(i):
        data = pd.read_csv('statistics/data.csv')
        day = data['Day']
        susceptible = data['Susceptible']
        exposed = data['Exposed']
        infective = data['Infected']
        recovered = data['Recovered']

        plt.cla()

        # plt.plot(day, susceptible, label='Susceptible')
        plt.plot(day, exposed, label='Exposed')
        plt.plot(day, infective, label='Infected')
        plt.plot(day, recovered, label='Recovered')

        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()


#graph()
