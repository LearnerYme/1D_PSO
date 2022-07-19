from utils import *

conf = args(1, 2, 2, 0.8, -1, 1, 0.2, 20)
gg = group(50, conf, 100)
gg.info()
gg.draw('./fig')
for i in range(gg.imax):
    gg.iteration()
    if i%10 == 0:
        gg.info()
    gg.draw('./fig')
gg.info(True)
print(f'{gg.best_group=}, {gg.best_x=}')