import numpy as np

def calculate_segments(case, number_of_segments=10):
    return sort_segments(generate_segments(case, number_of_segments))


def generate_segments(case, number_of_segments):
    segments = []
    for g in case.gen_name:
        pmin, pmax = case.gen.loc[g, ['PMIN', 'PMAX']]
        N = int(case.gencost.loc[g, 'NCOST'])
        cost = case.gencost.loc[g, ['COST_{}'.format(i) for i in range(0, N )]]
        x = np.linspace(pmin, pmax, number_of_segments+1)
        for i, p in enumerate(x[:-1]):
            # p = ( x[i] + x[i+1] ) / 2.0
            p_seg = dict()
            p_seg['slope'] = incremental_cost(p, cost, N)
            p_seg['segment'] = (x[i], x[i+1])
            p_seg['name'] = g
            segments.append(p_seg)
    return segments

def sort_segments(segments):
    minimum = sorted(segments, key=lambda x: x['slope'])[0]['segment'][0]
    for i, d in enumerate(sorted(segments, key=lambda x: x['slope'])):
        d['segment'] = (minimum, d['segment'][1] - d['segment'][0] + minimum)
        minimum = d['segment'][1]

    return sorted(segments, key=lambda x: x['slope'])


def incremental_cost(p, cost, N):
    return sum(cost['COST_{}'.format(i)] * i * p ** (i-1) for i in range(1, N))


