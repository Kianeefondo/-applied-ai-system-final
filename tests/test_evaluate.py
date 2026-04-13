import os
import importlib.util


def load_eval_module():
    path = os.path.expanduser('~/project/eval/evaluate.py')
    spec = importlib.util.spec_from_file_location('eval_module', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_evaluate_runs(tmp_path):
    mod = load_eval_module()
    project_root = os.path.expanduser('~/project')
    docs = os.path.join(project_root, 'data', 'docs')
    gt = os.path.join(project_root, 'eval', 'ground_truth.json')
    out = tmp_path / 'out.json'
    res = mod.evaluate(docs, gt, str(out))
    assert 'summary' in res
    assert res['summary']['total'] == 3
