import argparse
import json
import logging
import sys
from .system import QAPipeline

def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--docs', default='data/docs')
    parser.add_argument('--mode', default='mock')
    args = parser.parse_args()
    configure_logging()
    pipeline = QAPipeline(docs_dir=args.docs, generator_mode=args.mode)
    res = pipeline.answer(args.query)
    print(json.dumps(res, indent=2))

if __name__ == '__main__':
    main()
