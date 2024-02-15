from benchmark import parse_arguments
from diagram_creator import sort_dimensions, create_chart, read_from_csv


file = False

if __name__ == "__main__":
    args = parse_arguments()

    print(args)
    if args.lhs == "opti":
        CSV_filename = "results_opti.csv"
    elif args.lhs == "classic":
        CSV_filename = "results_classic.csv"
    elif args.lhs == "centered":
        CSV_filename = "results_centered.csv"
    elif args.lhs == "maximin":
        CSV_filename = "results_maximin.csv"
    elif args.lhs == "centered_maximin":
        CSV_filename = "results_centered_maximin.csv"

read_from_csv(CSV_filename)
create_chart(sort_dimensions(), file, args.lhs)
