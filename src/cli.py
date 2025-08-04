import argparse
from src.indexer import build_index
from src.query_engine import get_query_engine
from src.utils import get_logger, print_sources_with_links

logger = get_logger('cli')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Query local notes CLI")
    parser.add_argument('-q', '--query', type=str, metavar='TEXT', help="Question to ask")
    parser.add_argument('-r', '--reload', action='store_true', help="Rebuild index")
    args = parser.parse_args()

    if args.reload:
        build_index()

    engine = get_query_engine()

    if args.query:        
        try:
            resp = engine.query(args.query)
            print("\n", resp.response)
            print("\nSOURCES:")
            print_sources_with_links(resp.source_nodes)
        except Exception as e:
            logger.error("Error querying: %s", e)
    else:
        
        print("Enter queries, type 'exit' to quit")
        while True:
            query = input("Query: (Type 'quit' or 'exit' to terminate program)")
            if query.lower() == 'exit' or query.lower() == 'quit':
                break
            try:
                resp = engine.query(query)
                print("\n", resp.response)
                print("\nSOURCES:")
                print_sources_with_links(resp.source_nodes)
            except Exception as e:
                logger.error("Error querying: %s", e)