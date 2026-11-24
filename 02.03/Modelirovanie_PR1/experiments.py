"""Эксперименты: python experiments.py [--variant 1].

По умолчанию выполняется демонстрационный расчёт; --variant 1 запускает
серии для варианта 1. Графики строятся через matplotlib или ReportLab.
"""
import argparse
import csv
import math
from pathlib import Path
from model import simulate, first_95

OUT = Path(__file__).resolve().parent


def cases(variant):
    if variant == 1:
        a, k, n, t = 0.45, 80000, 3000, 30
        aa = [0.3, 0.45, 0.6, 1.2, 1.9, 2.2, 2.9]
        nn = [500, 16000, 72000, 84000]
        kk = [48000, 120000]
    else:
        a, k, n, t = 0.6, 100000, 5000, 24
        aa = [0.3, 0.6, 1.2, 1.9, 2.2, 2.55, 2.9]
        nn = [500, 20000, 90000, 105000]
        kk = [60000, 150000]
    result = [('a', x, k, n, t) for x in aa]
    result += [('N0', a, k, x, t) for x in nn]
    result += [('K', a, x, n, t) for x in kk]
    return result


def make_rows(variant):
    rows = []
    for series, a, k, n, months in cases(variant):
        values = simulate(a, k, n, months)
        tail = values[-8:]
        tolerance = k * 1e-8  # не считать погрешность округления перелётом
        crossings = sum((values[i] - k) * (values[i + 1] - k) < 0
                        and abs(values[i] - k) > tolerance
                        and abs(values[i + 1] - k) > tolerance
                        for i in range(len(values) - 1))
        rows.append({'series': series, 'a': a, 'K': k, 'N0': n, 'T': months,
                     't95': first_95(values, k), 'crossings': crossings,
                     'tail_min': min(tail), 'tail_max': max(tail),
                     'tail_range': max(tail) - min(tail), 'values': values})
    return rows


def plot_matplotlib(rows, prefix):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for num, series in enumerate(('a', 'N0', 'K'), 1):
        fig, ax = plt.subplots(figsize=(9, 5))
        for row in rows:
            if row['series'] != series:
                continue
            label = f"{series} = {row[series]}"
            ax.plot(range(row['T'] + 1), row['values'], marker='.', label=label)
        if series != 'K':
            ax.axhline(rows[0]['K'], color='gray', linestyle='--', label='K')
        ax.set(title=f'Серия {num}: влияние {series}', xlabel='Месяц t', ylabel='Число пользователей N(t)')
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT / f'{prefix}_series{num}.png', dpi=150)
        plt.close(fig)


def plot_reportlab(rows, prefix):
    # Запасной способ построить те же графики, если matplotlib не установлен.
    import pypdfium2
    from reportlab.graphics.shapes import Drawing, String
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics import renderPDF
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    pdfmetrics.registerFont(TTFont('GraphFont', r'C:\Windows\Fonts\arial.ttf'))
    palette = [colors.HexColor(x) for x in
               ('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2')]
    for num, series in enumerate(('a', 'N0', 'K'), 1):
        selected = [row for row in rows if row['series'] == series]
        drawing = Drawing(800, 480)
        drawing.add(String(110, 448, f'Серия {num}. Влияние {series}', fontName='GraphFont', fontSize=17))
        graph = LinePlot()
        graph.x, graph.y, graph.width, graph.height = 80, 95, 610, 320
        graph.data = [[(t, value) for t, value in enumerate(row['values'])] for row in selected]
        if series != 'K':
            graph.data.append([(0, selected[0]['K']), (selected[0]['T'], selected[0]['K'])])
        graph.xValueAxis.valueMin = 0
        graph.xValueAxis.valueMax = selected[0]['T']
        graph.xValueAxis.valueStep = 5
        graph.yValueAxis.valueMin = 0
        maximum = max(max(row['values']) for row in selected)
        step = math.ceil(maximum / 5 / 10000) * 10000
        graph.yValueAxis.valueMax = step * 5
        graph.yValueAxis.valueStep = step
        graph.xValueAxis.labels.fontName = 'GraphFont'
        graph.yValueAxis.labels.fontName = 'GraphFont'
        graph.xValueAxis.labels.fontSize = 9
        graph.yValueAxis.labels.fontSize = 9
        for i, row in enumerate(selected):
            graph.lines[i].strokeColor = palette[i]
            graph.lines[i].strokeWidth = 2
            x = 100 + (i % 3) * 225
            y = 54 - (i // 3) * 17
            drawing.add(String(x, y, f"{series} = {row[series]:g}",
                               fontName='GraphFont', fontSize=10, fillColor=palette[i]))
        if series != 'K':
            graph.lines[len(selected)].strokeColor = colors.grey
            graph.lines[len(selected)].strokeDashArray = [4, 3]
            drawing.add(String(710, 400, f"K = {selected[0]['K']}",
                               fontName='GraphFont', fontSize=9, fillColor=colors.grey))
        drawing.add(graph)
        drawing.add(String(325, 74, 'Месяц t', fontName='GraphFont', fontSize=11))
        drawing.add(String(80, 426, 'Число пользователей N(t)', fontName='GraphFont', fontSize=11))
        pdf = pypdfium2.PdfDocument(renderPDF.drawToString(drawing))
        pdf[0].render(scale=1.5).to_pil().save(OUT / f'{prefix}_series{num}.png')
        pdf.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', type=int, choices=[1], help='номер варианта')
    args = parser.parse_args()
    rows = make_rows(args.variant)
    prefix = 'variant1' if args.variant else 'demo'
    columns = ['series', 'a', 'K', 'N0', 'T', 't95', 'crossings',
               'tail_min', 'tail_max', 'tail_range']
    with (OUT / f'{prefix}_experiments.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    try:
        plot_matplotlib(rows, prefix)
        print('Графики построены с помощью matplotlib.')
    except ModuleNotFoundError as error:
        if not error.name.startswith('matplotlib'):
            raise
        plot_reportlab(rows, prefix)
        print('matplotlib не установлен; графики построены с помощью ReportLab.')
    print(f'Созданы таблица и три графика для {prefix}.')


if __name__ == '__main__':
    main()
