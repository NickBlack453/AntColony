from tkinter import *
from tkinter import ttk

import ants


root = Tk()
root.title('Симулятор муравьиной колонии')
root.geometry('1100x500')
root.resizable(False, True)

queens = IntVar(value=1)
soldiers = IntVar(value=50)
workers = IntVar(value=200)
babies = IntVar(value=20)
resources = DoubleVar(value=500)
days = IntVar(value=365)

queensResult = IntVar(value=0)
soldiersResult = IntVar(value=0)
workersResult = IntVar(value=0)
babiesResult = IntVar(value=0)
resourcesResult = DoubleVar(value=0)
daysResult = IntVar(value=0)

historyResult = Variable(value=[])

maxQueens = IntVar(value=10)
queenBabies = IntVar(value=4)
queenResources = DoubleVar(value=10000)
probSoldier = DoubleVar(value=0.25)
probAttack = DoubleVar(value=0.01)
pctAttack = DoubleVar(value=10)
powerAttack = IntVar(value=9)


frameState = ttk.Frame(borderwidth=1, relief=SOLID, padding=2)
frameState.grid(row=0, column=0, padx=2, pady=4, sticky=N)

ttk.Label(frameState, text='Состояние:', padding=2, justify=CENTER,
          font=('Arial', 12)).grid(row=0, column=0)
ttk.Label(frameState, text='исходное', padding=2, justify=CENTER,
          font=('Arial', 10)).grid(row=0, column=1)
ttk.Label(frameState, text='финальное', padding=2, justify=CENTER,
          font=('Arial', 10)).grid(row=0, column=2)

ttk.Label(frameState, text='Матки').grid(row=1, column=0)
ttk.Entry(frameState, textvariable=queens, width=7).grid(row=1, column=1)
ttk.Label(frameState, textvariable=queensResult).grid(row=1, column=2)
ttk.Label(frameState, text='Солдаты').grid(row=2, column=0)
ttk.Entry(frameState, textvariable=soldiers, width=7).grid(row=2, column=1)
ttk.Label(frameState, textvariable=soldiersResult).grid(row=2, column=2)
ttk.Label(frameState, text='Рабочие').grid(row=3, column=0)
ttk.Entry(frameState, textvariable=workers, width=7).grid(row=3, column=1)
ttk.Label(frameState, textvariable=workersResult).grid(row=3, column=2)
ttk.Label(frameState, text='Личинки').grid(row=4, column=0)
ttk.Entry(frameState, textvariable=babies, width=7).grid(row=4, column=1)
ttk.Label(frameState, textvariable=babiesResult).grid(row=4, column=2)
ttk.Label(frameState, text='Ресурсы').grid(row=5, column=0)
ttk.Entry(frameState, textvariable=resources, width=7).grid(row=5, column=1)
ttk.Label(frameState, textvariable=resourcesResult).grid(row=5, column=2)
ttk.Label(frameState, text='Дней симуляции').grid(row=6, column=0)
ttk.Entry(frameState, textvariable=days, width=7).grid(row=6, column=1)
ttk.Label(frameState, textvariable=daysResult).grid(row=6, column=2)

frameConfig = ttk.Frame(borderwidth=1, relief=SOLID, padding=2)
frameConfig.grid(row=1, column=0, padx=2, pady=0, sticky=N)

ttk.Label(frameConfig, text='Конфигурация симулятора', padding=2,
          justify=CENTER, font=('Arial', 12)).grid(row=0, column=0, columnspan=2)

ttk.Label(frameConfig, text='Максимальное кол-во маток\n[1..20]').grid(row=1, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=maxQueens, width=7).grid(row=1, column=1)
ttk.Label(frameConfig, text='Яиц на каждую матку\n[1..10]').grid(row=2, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=queenBabies, width=7).grid(row=2, column=1)
ttk.Label(frameConfig, text='Минимальный ресурс на матку\n[1000..100000]').grid(row=3, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=queenResources, width=7).grid(row=3, column=1)
ttk.Label(frameConfig, text='Вероятность развития солдата\n[0.00..0.99]').grid(row=4, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=probSoldier, width=7).grid(row=4, column=1)
ttk.Label(frameConfig, text='Вероятность нападения извне\n[0.00..0.99]').grid(row=5, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=probAttack, width=7).grid(row=5, column=1)
ttk.Label(frameConfig, text='Кол-во нападающих\n(% от размера колонии) [1..100]').grid(row=6, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=pctAttack, width=7).grid(row=6, column=1)
ttk.Label(frameConfig, text='Сила нападающих\n[1..10]').grid(row=7, column=0, sticky=W)
ttk.Entry(frameConfig, textvariable=powerAttack, width=7).grid(row=7, column=1)

root.grid_rowconfigure(2, weight=10)

notebook = ttk.Notebook()
diagramTab = ttk.Frame(notebook)
historyTab = ttk.Frame(notebook)

diagramTab.pack(fill=BOTH, expand=True)
historyTab.pack(fill=BOTH, expand=True)

notebook.add(diagramTab, text='Диаграмма')
notebook.add(historyTab, text='История')
notebook.grid(row=0, column=1, rowspan=3, sticky=N)

canvas = Canvas(diagramTab, bg='white', width=800, height=400, bd=0, highlightthickness=0, relief='ridge')
canvas.pack(anchor=NW)

history = Listbox(historyTab, listvariable=historyResult, selectmode=SINGLE, justify=LEFT, height=25, width=70)
history.pack(side=LEFT, fill=BOTH, expand=1)

historyScrollbar = ttk.Scrollbar(historyTab, orient='vertical', command=history.yview)
historyScrollbar.pack(side=RIGHT, fill=Y)
history['yscrollcommand'] = historyScrollbar.set


def run():
    state = ants.AntsColonyState(queens.get(), soldiers.get(), workers.get(), babies.get(), resources.get())

    config = ants.AntsColonyConfig(
        maxQueens.get(), queenBabies.get(), queenResources.get(),
        probSoldier.get(), probAttack.get(), pctAttack.get(), powerAttack.get())

    antsColony = ants.AntColony(config, state)

    simulatedDays = antsColony.simulate(days.get())
    
    daysResult.set(simulatedDays)

    queensResult.set(antsColony.state.queens)
    soldiersResult.set(antsColony.state.soldiers)
    workersResult.set(antsColony.state.workers)
    babiesResult.set(antsColony.state.babies)
    resourcesResult.set(antsColony.state.resources)

    canvas.configure(height=simulatedDays)
    root.update()

    antsColony.drawHistory(canvas)
    historyResult.set(antsColony.listHistory())


ttk.Button(text='Запуск', command=run, padding=2).grid(
    row=2, column=0, pady=4, sticky=N)

root.mainloop()
