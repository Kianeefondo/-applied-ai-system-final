"""Evaluation harness for retrieval accuracy and confidence.

Usage:
  python eval/evaluate.py --docs <docs_dir> --out results.json
"""
import argparse
import json
import logging
import os
from src.system import QAPipeline


def load_ground_truth(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate(docs_dir, gt_path, out_path):
    logging.basicConfig(level=logging.INFO)
    gt = load_ground_truth(gt_path)
    pipeline = QAPipeline(docs_dir=docs_dir, generator_mode='mock')
    results = []
    correct = 0
    total = 0
    confidences = []
    for item in gt:
        q = item['query']
        expected_doc = item.get('expected_doc')
        res = pipeline.answer(q)
        top_doc = res['retrieved'][0]['doc_id'] if res['retrieved'] else None
        conf = float(res.get('confidence', 0.0))
        ok = (top_doc == expected_doc)
        results.append({'query': q, 'top_doc': top_doc, 'expected': expected_doc, 'confidence': conf, 'correct': ok})
        correct += 1 if ok else 0
        total += 1
        confidences.append(conf)

    summary = {
        'accuracy': correct / total if total else 0.0,
        'mean_confidence': sum(confidences) / len(confidences) if confidences else 0.0,
        'total': total
    }

    out = {'summary': summary, 'results': results}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    logging.info('Wrote results to %s', out_path)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--docs', required=True)
    p.add_argument('--gt', default='eval/ground_truth.json')
    p.add_argument('--out', default='eval/results.json')
    args = p.parse_args()
    gt_path = args.gt
    if not os.path.isabs(gt_path):
        gt_path = os.path.join(os.getcwd(), gt_path)
    evaluate(args.docs, gt_path, args.out)


if __name__ == '__main__':
    main()
