from pygrn import grns, problems, evolution
import argparse
import os

parser = argparse.ArgumentParser(description='Evolve a GRN for regression')
parser.add_argument('--no-learn', dest='learn', action='store_const',
                    const=False, default=True,
                    help='Turn off learning')
parser.add_argument('--no-evo', dest='evo', action='store_const',
                    const=False, default=True,
                    help='Turn off evolution')
parser.add_argument('--lamarckian', dest='lamarckian', action='store_const',
                    const=True, default=False, help='Lamarckian evolution')
parser.add_argument('--unsupervised', dest='unsupervised', action='store_const',
                    const=True, default=False, help='Unsupervised evolution')
parser.add_argument('--stateful', dest='stateful', action='store_const',
                    const=True, default=False, help='Stateful model')
parser.add_argument('--id', type=str, help='Run id for logging')
parser.add_argument('--model', type=str, help='Model')
parser.add_argument('--seed', type=int, help='Random seed',
                    default=0)
parser.add_argument('--problem', type=str, help='Problem',
                    default='Prediction')
parser.add_argument('--epochs', type=int, help='Number of epochs', default=1)
parser.add_argument('--gens', type=int, help='Number of generations',
                    default=50)
parser.add_argument('--grn_file', type=str, help='Experts from GRN file',
                    default='')
parser.add_argument('--root_dir', type=str, help='Root directory',
                    default='./')

args = parser.parse_args()

log_dir = os.path.join(args.root_dir, 'logs')
grn_dir = os.path.join(args.root_dir, 'grns')
data_dir = os.path.join(args.root_dir, 'data')
log_file = os.path.join(log_dir, 'fits_' + args.id + '.log')

p = eval('problems.' + args.problem)
p = p(log_file, seed=args.seed, learn=args.learn, epochs=args.epochs,
      data_dir=data_dir, lamarckian=args.lamarckian,
      unsupervised=args.unsupervised, stateful=args.stateful,
      model=args.model)

newgrn = lambda: grns.DiffGRN()
if args.evo:
    grneat = evolution.Evolution(p, newgrn, run_id=args.id,
                                 grn_dir=grn_dir, log_dir=log_dir)
    grneat.run(args.gens)
elif args.grn_file:
    with open(args.grns, 'r') as f:
        for g in f.readlines():
            grn = newgrn()
            grn.from_str(g)
            p.generation = args.generation
            p.eval(grn)
else:
    for i in range(20):
        grn = newgrn()
        grn.random(p.nin, p.nout, 20)
        p.generation = i
        p.eval(grn)
